from dotenv import load_dotenv
load_dotenv()  # load all the environment variables

import streamlit as st
import os
import mysql.connector
import google.generativeai as genai

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt.format(question)])
    return response.text

# Function To retrieve query from the database
def read_sql_query(sql):
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST").strip('"'),  # Remove any surrounding quotes
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    except mysql.connector.Error as e:
        st.error(f"Database error: {e}")
        return None

# Set the maximum number of results to return
top_k = 5

# Define few-shot samples
few_shots = [
    {'Question' : "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery' : "SELECT SUM(stock_quantity) FROM atliq_tshirts.t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "91"},
    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery': "SELECT SUM(price * stock_quantity) FROM atliq_tshirts.t_shirts WHERE size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': "22292"},
    {'Question': "If we have to sell all the Levi's T-shirts today with discounts applied. How much revenue our store will generate (post discounts)?" ,
     'SQLQuery' : """
     SELECT SUM(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue 
     FROM (SELECT SUM(price * stock_quantity) as total_amount, t_shirt_id 
           FROM atliq_tshirts.t_shirts 
           WHERE brand = 'Levi'
           GROUP BY t_shirt_id) a 
     LEFT JOIN atliq_tshirts.discounts ON a.t_shirt_id = discounts.t_shirt_id
     """,
     'SQLResult': "Result of the SQL query",
     'Answer': "16725.4"} ,
     {'Question' : "If we have to sell all the Levi's T-shirts today. How much revenue our store will generate without discount?" ,
      'SQLQuery': "SELECT SUM(price * stock_quantity) FROM atliq_tshirts.t_shirts WHERE brand = 'Levi'",
      'SQLResult': "Result of the SQL query",
      'Answer' : "17462"},
    {'Question': "How many white color Levi's shirts do I have?",
     'SQLQuery' : "SELECT SUM(stock_quantity) FROM atliq_tshirts.t_shirts WHERE brand = 'Levi' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "290"
     },
    {'Question': "How many t-shirts do we have in total?",
     'SQLQuery' : "SELECT COUNT(*) FROM atliq_tshirts.t_shirts",
     'SQLResult': "Result of the SQL query",
     'Answer' : "The total number of t-shirts"
    }
]

# Construct the prompt with few-shot samples
few_shot_samples = "\n\n".join([
    f"Question: {sample['Question']}\nSQLQuery: {sample['SQLQuery']}\nSQLResult: {sample['SQLResult']}\nAnswer: {sample['Answer']}"
    for sample in few_shots
])

prompt = f"""You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Always use 'atliq_tshirts.t_shirts' as the table name, not just 't_shirts' or 'atliq_tshirts'.
    For counting all rows, use 'SELECT COUNT(*) FROM atliq_tshirts.t_shirts' instead of using 'count' or 'as cnt'.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".
    
    Use the following format:
    
    Question: Question here
    SQLQuery: Query to run with no pre-amble
    SQLResult: Result of the SQLQuery
    Answer: Final answer here
    
    No pre-amble.

{few_shot_samples}

Question: {{}}
"""

# Streamlit App
st.set_page_config(page_title="AtliQ T-Shirts Inventory Query")
st.header("Query AtliQ T-Shirts Inventory")

# Display current environment variables (for debugging)
st.sidebar.subheader("Current Environment Variables")
st.sidebar.text(f"DB_HOST: {os.getenv('DB_HOST')}")
st.sidebar.text(f"DB_USER: {os.getenv('DB_USER')}")
st.sidebar.text(f"DB_NAME: {os.getenv('DB_NAME')}")

# Add input fields for database connection details
db_host = st.sidebar.text_input("DB Host", value=os.getenv("DB_HOST", ""))
db_user = st.sidebar.text_input("DB User", value=os.getenv("DB_USER", ""))
db_password = st.sidebar.text_input("DB Password", value=os.getenv("DB_PASSWORD", ""), type="password")
db_name = st.sidebar.text_input("DB Name", value=os.getenv("DB_NAME", ""))

# Update environment variables with user input
os.environ["DB_HOST"] = db_host
os.environ["DB_USER"] = db_user
os.environ["DB_PASSWORD"] = db_password
os.environ["DB_NAME"] = db_name

question = st.text_input("Input your question:", key="input")

submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    
    # Parse the response
    response_parts = response.split('\n')
    sql_query = ''
    sql_result = ''
    answer = ''
    
    for part in response_parts:
        if part.startswith('SQLQuery:'):
            sql_query = part.replace('SQLQuery:', '').strip()
        elif part.startswith('SQLResult:'):
            sql_result = part.replace('SQLResult:', '').strip()
    
    st.subheader("Generated SQL Query:")
    st.code(sql_query, language="sql")
    
    query_result = read_sql_query(sql_query)
    if query_result is not None:
        st.subheader("Query Result:")
        st.table(query_result)