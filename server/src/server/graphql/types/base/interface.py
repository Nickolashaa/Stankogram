from datetime import datetime

import strawberry


@strawberry.interface
class IBaseType:
    id: int
    created_at: datetime
    updated_at: datetime


@strawberry.interface
class IBaseMeta:
    count: int
