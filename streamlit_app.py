import streamlit as st
import mysql.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

# See st.experimental_memo above? Without it, Streamlit would run the query every time the app reruns (e.g. on a widget interaction). With st.experimental_memo, it only runs when the query changes or after 10 minutes (that's what ttl is for).
#  Watch out: If your database updates more frequently, you should adapt ttl or remove caching so viewers always see the latest data.

rows = run_query("SELECT * from atp_megatable;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")



