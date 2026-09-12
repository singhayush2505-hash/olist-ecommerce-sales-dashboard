import pandas as pd


customers = pd.read_csv("olist_customers_dataset.csv")
orders = pd.read_csv("olist_orders_dataset.csv")
order_items = pd.read_csv("olist_order_items_dataset.csv")
payments = pd.read_csv("olist_order_payments_dataset.csv")
reviews = pd.read_csv("olist_order_reviews_dataset.csv")
products = pd.read_csv("olist_products_dataset.csv")
sellers = pd.read_csv("olist_sellers_dataset.csv")
geolocation = pd.read_csv("olist_geolocation_dataset.csv")
category_translation = pd.read_csv("product_category_name_translation.csv")


print("CUSTOMERS:", customers.shape)
print("ORDERS:", orders.shape)
print("ORDER ITEMS:", order_items.shape)
print("PAYMENTS:", payments.shape)
print("REVIEWS:", reviews.shape)
print("PRODUCTS:", products.shape)
print("SELLERS:", sellers.shape)
print("GEOLOCATION:", geolocation.shape)
print("CATEGORY TRANSLATION:", category_translation.shape)



datasets = {
    "Customers": customers,
    "Orders": orders,
    "Order Items": order_items,
    "Payments": payments,
    "Reviews": reviews,
    "Products": products,
    "Sellers": sellers,
    "Geolocation": geolocation,
    "Category Translation": category_translation
}

print("\n========== MISSING VALUES ==========")

for name, df in datasets.items():
    print(f"\n--- {name} ---")
    missing = df.isnull().sum()
    print(missing[missing > 0])




print("\n========== DUPLICATE ROWS ==========")

for name, df in datasets.items():
    print(f"{name}: {df.duplicated().sum()}")


print("\n========== DATA TYPES ==========")

for name, df in datasets.items():
    print(f"\n--- {name} ---")
    print(df.dtypes)


# Convert order date columns to datetime

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    orders[col] = pd.to_datetime(orders[col])


print("\n========== ORDERS DATA TYPES AFTER CONVERSION ==========")
print(orders[date_columns].dtypes)

print(orders[date_columns].head())



orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.days



print(orders[
    [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "delivery_days"
    ]
].head(10))



orders["delivery_delay_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.days

print(orders[
    [
         "order_delivered_customer_date",
            "order_estimated_delivery_date",
            "delivery_delay_days"
    ]
].head(10))


def delivery_status(row):

    if pd.isna(row["order_delivered_customer_date"]):
        return "Not Delivered"

    elif row["delivery_delay_days"] < 0:
        return "Early"

    elif row["delivery_delay_days"] == 0:
        return "On Time"

    else:
        return "Late"


orders["delivery_status"] = orders.apply(delivery_status, axis=1)


print(
    orders[
        [
            "delivery_delay_days",
            "delivery_status"
        ]
    ].head(20)
)

print("\n========== DELIVERY PERFORMANCE ==========")
delivery_summary = orders["delivery_status"].value_counts()

print(delivery_summary)



delivery_percentage = (
    orders["delivery_status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(delivery_percentage)



average_delivery_days = orders["delivery_days"].mean()
print("Average Delivery Days :" , round(average_delivery_days,2))



total_product_sales = order_items["price"].sum()
total_freight = order_items["freight_value"].sum()

total_sales_value = total_product_sales + total_freight

print("Total Product Sales:", round(total_product_sales, 2))
print("Total Freight Value:", round(total_freight, 2))
print("Total Sales Value:", round(total_sales_value, 2))


print(orders["order_status"].value_counts())

sales_data = order_items.merge(
    orders[["order_id", "order_status"]],
    on="order_id",
    how="left"
)

print(sales_data.head())
print(sales_data.shape)
print(sales_data["order_status"].value_counts())


sales_by_status = (
    sales_data
    .groupby("order_status")["price"]
    .sum()
    .sort_values(ascending=False)
)

print(sales_by_status)