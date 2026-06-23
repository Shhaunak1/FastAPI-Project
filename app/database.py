from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>:<port>/<database_name>"
# database connection URL string
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# defining engine that actually connects to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL) 
#If woking exclusively with sql-lite database, add this parameter to the create_engine method: connect_args={'check_same_thread':False}

# defining session to talk to the database 
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# defining base class which will be inherited in the python code to create objects using python model
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        