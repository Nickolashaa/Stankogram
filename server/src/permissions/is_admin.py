from fastapi import Depends, HTTPException

from ..dependencies import get_current_user
from ..schemas.users import UserResponse


async def is_admin(user: UserResponse = Depends(get_current_user)) -> None:
    if user.is_admin is False:
        raise HTTPException(status_code=403, detail="Access denied")
