import pandas as pd

df = pd.read_csv("sales.csv")

df['revenue'] = df['quantity'] * df['price_per_unit']
df['cost'] = df['quantity'] * df['cost_per_unit']
df['profit_per_order'] = df['revenue'] - df['cost']

product_summary = df.groupby('product').agg(
    total_revenue=('revenue', 'sum'),
    total_cost=('cost', 'sum'),
).reset_index()

product_summary['total_profit'] = product_summary['total_revenue'] - product_summary['total_cost']

most_profitable_product_row = product_summary.loc[product_summary['total_profit'].idxmax()]
most_profitable_product = most_profitable_product_row['product']
max_profit = most_profitable_product_row['total_profit']

print("## Product Financial Summary")
print(product_summary.to_markdown(index=False, floatfmt=".2f"))

print("\n" + "="*40)
print(f"The most profitable product overall is: {most_profitable_product}")
print(f"Total Profit: ${max_profit:.2f}")
print("="*40)