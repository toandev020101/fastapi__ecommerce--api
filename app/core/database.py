from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.settings import get_settings

settings = get_settings()
Base = declarative_base()


class AsyncDatabaseSession:
    """Wrapper class for managing asynchronous database sessions."""

    def __init__(self) -> None:
        self.session = None
        self.engine = None

    def __getattr__(self, name):
        return getattr(self.session, name)

    def init(self):
        # Initialize the database engine and session
        self.engine = create_async_engine(settings.DATABASE_URI, future=True, echo=True)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        # Asynchronously create all tables defined in SQLModel.metadata
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


# Create an instance of the database session
db = AsyncDatabaseSession()


async def commit_rollback():
    try:
        # Asynchronously commit changes
        await db.commit()
    except Exception as e:
        # Rollback changes in case of an exception
        await db.rollback()
        raise ValueError(f"Lỗi máy chủ: {e}")
