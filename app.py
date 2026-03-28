import streamlit as st
import sqlite3
import pandas as pd

# ------------------ CONFIG ------------------
st.set_page_config(page_title="PhonePe Dashboard", layout="wide")

# ------------------ DB CONNECTION ------------------
conn = sqlite3.connect("phonepe.db", check_same_thread=False)

def run_query(query):
    return pd.read_sql(query, conn)

# ------------------ TITLE ------------------
st.title("📊 PhonePe Transaction Insights Dashboard")

# ------------------ SIDEBAR FILTER ------------------
year_list = run_query("SELECT DISTINCT Year FROM aggregated_transaction ORDER BY Year")["Year"].tolist()
year = st.sidebar.selectbox("Select Year", ["All"] + year_list)

st.write("Selected Year:", year)

# ------------------ KPI SECTION ------------------
st.subheader("🔑 Key Metrics")

col1, col2 = st.columns(2)

if year == "All":
    total_txn_query = "SELECT SUM(Amount) as total FROM aggregated_transaction"
    total_user_query = "SELECT SUM(RegisteredUsers) as users FROM aggregated_user"
else:
    total_txn_query = f"SELECT SUM(Amount) as total FROM aggregated_transaction WHERE Year = {year}"
    total_user_query = f"SELECT SUM(RegisteredUsers) as users FROM aggregated_user WHERE Year = {year}"

total_txn = run_query(total_txn_query)["total"][0]
total_users = run_query(total_user_query)["users"][0]

col1.metric("Total Transaction Amount", f"{round(total_txn/1e12,2)} Trillion")
col2.metric("Total Users", f"{int(total_users/1e6)} Million")

# ------------------ CATEGORY ANALYSIS ------------------
st.subheader("📊 Transaction by Category")

if year == "All":
    query = """
    SELECT Category, SUM(Amount) as Total
    FROM aggregated_transaction
    GROUP BY Category
    """
else:
    query = f"""
    SELECT Category, SUM(Amount) as Total
    FROM aggregated_transaction
    WHERE Year = {year}
    GROUP BY Category
    """

df_cat = run_query(query)
st.bar_chart(df_cat.set_index("Category"))

# ------------------ TREND ------------------
st.subheader("📈 Transaction Trend")

if year == "All":
    query = """
    SELECT Year, SUM(Amount) as Total
    FROM aggregated_transaction
    GROUP BY Year
    ORDER BY Year
    """
    df_trend = run_query(query)
    st.line_chart(df_trend.set_index("Year"))
else:
    query = f"""
    SELECT Quarter, SUM(Amount) as Total
    FROM aggregated_transaction
    WHERE Year = {year}
    GROUP BY Quarter
    ORDER BY Quarter
    """
    df_trend = run_query(query)
    st.line_chart(df_trend.set_index("Quarter"))

# ------------------ TOP STATES ------------------
st.subheader("🌍 Top States by Transaction")

if year == "All":
    query = """
    SELECT Name, SUM(Amount) as Total
    FROM top_transaction
    WHERE Type='State'
    GROUP BY Name
    ORDER BY Total DESC
    LIMIT 10
    """
else:
    query = f"""
    SELECT Name, SUM(Amount) as Total
    FROM top_transaction
    WHERE Type='State' AND Year = {year}
    GROUP BY Name
    ORDER BY Total DESC
    LIMIT 10
    """

df_state = run_query(query)
st.bar_chart(df_state.set_index("Name"))

# ------------------ USER GROWTH ------------------
st.subheader("👥 User Growth")

if year == "All":
    query = """
    SELECT Year, SUM(RegisteredUsers) as Users
    FROM aggregated_user
    GROUP BY Year
    ORDER BY Year
    """
    df_user = run_query(query)
    st.line_chart(df_user.set_index("Year"))
else:
    query = f"""
    SELECT Quarter, SUM(RegisteredUsers) as Users
    FROM aggregated_user
    WHERE Year = {year}
    GROUP BY Quarter
    ORDER BY Quarter
    """
    df_user = run_query(query)
    st.line_chart(df_user.set_index("Quarter"))

# ------------------ MAP DATA ------------------
st.subheader("📍 State-wise Transactions")

if year == "All":
    query = """
    SELECT State, SUM(Amount) as Total
    FROM map_transaction
    GROUP BY State
    ORDER BY Total DESC
    LIMIT 10
    """
else:
    query = f"""
    SELECT State, SUM(Amount) as Total
    FROM map_transaction
    WHERE Year = {year}
    GROUP BY State
    ORDER BY Total DESC
    LIMIT 10
    """

df_map = run_query(query)
st.bar_chart(df_map.set_index("State"))

# ------------------ CLOSE CONNECTION ------------------
conn.close()