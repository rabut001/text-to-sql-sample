import os
import pyodbc
import pandas as pd
import streamlit as st
import requests

# Function to get the schema
@st.cache_data
def get_schema():
    connection = None
    try:
        print("Connecting to the database...")
        connection = pyodbc.connect(os.getenv("CONNECTION_STRING"))
        cursor = connection.cursor()

        # Execute a query to get the schema
        print("Executing schema query...")
        query = """
        SELECT TABLE_SCHEMA as [Schema Name], TABLE_NAME as [Table Name], COLUMN_NAME as [Column Name], DATA_TYPE as [Data Type] 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_CATALOG = 'AdventureWorks'
        ORDER BY TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME
        """
        cursor.execute(query)
        schema_info = cursor.fetchall()
        print("Schema query executed successfully!")

        # Create a DataFrame to display the schema
        schema_info_columns = [col[0] for col in cursor.description]
        schema_df = pd.DataFrame.from_records(schema_info, columns=schema_info_columns)
        print("Schema DataFrame created successfully!")
        return schema_df

    except Exception as error:
        print(f"Error retrieving schema: {error}")
        st.error(f"Error retrieving schema: {error}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Database connection closed.")

def format_schema(schema_df):
    schema_str = ""
    for index, row in schema_df.iterrows():
        schema_str += f"Schema: {row['Schema Name']}, Table: {row['Table Name']}, Column: {row['Column Name']}, Type: {row['Data Type']}\n"
    return schema_str

def generate_sql(schema_str, instruction):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Your task is to generate SQL based on provided database schema and the instruction.
    The database engine is SQL Server.

    Only generate the SQL itself, no any markdown like "```sql" or "```" or other formatting.

    here is the database schema:
    {schema_str}

    here is the instruction:
    {instruction}
    """

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 300
    }

    print("Sending request to LLM...")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print("Received response from LLM.")
    except Exception as e:
        print(f"Error in LLM request: {e}")
        return "", ""

    sql_query = response.json()["choices"][0]["message"]["content"]
    print(sql_query)

    explanation_prompt = f"""
    Explain this SQL very concisely (less than 30 words):
    {sql_query}
    """
    try:
        data["messages"] = [
            {"role": "user", "content": explanation_prompt}
        ]
        explanation_completion = requests.post(url, headers=headers, json=data)
        explanation_completion.raise_for_status()
        explanation = explanation_completion.json()["choices"][0]["message"]["content"]
        print(explanation)
    except Exception as e:
        explanation = f"Error generating explanation: {e}"

    return sql_query, explanation

def execute_sql(sql_query):
    try:
        print("Executing SQL query...")
        connection = pyodbc.connect(os.getenv("CONNECTION_STRING"))
        cursor = connection.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()

        result_columns = [col[0] for col in cursor.description]
        result_df = pd.DataFrame.from_records(result, columns=result_columns)
        print("SQL query executed successfully!")
        return result_df
    except Exception as error:
        st.error(f"Error executing SQL: {error}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Database connection closed.")

def main():
    st.title("Database Query Generator")
    instruction = st.text_area("Instruction:", height=50)
    sql_explanation = ""

    # Get the schema once and cache it
    schema_df = get_schema()
    if schema_df is not None:
        schema_str = format_schema(schema_df)

    if st.button("Query"):
        print("Query button clicked.")
        if schema_df is not None and instruction:
            generated_sql, sql_explanation = generate_sql(schema_str, instruction)
            if generated_sql:
                st.session_state.generated_sql = generated_sql
                st.session_state.sql_explanation = sql_explanation
                result_df = execute_sql(generated_sql)
                st.write(result_df)
            else:
                print("Failed to generate SQL.")

    if 'generated_sql' in st.session_state and st.session_state.generated_sql:
        st.info("✨Generated SQL Explanation✨：\n\n" + st.session_state.get('sql_explanation', sql_explanation))
        modified_sql = st.text_area("Modify SQL", value=st.session_state.generated_sql, height=200, key="modified_sql")
        if st.button("Query Again"):
            print("Query Again button clicked.")
            # Update the session state with the modified SQL right before executing it
            st.session_state.generated_sql = st.session_state.modified_sql
            result_df = execute_sql(st.session_state.modified_sql)
            st.write(result_df)

    if schema_df is not None:
        st.title("Database Schema")
        st.write(schema_df)

if __name__ == "__main__":
    main()
