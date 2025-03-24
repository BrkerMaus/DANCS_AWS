import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os
from models.product import get_products

IMAGE_DIR = "static/images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def clean_old_images():
    for file in os.listdir(IMAGE_DIR):
        file_path = os.path.join(IMAGE_DIR, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def generate_charts():
    products = get_products()
    custom_colors = ["#28a745", "#ffc107", "#dc3545"]

    stock_counts = {"Available": 0, "Low Stock": 0, "Out of Stock": 0}
    item_names = []
    item_prices = []
    item_quantities = []

    for product in products:
        stock_counts[product["status"]] += 1
        item_names.append(product["name"])
        item_prices.append(product["price"])
        item_quantities.append(product["quantity"])

    if os.listdir(IMAGE_DIR):  
        clean_old_images()

    plt.figure(figsize=(6, 6))
    plt.pie(
    stock_counts.values(), 
    labels=stock_counts.keys(), 
    autopct='%1.1f%%', 
    colors=custom_colors
    )
    plt.title("Stock Overview")
    plt.savefig(os.path.join(IMAGE_DIR, "stock_pie_chart.png"))
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.bar(item_names, item_prices, color="blue")
    plt.xlabel("Items")
    plt.ylabel("Price ($)")
    plt.title("Price Comparison")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, "price_bar_chart.png"))
    plt.close()
    
    plt.figure(figsize=(8, 5))
    plt.plot(item_names, item_quantities, marker="o", linestyle="-", color="purple")
    plt.xlabel("Items")
    plt.ylabel("Quantity")
    plt.title("Quantity Trends")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, "quantity_line_chart.png"))
    plt.close()
