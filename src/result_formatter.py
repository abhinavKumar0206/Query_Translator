import pandas as pd
import numpy as np

class ResultFormatter:
    def generate_summary(self, results: pd.DataFrame, original_query: str) -> str:
        """
        Generate a natural language summary of query results
        
        :param results: DataFrame containing query results
        :param original_query: Original natural language query
        :return: Descriptive summary of results
        """
        if results.empty:
            return "No results found. The query might be too specific or there's no matching data."
        
        summary_strategies = [
            self._numeric_summary,
            self._categorical_summary,
            self._general_summary
        ]
        
        for strategy in summary_strategies:
            summary = strategy(results, original_query)
            if summary:
                return summary
        
        return "Results processed successfully."

    def _numeric_summary(self, results: pd.DataFrame, query: str) -> str:
        """
        Generate summary for numeric-heavy results
        """
        numeric_columns = results.select_dtypes(include=['int64', 'float64'])
        
        if len(numeric_columns.columns) > 0:
            for column in numeric_columns.columns:
                stats = {
                    'total': numeric_columns[column].sum(),
                    'mean': numeric_columns[column].mean(),
                    'max': numeric_columns[column].max(),
                    'min': numeric_columns[column].min()
                }
                
                summary_templates = [
                    f"The total {column} is {stats['total']:,.2f}.",
                    f"Average {column} is {stats['mean']:,.2f}.",
                    f"Ranges from {stats['min']:,.2f} to {stats['max']:,.2f}."
                ]
                
                return " ".join(summary_templates)
        
        return None

    def _categorical_summary(self, results: pd.DataFrame, query: str) -> str:
        """
        Generate summary for categorical results
        """
        categorical_columns = results.select_dtypes(include=['object'])
        
        if len(categorical_columns.columns) > 0:
            for column in categorical_columns.columns:
                value_counts = results[column].value_counts()
                top_categories = value_counts.head(3)
                
                summary_parts = [
                    f"Top categories in {column}:",
                    ", ".join([f"{cat} ({count} occurrences)" for cat, count in top_categories.items()])
                ]
                
                return " ".join(summary_parts)
        
        return None

    def _general_summary(self, results: pd.DataFrame, query: str) -> str:
        """
        Fallback general summary method
        """
        row_count = len(results)
        column_count = len(results.columns)
        
        return f"Query returned {row_count} rows across {column_count} columns."

# Example usage
def main():
    # Sample DataFrame for testing
    data = pd.DataFrame({
        'product': ['Vintage T-Shirt', 'Modern Logo', 'Classic Fit'],
        'sales': [1500, 1200, 900],
        'region': ['North', 'South', 'East']
    })
    
    formatter = ResultFormatter()
    summary = formatter.generate_summary(data, "Show t-shirt sales by region")
    print(summary)

if __name__ == "__main__":
    main()