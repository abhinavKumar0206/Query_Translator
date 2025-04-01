from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os
from dotenv import load_dotenv
from src.errors import DatabaseConnectionError, QueryExecutionError

load_dotenv()

class DatabaseConnector:
    def __init__(self, db_url=None):
        self.db_url = db_url or os.getenv('DEFAULT_DB_URL')
        try:
            self.engine = create_engine(self.db_url)
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            raise DatabaseConnectionError(f"Connection failed: {str(e)}")
        
    def execute_query(self, query, params=None):
        try:
            with self.Session() as session:
                return pd.read_sql(query, session.bind, params=params)
        except Exception as e:
            raise QueryExecutionError(f"Query failed: {str(e)}", query)

    def get_schema(self):
        inspector = inspect(self.engine)
        return {
            table: [col['name'] for col in inspector.get_columns(table)]
            for table in inspector.get_table_names()
        }