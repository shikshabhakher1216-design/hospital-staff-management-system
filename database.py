from sqlalchemy import create_engine
# create_engine is responsible to create connection between python and database

from sqlalchemy.ext.declarative import declarative_base
# declarative_base helps create database tables using python classes instead od writing SQL manually

from sqlalchemy.orm import sessionmaker
# sessionmaker is used to create sessions that helps us talk to the database and perform CRUD operation

DATABASE_URL = "postgresql://postgres:<Your_Password>@localhost/hospital_db"
# it is a connection string used to connect Python with PostgreSQL database
# database type:// PostgreSQL username: password @ local machine / database name

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind = engine)

Base = declarative_base()

# create dependency_base()

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:
        db.close ()   