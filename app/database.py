from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQL_ALCHEMY_DATABASE_URL = (
    f"{settings.database_protocol}://{settings.database_username}:"
    f"{settings.database_password}@{settings.database_host}:"
    f"{settings.database_port}/{settings.database_host.split('.')[0]}.{settings.database_name}?sslmode={settings.database_connection_parameter}"
)
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
sessionlocal=sessionmaker(autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
