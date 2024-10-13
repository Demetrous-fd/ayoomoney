from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


def create_connection_pool(database_dsn: str) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(url=database_dsn, echo=False)
    pool = async_sessionmaker(engine, expire_on_commit=False)

    return pool


async def create_connection(session_pool: async_sessionmaker[AsyncSession]):
    return session_pool()
