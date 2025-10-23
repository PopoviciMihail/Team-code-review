"""
Exercise 1

Using pandas, determine the following for the sales.csv data:
The total revenue for each product (quantity  x price_per_unit).
The total cost for each product (quantity  x cost_per_unit).
The profit for each product (total revenue - total cost).
Finally, find the most profitable product overall

"""

import pandas as pd

df = pd.read_csv("sales.csv")

df["total_revenue"] = df["quantity"] * df["price_per_unit"]
df["total_cost"] = df["quantity"] * df["cost_per_unit"]
df["profit_per_product"] = df["total_revenue"] - df["total_cost"]

print(df["profit_per_product"])
most_profitable_row = df.sort_values(by="profit_per_product", ascending=False).iloc[0]
print(f"The most profitable single sale is: {most_profitable_row['product']}")

total_profit_by_product = df.groupby("product")["profit_per_product"].sum().sort_values(ascending=False)
print(total_profit_by_product)

most_profitable_product = total_profit_by_product.index[0]
print(f"The most profitable product overall is : {most_profitable_product}")
