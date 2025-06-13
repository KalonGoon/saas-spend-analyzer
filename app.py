import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SaaS Spend Analyzer", layout="wide")
st.title("💸 SaaS Spend Analyzer")

# --- Upload CSV ---
uploaded_file = st.file_uploader("Upload your SaaS Spend CSV", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # --- Schema Validation ---
        required_columns = {"Vendor", "Category", "Monthly Cost", "Start Date", "End Date", "User Count"}
        if not required_columns.issubset(df.columns):
            st.error(f"❌ Missing columns! Required: {', '.join(required_columns)}")
            st.stop()

        # --- Clean and Convert Types ---
        df['Monthly Cost'] = pd.to_numeric(df['Monthly Cost'], errors='coerce')
        df['User Count'] = pd.to_numeric(df['User Count'], errors='coerce')
        df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
        df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')
        df.dropna(subset=['Monthly Cost', 'User Count', 'Start Date'], inplace=True)

        # --- Summary Stats ---
        st.subheader("📊 Summary Stats")
        col1, col2 = st.columns(2)
        col1.metric("Total Vendors", df['Vendor'].nunique())
        col2.metric("Total Monthly Spend", f"${df['Monthly Cost'].sum():,.2f}")

        # --- Monthly Spend Trend ---
        df['Month'] = df['Start Date'].dt.to_period('M').astype(str)
        monthly_spend = df.groupby('Month')['Monthly Cost'].sum().reset_index()

        st.subheader("📈 Monthly SaaS Spend")
        fig1, ax1 = plt.subplots()
        ax1.plot(monthly_spend['Month'], monthly_spend['Monthly Cost'], marker='o')
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Total Spend ($)")
        ax1.set_title("Spend Over Time")
        ax1.tick_params(axis='x', rotation=45)
        st.pyplot(fig1)

        # --- Top Vendors by Spend ---
        top_vendors = df.groupby('Vendor')['Monthly Cost'].sum().sort_values(ascending=False).head(10)

        st.subheader("🏆 Top 10 Vendors by Spend (Sorted)")
        fig2, ax2 = plt.subplots()
        sorted_vendors = top_vendors.sort_values(ascending=True)
        ax2.barh(sorted_vendors.index, sorted_vendors.values)
        ax2.set_xlabel("Total Spend ($)")
        ax2.set_title("Top 10 Vendors by Total Monthly Spend")
        st.pyplot(fig2)

        # --- Underutilized Tools (Cost per User > $100) ---
        df['Cost Per User'] = (df['Monthly Cost'] / df['User Count']).round(2)
        underutilized = df[df['Cost Per User'] > 100]

        st.subheader("⚠️ Underutilized Tools ($100+ per user)")
        st.dataframe(underutilized[['Vendor', 'Monthly Cost', 'User Count', 'Cost Per User']])

        # --- Full Table Preview ---
        st.markdown("### 📋 Full Data Table")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("👆 Upload a SaaS spend CSV to begin.")
