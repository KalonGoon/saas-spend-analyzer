import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SaaS Spend Analyzer", layout="wide")
st.title("💸 SaaS Spend Analyzer")

uploaded_file = st.file_uploader("Upload your SaaS Spend CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Clean up
    df['Monthly Cost'] = pd.to_numeric(df['Monthly Cost'], errors='coerce')
    df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
    df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')

    st.subheader("📋 Raw Data")
    st.dataframe(df)

    # Monthly spend
    df['Month'] = df['Start Date'].dt.to_period('M').astype(str)
    monthly_spend = df.groupby('Month')['Monthly Cost'].sum().reset_index()

    st.subheader("📈 Monthly SaaS Spend")
    fig, ax = plt.subplots()
    ax.plot(monthly_spend['Month'], monthly_spend['Monthly Cost'], marker='o')
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Spend ($)")
    ax.set_title("Spend Over Time")
    st.pyplot(fig)

    # Top vendors
    top_vendors = df.groupby('Vendor')['Monthly Cost'].sum().sort_values(ascending=False).head(10)

    st.subheader("🏆 Top Vendors by Spend")
    st.bar_chart(top_vendors)

    # Underutilized tools (cost per user > $100)
    df['Cost Per User'] = df['Monthly Cost'] / df['User Count']
    underutilized = df[df['Cost Per User'] > 100]

    st.subheader("⚠️ Underutilized Tools ($100+/user)")
    st.dataframe(underutilized[['Vendor', 'Monthly Cost', 'User Count', 'Cost Per User']])
