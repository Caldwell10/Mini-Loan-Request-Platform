from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgres+pysocopg2://postgres:postgres@localhost:5342/loans")

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

