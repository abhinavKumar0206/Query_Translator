import streamlit as st
from src.database_connector import DatabaseConnector
from src.nlp_processor import NLPToSQLTranslator
from src.result_formatter import ResultFormatter
from src.errors import QueryExecutionError
from src.utils import log_query_error
import plotly.express as px
import pandas as pd

def init_session():
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'db' not in st.session_state:
        st.session_state.db = DatabaseConnector()
    if 'translator' not in st.session_state:
        st.session_state.translator = NLPToSQLTranslator(st.session_state.db)
    if 'formatter' not in st.session_state:
        st.session_state.formatter = ResultFormatter()

def show_sidebar():
    st.sidebar.title("Query History")
    for idx, item in enumerate(st.session_state.history[:10]):
        with st.sidebar.expander(f"Query {idx+1}: {item.get('query','')[:30]}..."):
            if 'error' in item:
                st.error("❌ Failed")
                st.code(item['error'])
            else:
                st.success("✅ Success")
                st.code(item.get('sql',''))

def main_interface():
    st.title("T-Shirt Sales Analytics")
    query = st.text_input("Ask about your t-shirt sales data:", placeholder="e.g. Show top selling products")
    
    if st.button("Run Query") or query:
        try:
            with st.spinner("Processing..."):
                sql = st.session_state.translator.translate_to_sql(query)
                results = st.session_state.db.execute_query(sql)
                
                st.session_state.history.insert(0, {
                    'query': query,
                    'sql': sql,
                    'results': results
                })
                
                st.subheader("Results")
                st.dataframe(results)
                
                if not results.empty:
                    create_visualization(results)
                
                st.info(st.session_state.formatter.generate_summary(results, query))
                
                with st.expander("View Generated SQL"):
                    st.code(sql)
                    
        except QueryExecutionError as e:
            error_info = log_query_error(e, e.sql)
            st.error("🚨 Query Failed")
            st.info(f"💡 Suggestion: {error_info['suggestion']}")
            st.session_state.history.insert(0, {
                'query': query,
                'error': error_info['error'],
                'sql': e.sql
            })
            
        except Exception as e:
            error_info = log_query_error(e, query)
            st.error(f"⚠️ Unexpected Error: {error_info['error']}")
            st.info(f"💡 Suggestion: {error_info['suggestion']}")

def create_visualization(df):
    if len(df.columns) >= 2:
        with st.expander("Visualize"):
            x_col = st.selectbox("X-axis", df.columns)
            y_col = st.selectbox("Y-axis", [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])])
            if y_col:
                fig = px.bar(df, x=x_col, y=y_col)
                st.plotly_chart(fig)

if __name__ == "__main__":
    init_session()
    show_sidebar()
    main_interface()