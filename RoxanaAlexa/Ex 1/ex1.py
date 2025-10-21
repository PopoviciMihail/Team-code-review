import pandas as pd

df = pd.read_csv("sales.csv")

df["total_revenue"] = df["quantity"] * df["price_per_unit"]
df["total_cost"] = df["quantity"] * df["cost_per_unit"]
df["profit_per_product"] = df["total_revenue"] - df["total_cost"]

print(df["profit_per_product"])
most_profitable_row = df.sort_values(by="profit_per_product", ascending=False).iloc[0]
print(f"Cel mai profitabil produs este: {most_profitable_row['product']}")

total_profit_by_product = df.groupby("product")["profit_per_product"].sum().sort_values(ascending=False)
print(total_profit_by_product)

most_profitable_product = total_profit_by_product.index[0]
print(f"Cel mai profibail produs dintre toate este: {most_profitable_product}")
