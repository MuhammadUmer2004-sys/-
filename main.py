import aio_pika
import asyncio
from fastapi import FastAPI, BackgroundTasks, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_session  # SQLAlchemy session management
from asyncpg_operations import update_stock  # Import asyncpg functions (stock update)
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from prometheus_fastapi_instrumentator import Instrumentator
from models import Product  # Assuming you have a Product model for your DB

# Create FastAPI app instance
app = FastAPI()

# Initialize Prometheus instrumentation
instrumentator = Instrumentator()

# Apply Prometheus instrumentation
instrumentator.instrument(app).expose(app, "/metrics")

# Initialize FastAPI Limiter
FastAPILimiter.init(app)

# Connect to RabbitMQ
async def get_rabbitmq_connection():
    return await aio_pika.connect_robust("amqp://guest:guest@localhost/")

# Function to publish a message to the queue (RabbitMQ)
async def publish_message(message: str):
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()  # Create a new channel
    queue = await channel.declare_queue('stock_updates', durable=True)
    await channel.default_exchange.publish(
        aio_pika.Message(body=message.encode()),
        routing_key=queue.name,
    )
    await connection.close()

# Endpoint to update stock and trigger background task
@app.post("/update-stock/")
async def update_stock(product_id: int, quantity: int, background_tasks: BackgroundTasks):
    # Publish stock update message to RabbitMQ in the background
    message = f"Product {product_id} stock updated to {quantity}"
    background_tasks.add_task(publish_message, message)
    
    # Asynchronously update stock in the database
    await update_stock(product_id, quantity)
    
    return {"message": "Stock update is processing."}

# Endpoint for getting products (read from replica)
@app.get("/products/")
def get_products(db: Session = Depends(lambda: get_session(is_read=True))):
    # Perform a read operation using SQLAlchemy (replica)
    products = db.execute(select(Product)).scalars().all()
    return products

# Endpoint for adding a new product (write to master)
@app.post("/add-product/")
def add_product(product_data: dict, db: Session = Depends(lambda: get_session(is_read=False))):
    # Perform a write operation using SQLAlchemy (master)
    new_product = Product(**product_data)
    db.add(new_product)
    db.commit()  # Commit the transaction to the database
    return {"message": "Product added successfully"}

# Rate-limited endpoint example
@app.get("/some-data/")
async def get_data(response: Response, rate_limit: str = Depends(RateLimiter(times=5, seconds=60))):
    return {"message": "Data response"}

# Root endpoint (just for testing)
@app.get("/")
async def root():
    return {"message": "Hello, World!"}