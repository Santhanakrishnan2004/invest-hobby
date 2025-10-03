import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# Supabase setup (store keys in Streamlit secrets)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("💰 Investment Tracker (Gold & Silver)")

# Investment type
investment_type = st.selectbox("Select Investment Type", ["Gold", "Silver"])

# Inputs
grams = st.number_input("Enter weight (grams)", min_value=0.01, format="%.2f")
price = st.number_input("Enter price (per gram or total)", min_value=0.0, format="%.2f")
date = st.date_input("Date of Purchase", datetime.today())

# Add entry button
if st.button("Add Entry"):
    data = {"type": investment_type, "grams": grams, "price": price, "date": str(date)}
    supabase.table("investments").insert(data).execute()
    st.success("Entry added successfully!")

# Fetch data
response = supabase.table("investments").select("*").execute()
records = response.data
df = pd.DataFrame(records)

# Show table
st.subheader("📊 Investment Records")
st.dataframe(df)

# Show totals
if not df.empty:
    total_gold = df[df["type"] == "Gold"]["grams"].sum()
    total_silver = df[df["type"] == "Silver"]["grams"].sum()
    total_cost = df["price"].sum()

    st.write(f"**Total Gold Purchased:** {total_gold:.2f} g")
    st.write(f"**Total Silver Purchased:** {total_silver:.2f} g")
    st.write(f"**Total Cost (₹):** {total_cost:.2f}")
