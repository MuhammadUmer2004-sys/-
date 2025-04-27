# from celery import Celery
# from time import sleep

# # Setup Celery instance
# app = Celery('tasks', broker='amqp://guest:guest@localhost//')

# @app.task
# def update_inventory(product_id, quantity):
#     # Simulating a long-running task (e.g., updating stock in the database)
#     sleep(10)
#     print(f'Inventory for product {product_id} updated to {quantity}')
#     return f'Updated product {product_id} with quantity {quantity}'

from celery import Celery
import os
from time import sleep

# Create a Celery app instance
app = Celery('tasks', broker=os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/"))

# Task to update inventory
@app.task
def update_inventory(product_id: int, quantity: int):
    # Logic to update inventory in the database
    print(f"Updating product {product_id} with quantity {quantity}")
    # Add your database update logic here
    # Example: update_stock_db(product_id, quantity)
    return f"Product {product_id} updated with quantity {quantity}"

# Task to process order
@app.task
def process_order(order_id: int):
    # Simulate order processing logic
    print(f"Processing order {order_id}...")
    sleep(5)  # Simulating order processing time
    print(f"Order {order_id} processed successfully.")
    return f"Order {order_id} completed successfully"
