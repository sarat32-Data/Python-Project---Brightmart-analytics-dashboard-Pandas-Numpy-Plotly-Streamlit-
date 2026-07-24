import pandas as pd
import numpy as num

#------------------------PART A — DATA PREPARATION & JOINING  (15 marks)-------------------------------

#Load all datasets:
customers = pd.read_csv("customers.csv")
orders = pd.read_csv("orders.csv")
order_items = pd.read_csv("order_items.csv")
products = pd.read_csv("products.csv")

#Merge datasets:
df = order_items.merge(orders, on="order_id", how="left")
df = df.merge(customers, on="customer_id", how="left")
df = df.merge(products, on="product_id", how="left")

print(df.shape)
print(df.columns.tolist())
print(df.head())


# Revenue calculation:
df["line_revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])

# Fix date types
df["order_date"] = pd.to_datetime(df["order_date"])
df["signup_date"] = pd.to_datetime(df["signup_date"])

# Month column for trend analysis:
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

# Separate cancelled orders:
df_cancelled = df[df["order_status"] == "Cancelled"]
df_valid = df[df["order_status"] != "Cancelled"]

print(df.dtypes[["order_date", "signup_date", "line_revenue", "order_month"]])
print(df_valid[["order_date", "order_month", "line_revenue"]].head(10))