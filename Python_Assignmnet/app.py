from ast import Add

import streamlit as st
import pandas as pd
import plotly.express as px

# Create app.py (this is the Streamlit file separate from queries.py):

st.set_page_config(page_title="BrightMart Analytics", layout="wide")

@st.cache_data
def load_data():
    customers = pd.read_csv("customers.csv")
    orders = pd.read_csv("orders.csv")
    order_items = pd.read_csv("order_items.csv")
    products = pd.read_csv("products.csv")

    df = order_items.merge(orders, on="order_id", how="left")
    df = df.merge(customers, on="customer_id", how="left")
    df = df.merge(products, on="product_id", how="left")

    df["line_revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

    return df

df = load_data()
df_valid = df[df["order_status"] != "Cancelled"]

st.title("BrightMart Analytics Dashboard")


#-------------------------------------- Add sidebar filters---------------------------------------

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Region",
    options=df_valid["region"].unique(),
    default=df_valid["region"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    options=df_valid["category"].unique(),
    default=df_valid["category"].unique()
)

segment = st.sidebar.multiselect(
    "Segment",
    options=df_valid["segment"].unique(),
    default=df_valid["segment"].unique()
)

min_date = df_valid["order_date"].min()
max_date = df_valid["order_date"].max()
date_range = st.sidebar.date_input("Order date range", [min_date, max_date])

# Apply all filters together
mask = (
    df_valid["region"].isin(region) &
    df_valid["category"].isin(category) &
    df_valid["segment"].isin(segment) &
    (df_valid["order_date"] >= pd.to_datetime(date_range[0])) &
    (df_valid["order_date"] <= pd.to_datetime(date_range[1]))
)
filtered = df_valid[mask]


# -----------------------------------------Add the KPI row------------------------------------

st.divider()

# Custom CSS for card styling
st.markdown("""
<style>
.kpi-card {
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    color: white;
}
.kpi-label {
    font-size: 14px;
    opacity: 0.85;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

total_revenue = filtered['line_revenue'].sum()
total_orders = filtered['order_id'].nunique()
avg_order_value = filtered.groupby('order_id')['line_revenue'].sum().mean()
unique_customers = filtered['customer_id'].nunique()

kpis = [
    ("Total Revenue", f"₹{total_revenue:,.0f}", "#6C5CE7"),
    ("Total Orders", f"{total_orders}", "#00B894"),
    ("Avg Order Value", f"₹{avg_order_value:,.0f}", "#0984E3"),
    ("Unique Customers", f"{unique_customers}", "#E17055"),
]

col1, col2, col3, col4 = st.columns(4)
for col, (label, value, color) in zip([col1, col2, col3, col4], kpis):
    col.markdown(f"""
    <div class="kpi-card" style="background-color:{color};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------Add the tabs structure and charts------------------------------------

st.divider()

tab1, tab2 = st.tabs(["Overview", "Customer Deep-Dive"])

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        monthly = filtered.groupby("order_month")["line_revenue"].sum().reset_index()
        fig1 = px.line(monthly, x="order_month", y="line_revenue", title="Monthly Revenue Trend", markers=True, text="line_revenue")
        fig1.update_traces(texttemplate='₹%{text:,.0f}', textposition="top center")
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        cat_rev = filtered.groupby("category")["line_revenue"].sum().reset_index()
        fig2 = px.bar(cat_rev, x="category", y="line_revenue", title="Revenue by Category", text="line_revenue")
        fig2.update_traces(texttemplate='₹%{text:,.0f}', textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        top_customers = filtered.groupby("customer_name")["line_revenue"].sum().nlargest(10).reset_index()
        fig3 = px.bar(top_customers, x="line_revenue", y="customer_name", orientation="h", title="Top 10 Customers by Revenue", text="line_revenue")
        fig3.update_traces(texttemplate='₹%{text:,.0f}', textposition="outside")
        fig3.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        region_orders = filtered.groupby("region")["order_id"].nunique().reset_index()
        fig4 = px.pie(region_orders, names="region", values="order_id", title="Orders by Region")
        fig4.update_traces(textinfo="label+percent+value")
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Filtered Data")
    st.dataframe(filtered)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data as CSV", csv, "filtered_data.csv", "text/csv")


#----------------------------Add the Customer Deep-Dive tab------------------------------------


with tab2:
    st.subheader("Customer Deep-Dive")

    selected_customer = st.selectbox("Select a customer", sorted(filtered["customer_name"].unique()))
    cust_data = filtered[filtered["customer_name"] == selected_customer]

    d1, d2, d3 = st.columns(3)
    d1.metric("Lifetime Value", f"₹{cust_data['line_revenue'].sum():,.0f}")
    d2.metric("Total Orders", cust_data["order_id"].nunique())
    d3.metric("Total Items Bought", int(cust_data["quantity"].sum()))

    st.write(f"**Segment:** {cust_data['segment'].iloc[0]}  |  **City:** {cust_data['city'].iloc[0]}, {cust_data['state'].iloc[0]}")

    st.markdown("#### Order History")
    st.dataframe(
        cust_data[["order_id", "order_date", "product_name", "category", "quantity", "discount", "line_revenue"]]
        .sort_values("order_date", ascending=False)
    )