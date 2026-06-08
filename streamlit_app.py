import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ----------------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------------

st.set_page_config(
    page_title="Sellers Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sellers Performance Dashboard")

# ----------------------------------------------------------
# LOAD DATA SAFELY
# ----------------------------------------------------------

FILE_NAME = "sellers.xlsx"

try:

    # Check if file exists
    if not Path(FILE_NAME).exists():
        st.error(f"File not found: {FILE_NAME}")
        st.stop()

    # Read Excel file
    df = pd.read_excel(FILE_NAME)

    # Debug information
    with st.expander("Debug Information"):
        st.write("File loaded successfully")
        st.write(f"Rows: {len(df)}")
        st.write(f"Columns: {list(df.columns)}")

except Exception as e:
    st.error("Error reading Excel file")
    st.exception(e)
    st.stop()

# ----------------------------------------------------------
# VERIFY REQUIRED COLUMNS
# ----------------------------------------------------------

required_columns = [
    "REGION",
    "ID",
    "NAME",
    "LASTNAME",
    "INCOME",
    "SOLD UNITS",
    "TOTAL SALES",
    "SALES AVERAGE"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

# ----------------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------------

st.sidebar.header("Filters")

regions = ["All"] + sorted(df["REGION"].dropna().unique().tolist())

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)

# Filter data
if selected_region == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["REGION"] == selected_region].copy()

# ----------------------------------------------------------
# METRICS
# ----------------------------------------------------------

st.subheader("General Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Units Sold",
        f"{filtered_df['SOLD UNITS'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Total Sales",
        f"${filtered_df['TOTAL SALES'].sum():,.2f}"
    )

with col3:
    st.metric(
        "Average Sales",
        f"${filtered_df['SALES AVERAGE'].mean():,.2f}"
    )

# ----------------------------------------------------------
# DATA TABLE
# ----------------------------------------------------------

with st.container():

    st.subheader("Seller Data")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

# ----------------------------------------------------------
# CHARTS
# ----------------------------------------------------------

st.subheader("Performance Charts")

# Chart 1
fig_units = px.bar(
    filtered_df,
    x="NAME",
    y="SOLD UNITS",
    color="REGION",
    title="Units Sold by Seller"
)

st.plotly_chart(
    fig_units,
    use_container_width=True
)

# Chart 2
fig_sales = px.bar(
    filtered_df,
    x="NAME",
    y="TOTAL SALES",
    color="REGION",
    title="Total Sales by Seller"
)

st.plotly_chart(
    fig_sales,
    use_container_width=True
)

# Chart 3
fig_avg = px.line(
    filtered_df,
    x="NAME",
    y="SALES AVERAGE",
    markers=True,
    title="Average Sales by Seller"
)

st.plotly_chart(
    fig_avg,
    use_container_width=True
)

# ----------------------------------------------------------
# SELLER DETAILS
# ----------------------------------------------------------

st.subheader("Individual Seller Information")

filtered_df["FULL NAME"] = (
    filtered_df["NAME"].astype(str)
    + " "
    + filtered_df["LASTNAME"].astype(str)
)

seller_list = sorted(filtered_df["FULL NAME"].unique())

selected_seller = st.selectbox(
    "Select Seller",
    seller_list
)

if st.button("Show Seller Details"):

    seller_data = filtered_df[
        filtered_df["FULL NAME"] == selected_seller
    ].iloc[0]

    c1, c2 = st.columns(2)

    with c1:
        st.info("Personal Information")
        st.write("ID:", seller_data["ID"])
        st.write("Name:", seller_data["FULL NAME"])
        st.write("Region:", seller_data["REGION"])

    with c2:
        st.info("Sales Information")
        st.write("Income:", seller_data["INCOME"])
        st.write("Units Sold:", seller_data["SOLD UNITS"])
        st.write("Total Sales:", seller_data["TOTAL SALES"])
        st.write("Average Sales:", seller_data["SALES AVERAGE"])

# ----------------------------------------------------------
# DOWNLOAD FILTERED DATA
# ----------------------------------------------------------

st.subheader("Download Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered CSV",
    data=csv,
    file_name="filtered_sellers.csv",
    mime="text/csv"
)

# ----------------------------------------------------------
# FOOTER
# ----------------------------------------------------------

st.success("Dashboard loaded successfully.")