from sqlalchemy.sql._typing import _ColumnExpressionArgument
from sqlalchemy.ext.asyncio import AsyncSession


class BaseQueryExpression:
    def complete(self) -> _ColumnExpressionArgument[bool]:
        raise NotImplementedError


class BaseDBRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self.session.close()
