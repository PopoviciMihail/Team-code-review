"""
Exercise 1:
Using pandas, determine the following for the sales.csv data:
- The total revenue for each product (quantity x price_per_unit)
- The total cost for each product (quantity x cost_per_unit)
- The profit for each product (total revenue - total cost)
- Finally, find the most profitable product overall
"""

import pandas as pd

df = pd.read_csv("sales.csv")

# Step 1: Calculate totals per row
df["total_revenue"] = df["quantity"] * df["price_per_unit"]
df["total_cost"] = df["quantity"] * df["cost_per_unit"]
df["profit"] = df["total_revenue"] - df["total_cost"]

# Step 2: Summarize by product
product_summary = (
    df.groupby("product")[["total_revenue", "total_cost", "profit"]]
    .sum()
    .reset_index()
)

# Step 3: Find the most profitable product
most_profitable = product_summary.sort_values(by="profit", ascending=False).head(1)

print("=== Product Profit Summary ===")
print(product_summary)

print("\n=== Most Profitable Product ===")
print(most_profitable)
