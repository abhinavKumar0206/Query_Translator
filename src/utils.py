import logging
import re
import pandas as pd
from typing import Optional, Union, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from src.errors import QueryExecutionError

def setup_logging(log_level: str = "INFO") -> None:
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("query_translator.log"), logging.StreamHandler()]
    )

def log_query_error(error: Exception, query: str) -> Dict[str, str]:
    """Log errors with context and return user-friendly message"""
    logging.error(f"Query failed: {query}\nError: {str(error)}")
    return {
        'error': str(error),
        'suggestion': _get_suggestion(error)
    }

def _get_suggestion(error: Exception) -> str:
    if "no such column" in str(error):
        return "Try asking about existing columns like 'color' or 'price'"
    elif "syntax error" in str(error):
        return "Try simpler phrasing like 'Show me all t-shirts'"
    return "Please rephrase your question"

# Initialize logging when module is imported
setup_logging()

if __name__ == "__main__":
    from database_connector import DatabaseConnector
    db = DatabaseConnector()
    try:
        print("Test query:", db.execute_query("SELECT 1"))
    except Exception as e:
        print("Test failed:", str(e))