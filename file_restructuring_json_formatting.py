import json
import csv

# Read JSON file
with open("sales.json", "r") as file:
    data = json.load(file)

records = []

# Process each order
for order in data.get("orders", []):

    order_id = order.get("order_id", "Unknown")
    customer_name = order.get("customer", {}).get("name", "Unknown")
    shipping_address = order.get("shipping_address", "Unknown")

    # Extract country/state code
    country_code = shipping_address.split(",")[-1].strip()

    items = order.get("items", [])

    # Calculate total order value
    order_total = 0
    total_quantity = 0

    for item in items:
        price = item.get("price", 0)
        quantity = item.get("quantity", 0)

        order_total += price * quantity
        total_quantity += quantity

    # Apply discount
    discount = 0
    if order_total > 100:
        discount = order_total * 0.10

    # Shipping cost
    shipping_cost = total_quantity * 5

    # Final total
    final_total = order_total - discount + shipping_cost

    # Create record for each item
    for item in items:

        product_name = item.get("name", "Unknown")
        price = item.get("price", 0)
        quantity = item.get("quantity", 0)

        total_value = price * quantity

        records.append([
            order_id,
            customer_name,
            product_name,
            price,
            quantity,
            total_value,
            discount,
            shipping_cost,
            final_total,
            shipping_address,
            country_code
        ])

# Sort records by Final Total
records.sort(key=lambda x: x[8], reverse=True)

# Write to CSV file
with open("output.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Order ID",
        "Customer Name",
        "Product Name",
        "Product Price",
        "Quantity Purchased",
        "Total Value",
        "Discount",
        "Shipping Cost",
        "Final Total",
        "Shipping Address",
        "Country Code"
    ])

    writer.writerows(records)

print("CSV file generated successfully: output.csv")

