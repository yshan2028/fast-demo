import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from backend.config import settings
from backend.models import Role, User
from backend.server import app

DB_URL = "sqlite://:memory:"
username, password = ["admin", "a12345678"]


# 参考文档
# https://stackoverflow.com/questions/65716897/testing-in-fastapi-using-tortoise-orm/69055243
# https://github.com/waketzheng/fastapi-tortoise-pytest-demo.git

async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
            db_url=db_url, modules={"base": settings.tortoise_orm_model_modules}, _create_db=create_db
            )
    if create_db:
        print(f"Database created! {db_url = }")
    if schemas:
        await Tortoise.generate_schemas()
        print("Success to generate schemas")


async def init(db_url: str = DB_URL):
    await init_db(db_url, True, True)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test" + settings.url_prefix) as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="session")
async def client_with_token(client: AsyncClient):
    data = {"username": username, "password": password}
    response = await client.post("/test/token", data=data)
    token_type = response.json().get('token_type')
    access_token = response.json().get('access_token')
    client.headers['Authorization'] = f"{token_type} {access_token}"
    yield client


async def init_sql():
    # 设置超管账号
    user = await User.create(username=username, password=password, is_active=True, is_superuser=True)
    await user.set_password(password)
    # 插入一些账号数据
    for i in range(25):
        user = await User.create(username=f"username{i}", password="xx")
        await user.set_password(f"password{i}")

    # 插入一些角色数据
    for i in range(25):
        await Role.create(role_name=f"role_name{i}")


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    await init_sql()
    yield
    await Tortoise._drop_databases()
