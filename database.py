from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Connect to SQLite3
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# Connect to PostgresSQL
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/todosapp'

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:@localhost:3306/todosapp'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()