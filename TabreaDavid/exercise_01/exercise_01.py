import pandas as pd
"""
Exercise 1

Using pandas, determine the following for the sales.csv data:
The total revenue for each product (quantity  x price_per_unit).
The total cost for each product (quantity  x cost_per_unit).
The profit for each product (total revenue - total cost).
Finally, find the most profitable product overall.
"""


def exercise_01(process_file: str):
    df = pd.read_csv(process_file, on_bad_lines="skip")
    df["revenue"] = df["quantity"] * df["price_per_unit"]
    df["cost"] = df["quantity"] * df["cost_per_unit"]

    summary = df.groupby("product")[["revenue", "cost"]].sum()
    summary["profit"] = summary["revenue"] - summary["cost"]

    most_profitable = summary["profit"].idxmax()
    print(summary)
    print(f"Most profitable product overall: {most_profitable} (profit={summary.loc[most_profitable, 'profit']})")

    return summary, most_profitable

if __name__ == "__main__":
    exercise_01("sales.csv")