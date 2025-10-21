from pandas import DataFrame, read_csv

def main():
    df :DataFrame = read_csv("sales.csv")

    df["total_revenue"] = df["quantity"] * df["price_per_unit"]
    df["total_cost"] = df["quantity"] * df["cost_per_unit"]
    df["profit"] = df["total_revenue"] - df["total_cost"]

    product_summary :DataFrame = (
        df.groupby("product")[["total_revenue", "total_cost", "profit"]]
        .sum()
        .reset_index()
    )

    most_profitable :DataFrame = product_summary.sort_values(by="profit", ascending=False).head(1)

    print("=== Product Profit Summary ===")
    print(product_summary)
    print("\n=== Most Profitable Product ===")
    print(most_profitable)

if __name__ == "__main__":
    main()