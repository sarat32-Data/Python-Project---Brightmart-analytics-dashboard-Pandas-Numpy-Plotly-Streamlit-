# Python-Project---Brightmart-analytics-dashboard-Pandas-Numpy-Plotly-Streamlit-
Interactive multi-table e-commerce analytics dashboard built with Streamlit and Plotly. Joins 4 relational CSVs (customers, orders, order items, products) into a single dataset, with reactive filters, KPI cards, and revenue/customer visualizations — turning raw pandas analysis into a live, shareable web app.
# BrightMart Analytics Dashboard

An interactive multi-table analytics dashboard built with Streamlit and Plotly, analyzing e-commerce performance across customers, orders, products, and order line items for a fictional retail company, BrightMart.

🔗[Dashboard Preview](https://github.com/sarat32-Data/Python-Project---Brightmart-analytics-dashboard-Pandas-Numpy-Plotly-Streamlit-/blob/main/Dashboard_Preview.png)

## Overview

BrightMart's sales and operations team needed a way to explore performance without writing SQL queries every time. This project takes four raw CSV extracts, joins them into a single analysis-ready dataset, and presents it through a fully interactive, filterable dashboard.

## Tech Stack

- **Python** — data processing
- **Pandas** — multi-table joins, aggregation, datetime handling
- **Streamlit** — interactive web app framework
- **Plotly Express** — interactive charts (line, bar, pie)
- **HTML/CSS** (injected via `st.markdown`) — custom-styled KPI cards

## Data Model

Four related CSVs joined on shared keys into one master DataFrame:
customers.csv → orders.csv → order_items.csv ← products.csv

| File | Rows | Key Columns |
|---|---|---|
| customers.csv | 60 | customer_id |
| products.csv | 26 | product_id |
| orders.csv | 220 | order_id, customer_id |
| order_items.csv | 556 | order_item_id, order_id, product_id |

A calculated `line_revenue` column (`quantity × unit_price × (1 − discount)`) drives all revenue metrics. Cancelled orders are excluded from all financial KPIs but retained separately for auditing.

## Features

- **Sidebar filters** — Region, Category, Segment, and Order Date range, all fully reactive
- **KPI cards** — Total Revenue, Total Orders, Average Order Value, Unique Customers, styled with custom rounded CSS cards
- **4 interactive visualizations** — Monthly revenue trend, revenue by category, top 10 customers by revenue, order distribution by region — all with data labels
- **Filtered data table** with CSV export
- **Customer Deep-Dive tab** — select any customer to see their lifetime value, order count, and full order history

## Key Insights

Based on 206 valid orders (14 cancelled orders excluded) from 60 customers, totaling ₹27.8L in revenue:

- **Furniture is the top revenue category** at ₹12.9L — more than double the next category (Apparel, ₹5.8L), despite typically having fewer, higher-ticket transactions.
- **South is the highest-revenue region** (₹8.1L), narrowly ahead of North (₹7.9L), with West trailing at ₹5.7L.
- **December 2024 was the strongest month** (₹3.5L), roughly 3x a typical month — likely a seasonal/holiday effect — followed by a smaller spike in May 2025.
- **Home Office customers have the highest average order value** (₹14,899), ahead of Consumer (₹13,436) and Corporate (₹11,690) — despite Corporate often being assumed to spend more per transaction.

## Recommendations

- Prioritise Furniture and South-region inventory/marketing given their outsized revenue share.
- Investigate the December revenue spike to plan promotions or stock levels around that period annually.
- Target Home Office segment with premium/bundle offers, since they already convert to the highest order values — small AOV lifts here compound faster than in higher-volume, lower-value segments.

## Project Structure

brightmart-dashboard/
├── app.py # Streamlit dashboard
├── queries.py # Exploratory pandas analysis (joins, validation)
├── customers.csv
├── orders.csv
├── order_items.csv
├── products.csv
├── requirements.txt
└── README.md
