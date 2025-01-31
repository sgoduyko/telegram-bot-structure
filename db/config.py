import os

from sqlalchemy.ext.asyncio import create_async_engine

db_user = os.getenv("POSTGRES_USER") or ValueError("Postgres user is null")
db_pass = os.getenv("POSTGRES_PASSWORD") or ValueError("Postgres pass is null")
db_name = os.getenv("POSTGRES_DB") or ValueError("Postgres db is null")
host = os.getenv("POSTGRES_HOST") or ValueError("Postgres host is null")
port = os.getenv("POSTGRES_PORT") or ValueError("Postgres port is null")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{host}:{port}/{db_name}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
