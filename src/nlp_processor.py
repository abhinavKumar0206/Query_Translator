from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.llms import Ollama
import re
import os
from src.errors import SQLTranslationError, SQLValidationError
from dotenv import load_dotenv

load_dotenv()

class NLPToSQLTranslator:
    def __init__(self, database_connector):
        self.db = SQLDatabase.from_uri(database_connector.db_url)
        self.llm = Ollama(model="sqlcoder", temperature=0)
        self.chain = create_sql_query_chain(self.llm, self.db)

    def translate_to_sql(self, natural_query: str) -> str:
        try:
            sql = self.chain.invoke({"question": natural_query})
            return self._validate_sql(sql)
        except Exception as e:
            raise SQLTranslationError(f"Translation failed: {str(e)}")

    def _validate_sql(self, sql: str) -> str:
        sql = re.sub(r'--.*?\n', '', sql)
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
        sql = sql.strip()
        
        if not re.match(r'^\s*SELECT\s', sql, re.IGNORECASE):
            raise SQLValidationError(f"Only SELECT queries allowed. Query start: {sql[:100]}...")
            
        forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", ";--"]
        if any(cmd in sql.upper() for cmd in forbidden):
            raise SQLValidationError(f"Query contains forbidden operations: {sql[:100]}...")
            
        return sql

# class SQLTranslationError(Exception):
#     pass

# class SQLValidationError(Exception):
#     pass