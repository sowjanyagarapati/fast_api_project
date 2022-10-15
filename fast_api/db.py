from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Crating Database Connection
sqlite_db_url = "sqlite:///./customers.db"
engine = create_engine(sqlite_db_url, connect_args={"check_same_thread": False})
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
