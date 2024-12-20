# from fastapi import APIRouter
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
# from sqlalchemy.orm import DeclarativeBase
# from .config import config

# app = APIRouter(prefix="/db")

# engine = create_async_engine(url=f'postgresql+asyncpg://{config.user}:{config.password}@{config.host}/{config.database}')

# async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# async def get_session():
#     async with  async_session() as session:
#         yield session
#         await session.commit()

# class Base(AsyncAttrs, DeclarativeBase):
#     pass

# @app.get("/")
# async def create_db():
#     async with engine.begin() as conn:
#         try:
#             await conn.run_sync(Base.metadata.drop_all)
#         except:
#             pass
#         await  conn.run_sync(Base.metadata.create_all)
#     return({"msg":"db creat! =)"})
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from .config import config

app = APIRouter(prefix="/db")

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(
    url=f'postgresql+asyncpg://{config.user}:{config.password}@{config.host}/{config.database}'
)

# Фабрика асинхронных сессий
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Зависимость для получения сессии
async def get_session():
    async with async_session() as session:
        yield session


# Базовый класс для моделей
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Эндпоинт для создания базы данных
@app.get("/")
async def create_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except Exception as e:
            # Логируйте исключение, если это необходимо
            print(f"Ошибка при удалении таблиц: {e}")
        await conn.run_sync(Base.metadata.create_all)
    return {"msg": "Database created! =)"}
