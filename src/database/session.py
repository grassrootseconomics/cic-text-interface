# external imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# local import
from src.config import config
from src.database import data_source_name_from_config

DATABASE_URI = data_source_name_from_config(config)


engine = create_engine(DATABASE_URI, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
