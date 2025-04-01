# src/errors.py
class DatabaseConnectionError(Exception):
    pass

class QueryExecutionError(Exception):
    def __init__(self, message, sql=None):
        self.message = message
        self.sql = sql
        super().__init__(f"{message}\nSQL: {sql[:200] if sql else 'None'}")

# Add these new classes
class SQLTranslationError(Exception):
    """Raised when natural language to SQL translation fails"""
    pass

class SQLValidationError(Exception):
    """Raised when generated SQL is invalid"""
    def __init__(self, message, sql=None):
        self.message = message
        self.sql = sql
        super().__init__(f"{message}\nSQL: {sql[:100] if sql else 'None'}")