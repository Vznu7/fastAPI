from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine 

db_url = "postgresql://postgres:1008@localhost:5432/vishnu"
engine = create_engine(db_url)
session = sessionmaker(autocommit =False,autoflush=False,bind=engine)
