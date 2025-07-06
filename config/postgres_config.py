from sqlalchemy import create_engine
from config.settings import settings

# DB_HOST = "0.0.0.0"  # or your cloud DB endpoint
# DB_HOST = "localhost"  # or your cloud DB endpoint
DB_HOST = "host.docker.internal"  # or your cloud DB endpoint
DB_PORT = "5432"
DB_NAME = "mydatabase"

DATABASE_URL = f"postgresql://{settings.POSTGRES_DB_USER}:{settings.POSTGRES_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
POSTGRES_ENGINE = create_engine(DATABASE_URL)