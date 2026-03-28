import streamlit as st
import sqlite3
import pandas as pd

# Connect DB
conn = sqlite3.connect("phonepe.db")

st.set_page_config(page_title="PhonePe Dashboard", layout="wide")

st.title("📊 PhonePe Transaction Insights Dashboard")

# Sidebar Filters
year = st.sidebar.selectbox("Select Year", ["All"] + list(range(2018, 2025)))

# ---------- QUERY FUNCTION ----------
def run_query(query):
    return pd.read_sql(query, conn)

# ---------- KPI SECTION ----------
st.subheader("🔑 Key Metrics")

col1, col2 = st.columns(2)

total_txn = run_query("SELECT SUM(Amount) as total FROM aggregated_transaction")["total"][0]
total_users = run_query("SELECT SUM(RegisteredUsers) as users FROM aggregated_user")["users"][0]

col1.metric("Total Transaction Amount", f"{round(total_txn/1e12,2)} Trillion")
col2.metric("Total Users", f"{int(total_users/1e6)} Million")

# ---------- CATEGORY ANALYSIS ----------
st.subheader("📊 Transaction by Category")

query = "SELECT Category, SUM(Amount) as Total FROM aggregated_transaction GROUP BY Category"
df_cat = run_query(query)

st.bar_chart(df_cat.set_index("Category"))

# ---------- YEARLY TREND ----------
st.subheader("📈 Year-wise Transaction Trend")

query = """
SELECT Year, SUM(Amount) as Total
FROM aggregated_transaction
GROUP BY Year
ORDER BY Year
"""
df_year = run_query(query)

st.line_chart(df_year.set_index("Year"))

# ---------- TOP STATES ----------
st.subheader("🌍 Top States by Transaction")

query = """
SELECT Name, SUM(Amount) as Total
FROM top_transaction
WHERE Type='State'
GROUP BY Name
ORDER BY Total DESC
LIMIT 10
"""
df_state = run_query(query)

st.bar_chart(df_state.set_index("Name"))

# ---------- USER GROWTH ----------
st.subheader("👥 User Growth")

query = """
SELECT Year, SUM(RegisteredUsers) as Users
FROM aggregated_user
GROUP BY Year
"""
df_user = run_query(query)

st.line_chart(df_user.set_index("Year"))

# ---------- MAP DATA ----------
st.subheader("📍 State-wise Transactions")

query = """
SELECT State, SUM(Amount) as Total
FROM map_transaction
GROUP BY State
ORDER BY Total DESC
LIMIT 10
"""
df_map = run_query(query)

st.bar_chart(df_map.set_index("State"))

conn.close()