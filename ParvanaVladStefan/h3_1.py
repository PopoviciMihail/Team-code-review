"""
Exercise 1

Using pandas, determine the following for the sales.csv data:
The total revenue for each product (quantity  x price_per_unit).
The total cost for each product (quantity  x cost_per_unit).
The profit for each product (total revenue - total cost).
Finally, find the most profitable product overall.

"""

import pandas as pd

df = pd.read_csv("sales.csv")

print(df.head())

def calculate_revenue_for_product(dataframe):
    dataframe['total_revenue'] = dataframe['quantity'] * dataframe['price_per_unit']
    return dataframe

def calculate_cost_for_product(dataframe):
    dataframe['total_cost'] = dataframe['quantity'] * dataframe['cost_per_unit']
    return dataframe

def calculate_profit_for_product(dataframe):
    dataframe['profit'] = dataframe['total_revenue'] - dataframe['total_cost']
    return dataframe

def find_most_profitable_product(dataframe):
    return dataframe.loc[dataframe['profit'].idxmax()]

df = calculate_revenue_for_product(df)
df = calculate_cost_for_product(df)
df = calculate_profit_for_product(df)
most_profitable_product = find_most_profitable_product(df)
print("Most Profitable Product:")
print(most_profitable_product)
print(df)