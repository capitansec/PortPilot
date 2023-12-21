import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()  # .env dosyasını yükler


class DatabaseConnector:
    """
    This class is responsible for connecting to the database.
    """

    def __init__(self):
        """
        Initializes the DatabaseConnector object with connection parameters.
        """
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT"))
        self.driver = os.getenv("DB_DRIVER")
        self.name = os.getenv("DB_NAME")
        self.username = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD")

    def init_conn_str(self):
        """
        Initializes the database connection string.
        """
        return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"

    def connect(self):
        """
        Creates a network connection to the database.
        """
        return create_engine(self.init_conn_str())


db_connector = DatabaseConnector()
engine = db_connector.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Yields a database session for usage and ensures proper closure afterward.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
