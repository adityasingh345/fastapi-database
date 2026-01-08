# this is going to have all of our connection strings for our application to be able to connect it to SQL

from sqlalchemy import create_engine
#this will be able to create the engine for our databse to communicate with our application
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'mysql+pymysql://root:123456788@localhost:3306/blog2'

# engine -> manages the connections, talk to database, Executes SQL under the hood ( a kind of bridge between python and mysql )
engine = create_engine(URL_DATABASE)

# fastapi handles many users-> each request needs its own DB session. 
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

# this is the parent class for all models.
Base = declarative_base()