from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

database_url = 'sqlite:///data/sqlite.db'
engine = create_engine(database_url)
async_engine = create_async_engine("sqlite+aiosqlite:///data/sqlite.db")
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass


class DBUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    user_email = Column(String(255), nullable=False)
    hash_password = Column(String(255), nullable=False, unique=True)
    balance = Column(Integer, default=500)


class DBPredictor(Base):
    __tablename__ = "predictor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    filename = Column(String(255), nullable=False, unique=True)
    cost = Column(Integer)


class DBPrediction(Base):
    __tablename__ = "prediction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    predictor_id = Column(Integer, ForeignKey("predictor.id"))
    is_success = Column(Boolean, nullable=True, default=None)
    is_finished = Column(Boolean, nullable=False, default=False)
    output_data = Column(String, nullable=True)
    error_info = Column(String(255), nullable=True)


def create_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
