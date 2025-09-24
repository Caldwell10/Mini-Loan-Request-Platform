from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# database connection URL
database_url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/loans'

# create the SQLAlchemy engine object
engine = create_engine(database_url)

#create a configured Session object
Sessionmaker = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Define base for models
Base = declarative_base()

# Get DB session
def get_db():
    db = Sessionmaker()
    try:
        yield db
    finally:
        db.close()

