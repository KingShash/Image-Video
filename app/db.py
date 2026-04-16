from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import String, Text, DateTime,ForeignKey , Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime





DATABASE_URL = "sqlite+aiosqlite:///./test.db" #To connect to local database file called test.db


class Base(DeclarativeBase):
    pass


class Post(Base):

    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  #all clases that inherit from Base will be created as tables in the database\


async def get_async_session() -> AsyncGenerator[AsyncSession, None]: #get session which allows to write and read data async
    async with async_session_maker() as session:
        yield session


