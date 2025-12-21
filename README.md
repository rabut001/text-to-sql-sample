# README
This is a Streamlit text-to-SQL application. It takes natural language input, retrieves the database schema, and generates SQL based on the schema and instructions. The app can execute the SQL and provide a natural language explanation of the generated SQL. Users can recognize discrepancies between their intent and the generated SQL, modify the SQL, and re-execute it.

This code was forked from https://github.com/arvehisa/text-to-sql-bedrock.git .

The main differences from the original are as follows.

- Adding a Docker environment to execute the code.
- Adding sample data to execute the code.
- Changing the database from PostgreSQL to SQL Server to use the sample database AdventureWorks.
- Changing the LLM platform from Amazon Bedrock to OpenAI.

## Prerequisites

- A Docker environment
- An OpenAI API key

## Setup

Set your OpenAI API key in the file .env:
```
OPENAI_API_KEY=add-your-api-key-here
```

## Running the Application

To start the Streamlit application, run `streamlit run text-to-sql-bedrock.py`
