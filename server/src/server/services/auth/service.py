import asyncio
from datetime import UTC, datetime, timedelta
from pathlib import Path
from secrets import choice
from string import Template, ascii_letters, digits
from typing import Sequence, Unpack
from uuid import UUID, uuid4

import bcrypt
import jwt
from pydantic import TypeAdapter, ValidationError
from pydantic.networks import EmailStr
from sqlalchemy import Select, delete, func, insert, or_, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ...config import (
    APP_BASE_URL,
    JWT_ACCESS_EXP_MINUTES,
    JWT_REFRESH_EXP_DAYS,
    PASSWORD_LEN,
    PASSWORD_RESET_CODE_EXP_MINUTES,
    PASSWORD_RESET_CODE_LEN,
    USERS_IMPORT_MAX_FILE_SIZE,
    USERS_IMPORT_MAX_ROWS,
    USERS_IMPORT_MAX_SCAN_ROWS,
    USERS_IMPORT_MAX_VALUE_LEN,
)
from ...database.models.auth import CancelledToken, PasswordResetCode, User
from ...enums.users import UserRole
from ...utils.smtp import send_email
from ...utils.xlsx import (
    add_column_choices,
    add_fields_sheet,
    add_table_sheet,
    add_text_sheet,
    apply_code_style,
    apply_failure_style,
    apply_success_style,
    create_workbook,
    read_rows,
    to_bytes,
)
from ..base import BasePagination, BaseService
from ..exceptions import (
    InvalidInput,
    ObjectAlreadyExists,
    ObjectNotFound,
    Unauthorized,
)
from .schemas import (
    CreatedUserSchema,
    JWTPayload,
    JWTsSchema,
    UserImportResultSchema,
    UserImportRowSchema,
    UserResponse,
    UsersImportReportSchema,
    XlsxFileSchema,
)
from .types import (
    UserCreateParams,
    UserCredentials,
    UserGetListFilters,
    UserUpdateParams,
)

_PASSWORD_RESET_EMAIL_TEMPLATE = Template(
    (Path(__file__).resolve().parent / "password_reset_email.html").read_text(
        encoding="utf-8"
    )
)
_PASSWORD_RESET_CONFIRM_EMAIL_TEMPLATE = Template(
    (Path(__file__).resolve().parent / "password_reset_confirm_email.html").read_text(
        encoding="utf-8"
    )
)

_EMAIL_ADAPTER = TypeAdapter(EmailStr)

_IMPORT_TEMPLATE_FILENAME = "Шаблон импорта сотрудников.xlsx"
_IMPORT_REPORT_FILENAME = "Результат импорта сотрудников.xlsx"

_IMPORT_HEADERS = ("Имя", "Фамилия", "Отчество", "Почта", "Роль")
_IMPORT_RESULT_HEADERS = ("Результат", "Пароль", "Причина")
_IMPORT_SUCCESS = "ОК"
_IMPORT_FAILURE = "Ошибка"

_IMPORT_ROLE_LABELS = {
    UserRole.STUDENT: "Студент",
    UserRole.TEACHER: "Преподаватель",
}
_IMPORT_ROLES = {
    label.casefold(): role for role, label in _IMPORT_ROLE_LABELS.items()
} | {role.value.casefold(): role for role in UserRole}

_IMPORT_ROLE_HINT = " или ".join(
    f"{label} ({role.value})" for role, label in _IMPORT_ROLE_LABELS.items()
)
_IMPORT_HEADER_HINTS = {
    "Отчество": "если есть",
    "Почта": "ivanov@example.ru",
    "Роль": _IMPORT_ROLE_HINT,
}
_IMPORT_DISPLAY_HEADERS = tuple(
    title
    if title not in _IMPORT_HEADER_HINTS
    else f"{title} — {_IMPORT_HEADER_HINTS[title]}"
    for title in _IMPORT_HEADERS
)

_IMPORT_SHEET_TITLE = "Сотрудники"
_IMPORT_SUMMARY_SHEET_TITLE = "Итоги"
_IMPORT_GUIDE_SHEET_TITLE = "Инструкция"

_IMPORT_TEMPLATE_WIDTHS = (22, 22, 26, 34, 34)

_IMPORT_GUIDE_LINES = (
    f"Заполните лист «{_IMPORT_SHEET_TITLE}», начиная со второй строки.",
    "Имя, Фамилия, Почта и Роль обязательны, Отчество можно оставить пустым.",
    "Почта должна быть корректной и не должна повторяться.",
    f"Роль выбирается из списка в ячейке: {_IMPORT_ROLE_HINT}.",
    "Строки без данных пропускаются.",
    f"За один раз можно загрузить не больше {USERS_IMPORT_MAX_ROWS} строк.",
    "В ответ вернётся тот же файл с колонками «Результат», «Пароль» и «Причина».",
    "Пароли показываются один раз — сохраните файл и передайте их сотрудникам.",
    "Забытый пароль восстанавливается через «Забыли пароль?» на странице входа.",
)


class AuthService(BaseService):
    @staticmethod
    def _generate_password() -> str:
        return "".join(choice(ascii_letters + digits) for _ in range(PASSWORD_LEN))

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt()).decode()

    @staticmethod
    def _generate_password_reset_code() -> str:
        return "".join(choice(digits) for _ in range(PASSWORD_RESET_CODE_LEN))

    @staticmethod
    def _generate_password_reset_email(user_id: int, code: str) -> str:
        url = f"{APP_BASE_URL}/reset-password-confirm?id={user_id}&code={code}"
        return _PASSWORD_RESET_EMAIL_TEMPLATE.substitute(url=url)

    @staticmethod
    def _generate_password_reset_confirm_email(email: str, password: str) -> str:
        return _PASSWORD_RESET_CONFIRM_EMAIL_TEMPLATE.substitute(
            email=email, password=password, app_url=APP_BASE_URL
        )

    @staticmethod
    def generate_jwts(id: int, is_admin: bool) -> JWTsSchema:
        return JWTsSchema(
            access_token=JWTPayload(
                id=id,
                is_admin=is_admin,
                jti=str(uuid4()),
                type="access",
                exp=datetime.now(UTC) + timedelta(minutes=JWT_ACCESS_EXP_MINUTES),
            ).generate_token(),
            refresh_token=JWTPayload(
                id=id,
                is_admin=is_admin,
                jti=str(uuid4()),
                type="refresh",
                exp=datetime.now(UTC) + timedelta(days=JWT_REFRESH_EXP_DAYS),
            ).generate_token(),
        )

    async def cancel_token(self, jti: UUID) -> None:
        stmt = insert(CancelledToken).values(jti=jti)
        try:
            await self._execute(stmt)
        except IntegrityError:
            raise ObjectAlreadyExists(f"Token with jti {jti} already exists")

    async def create(
        self,
        **values: Unpack[UserCreateParams],
    ) -> CreatedUserSchema:
        password = self._generate_password()
        hashed_password = self._hash_password(password)

        stmt = (
            insert(User)
            .values(
                hashed_password=hashed_password,
                **values,
            )
            .returning(User)
        )

        try:
            res = await self._execute(stmt)
        except IntegrityError:
            raise ObjectAlreadyExists(
                f"User with email {values.get('email')} already exists"
            )

        return CreatedUserSchema(
            user=UserResponse.model_validate(res.scalar_one()),
            password=password,
        )

    async def get(
        self,
        id: int,
    ) -> UserResponse:
        stmt = select(User).where(User.id == id)
        res = await self._execute(stmt)
        entity = res.scalar_one_or_none()
        if entity is None:
            raise ObjectNotFound(
                f"User with id {id} not found",
            )
        return UserResponse.model_validate(entity)

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[User]],
        **filters: Unpack[UserGetListFilters],
    ) -> Select[tuple[User]]:
        if (search_query := filters.get("search_query")) is not None:
            stmt = stmt.where(
                or_(
                    User.name.icontains(search_query),
                    User.surname.icontains(search_query),
                    User.patronymic.icontains(search_query),
                    User.email.icontains(search_query),
                )
            )

        if (role := filters.get("role")) is not None:
            stmt = stmt.where(User.role == role)

        if (is_admin := filters.get("is_admin")) is not None:
            stmt = stmt.where(User.is_admin == is_admin)

        if (ids := filters.get("ids")) is not None:
            stmt = stmt.where(User.id.in_(ids))

        return stmt

    async def get_list(
        self,
        pagination: BasePagination | None = None,
        **filters: Unpack[UserGetListFilters],
    ) -> list[UserResponse]:
        stmt = select(User).order_by(User.id)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        res = await self._execute(stmt)

        return [UserResponse.model_validate(entity) for entity in res.scalars().all()]

    async def count(
        self,
        **filters: Unpack[UserGetListFilters],
    ) -> int:
        stmt = select(User)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = self._get_count_stmt(stmt)

        res = await self._execute(stmt)

        return res.scalar_one()

    async def get_by_email(
        self,
        email: str,
    ) -> UserResponse:
        stmt = select(User).where(User.email == email)
        res = await self._execute(stmt)
        entity = res.scalar_one_or_none()
        if entity is None:
            raise ObjectNotFound(
                f"User with email {email} not found",
            )
        return UserResponse.model_validate(entity)

    async def login(
        self,
        **credentials: Unpack[UserCredentials],
    ) -> UserResponse:
        user = await self.get_by_email(credentials.get("email"))

        if bcrypt.checkpw(
            credentials.get("password").encode(), user.hashed_password.encode()
        ):
            return user

        raise ObjectNotFound(
            f"User with email {credentials.get('email')} and password "
            f"{credentials.get('password')} not found"
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        stmt = delete(User).where(User.id == id)
        await self._execute(stmt)

    async def update(
        self,
        id: int,
        **values: Unpack[UserUpdateParams],
    ) -> UserResponse:
        await self.get(id)

        stmt = update(User).where(User.id == id).values(**values).returning(User)

        try:
            res = await self._execute(stmt)
            return UserResponse.model_validate(res.scalar_one())
        except IntegrityError:
            raise ObjectAlreadyExists(
                f"User with email {values.get('email')} already exists"
            )

    async def mark_last_online(
        self,
        id: int,
    ) -> UserResponse:
        stmt = (
            update(User)
            .where(User.id == id)
            .values(last_online_at=datetime.now(UTC))
            .returning(User)
        )

        res = await self._execute(stmt)
        entity = res.scalar_one_or_none()
        if entity is None:
            raise ObjectNotFound(
                f"User with id {id} not found",
            )
        return UserResponse.model_validate(entity)

    async def reset_password_request(
        self,
        email: str,
    ) -> None:
        user = await self.get_by_email(email)

        code = self._generate_password_reset_code()
        stmt = (
            insert(PasswordResetCode)
            .values(
                user_id=user.id,
                value=code,
            )
            .returning(PasswordResetCode)
        )

        await self._execute(stmt)

        await send_email(
            to_email=user.email,
            subject="Stankogram:Подтверждение сброса пароля",
            body=self._generate_password_reset_email(
                user_id=user.id,
                code=code,
            ),
        )

    async def reset_password_confirm(
        self,
        id: int,
        code: str,
    ) -> None:
        user = await self.get(id)

        stmt = select(PasswordResetCode).where(
            PasswordResetCode.user_id == user.id,
            PasswordResetCode.value == code,
            PasswordResetCode.created_at
            >= datetime.now(UTC) - timedelta(minutes=PASSWORD_RESET_CODE_EXP_MINUTES),
        )

        res = await self._execute(stmt)
        entity = res.scalar_one_or_none()
        if entity is None:
            raise ObjectNotFound(
                f"Valid password reset code for user {user.id} not found"
            )

        stmt = delete(PasswordResetCode).where(PasswordResetCode.id == entity.id)
        await self._execute(stmt)

        new_password = self._generate_password()
        new_hashed_password = self._hash_password(new_password)

        stmt = (
            update(User)
            .where(User.id == id)
            .values(hashed_password=new_hashed_password)
        )
        await self._execute(stmt)

        await send_email(
            to_email=user.email,
            subject="Stankogram:Данные для входа",
            body=self._generate_password_reset_confirm_email(
                email=user.email,
                password=new_password,
            ),
        )

    async def get_from_token(
        self,
        token: str,
    ) -> UserResponse:
        try:
            payload = JWTPayload.from_token(token)
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Expired token")
        except jwt.InvalidTokenError:
            raise Unauthorized("Invalid token")

        if payload.type == "refresh":
            raise Unauthorized("Invalid token type")

        return await self.get(payload.id)

    @staticmethod
    def _parse_import_role(value: str) -> UserRole | None:
        return _IMPORT_ROLES.get(value.casefold())

    @classmethod
    def _validate_import_row(cls, row: UserImportRowSchema) -> str | None:
        if not row.name:
            return "Не указано имя"
        if not row.surname:
            return "Не указана фамилия"
        if not row.email:
            return "Не указана почта"
        for label, value in (
            ("Имя", row.name),
            ("Фамилия", row.surname),
            ("Отчество", row.patronymic or ""),
            ("Почта", row.email),
        ):
            if len(value) > USERS_IMPORT_MAX_VALUE_LEN:
                return f"{label} длиннее {USERS_IMPORT_MAX_VALUE_LEN} символов"
        try:
            _EMAIL_ADAPTER.validate_python(row.email)
        except ValidationError:
            return "Некорректный формат почты"
        if not row.role:
            return "Не указана роль"
        if cls._parse_import_role(row.role) is None:
            return "Неизвестная роль, допустимо: " + ", ".join(
                _IMPORT_ROLE_LABELS.values()
            )
        return None

    @staticmethod
    def _import_failure(
        row: UserImportRowSchema,
        reason: str,
    ) -> UserImportResultSchema:
        return UserImportResultSchema(row=row, is_success=False, reason=reason)

    async def _rollback_quietly(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError:
            pass

    @staticmethod
    def _normalize_import_header(cell: str) -> str:
        return cell.partition("—")[0].strip().casefold()

    @classmethod
    def _is_import_header_valid(cls, cells: Sequence[str]) -> bool:
        return [cls._normalize_import_header(cell) for cell in cells] == [
            title.casefold() for title in _IMPORT_HEADERS
        ]

    @classmethod
    def _parse_import_rows(cls, content: bytes) -> list[UserImportRowSchema]:
        cells_rows = read_rows(content, len(_IMPORT_HEADERS))
        rows: list[UserImportRowSchema] = []

        try:
            header = next(cells_rows, None)
            if header is None or not cls._is_import_header_valid(header):
                raise InvalidInput(
                    "Первая строка файла должна содержать колонки: "
                    + ", ".join(_IMPORT_HEADERS)
                )

            for number, cells in enumerate(cells_rows, start=2):
                if number > USERS_IMPORT_MAX_SCAN_ROWS:
                    raise InvalidInput(
                        f"В файле больше {USERS_IMPORT_MAX_SCAN_ROWS} строк"
                    )

                if not any(cells):
                    continue

                if len(rows) == USERS_IMPORT_MAX_ROWS:
                    raise InvalidInput(
                        f"В файле больше {USERS_IMPORT_MAX_ROWS} строк с сотрудниками"
                    )

                name, surname, patronymic, email, role = cells
                rows.append(
                    UserImportRowSchema(
                        name=name,
                        surname=surname,
                        patronymic=patronymic or None,
                        email=email,
                        role=role,
                    )
                )
        finally:
            cells_rows.close()

        if not rows:
            raise InvalidInput("В файле нет ни одного сотрудника")

        return rows

    @classmethod
    def _read_import_rows(cls, content: bytes) -> list[UserImportRowSchema]:
        if len(content) > USERS_IMPORT_MAX_FILE_SIZE:
            raise InvalidInput(
                f"Файл больше {USERS_IMPORT_MAX_FILE_SIZE // 1024 // 1024} МБ"
            )

        try:
            return cls._parse_import_rows(content)
        except InvalidInput:
            raise
        except Exception:
            raise InvalidInput(
                "Не удалось прочитать файл, ожидается таблица формата xlsx"
            )

    @staticmethod
    def _build_import_report(results: Sequence[UserImportResultSchema]) -> bytes:
        workbook = create_workbook()

        sheet = add_table_sheet(
            workbook,
            title=_IMPORT_SHEET_TITLE,
            headers=_IMPORT_DISPLAY_HEADERS + _IMPORT_RESULT_HEADERS,
            rows=[
                (
                    result.row.name,
                    result.row.surname,
                    result.row.patronymic or "",
                    result.row.email,
                    result.row.role,
                    _IMPORT_SUCCESS if result.is_success else _IMPORT_FAILURE,
                    result.password or "",
                    result.reason or "",
                )
                for result in results
            ],
        )

        for number, result in enumerate(results, start=2):
            cell = sheet.cell(row=number, column=len(_IMPORT_HEADERS) + 1)
            if result.is_success:
                apply_success_style(cell)
            else:
                apply_failure_style(cell)

            apply_code_style(sheet.cell(row=number, column=len(_IMPORT_HEADERS) + 2))

        succeeded = sum(1 for result in results if result.is_success)
        summary = add_fields_sheet(
            workbook,
            title=_IMPORT_SUMMARY_SHEET_TITLE,
            heading="Итоги импорта",
            fields=(
                ("Всего строк", len(results)),
                ("Зарегистрировано", succeeded),
                ("С ошибками", len(results) - succeeded),
            ),
        )
        apply_success_style(summary.cell(row=4, column=2))
        apply_failure_style(summary.cell(row=5, column=2))

        return to_bytes(workbook)

    @staticmethod
    def build_import_template() -> XlsxFileSchema:
        workbook = create_workbook()

        sheet = add_table_sheet(
            workbook,
            title=_IMPORT_SHEET_TITLE,
            headers=_IMPORT_DISPLAY_HEADERS,
            widths=_IMPORT_TEMPLATE_WIDTHS,
        )
        add_column_choices(
            sheet,
            column=len(_IMPORT_HEADERS),
            choices=list(_IMPORT_ROLE_LABELS.values()),
            rows=USERS_IMPORT_MAX_ROWS,
            prompt=f"Допустимые значения: {_IMPORT_ROLE_HINT}",
        )
        add_text_sheet(
            workbook,
            title=_IMPORT_GUIDE_SHEET_TITLE,
            heading="Импорт сотрудников",
            lines=_IMPORT_GUIDE_LINES,
        )

        return XlsxFileSchema(
            filename=_IMPORT_TEMPLATE_FILENAME,
            content=to_bytes(workbook),
        )

    async def import_users(
        self,
        content: bytes,
    ) -> UsersImportReportSchema:
        results = await self._register_import_rows(self._read_import_rows(content))
        succeeded = sum(1 for result in results if result.is_success)

        return UsersImportReportSchema(
            file=XlsxFileSchema(
                filename=_IMPORT_REPORT_FILENAME,
                content=self._build_import_report(results),
            ),
            total=len(results),
            succeeded=succeeded,
            failed=len(results) - succeeded,
        )

    async def _get_existing_emails(self, emails: Sequence[str]) -> set[str]:
        if not emails:
            return set()

        stmt = select(User.email).where(func.lower(User.email).in_(emails))
        res = await self._execute(stmt)

        return {email.casefold() for email in res.scalars().all()}

    async def _create_import_user(
        self,
        row: UserImportRowSchema,
        password: str,
    ) -> None:
        hashed_password = await asyncio.to_thread(self._hash_password, password)

        stmt = insert(User).values(
            name=row.name,
            surname=row.surname,
            patronymic=row.patronymic,
            email=row.email,
            hashed_password=hashed_password,
            role=self._parse_import_role(row.role),
        )

        await self._execute(stmt)
        await self._session.commit()

    async def _register_import_rows(
        self,
        rows: Sequence[UserImportRowSchema],
    ) -> list[UserImportResultSchema]:
        results: list[UserImportResultSchema] = []
        pending: list[int] = []
        emails: set[str] = set()

        for row in rows:
            reason = self._validate_import_row(row)
            if reason is None and row.email.casefold() in emails:
                reason = "Почта повторяется в файле"

            if reason is None:
                emails.add(row.email.casefold())
                pending.append(len(results))
                results.append(
                    UserImportResultSchema(row=row, is_success=True, reason=None)
                )
                continue

            results.append(self._import_failure(row, reason))

        existing = await self._get_existing_emails(sorted(emails))

        for index in pending:
            row = results[index].row

            if row.email.casefold() in existing:
                results[index] = self._import_failure(
                    row, "Пользователь с такой почтой уже зарегистрирован"
                )
                continue

            password = self._generate_password()
            try:
                await self._create_import_user(row, password)
            except IntegrityError:
                await self._rollback_quietly()
                results[index] = self._import_failure(
                    row, "Пользователь с такой почтой уже зарегистрирован"
                )
                continue
            except Exception:
                await self._rollback_quietly()
                results[index] = self._import_failure(
                    row, "Не удалось сохранить сотрудника"
                )
                continue

            results[index] = UserImportResultSchema(
                row=row,
                is_success=True,
                reason=None,
                password=password,
            )

        return results
