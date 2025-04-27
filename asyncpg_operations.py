import asyncpg
import asyncio

# Asyncpg connection setup
async def get_db_connection():
    conn = await asyncpg.connect(user='your_user', password='your_password', database='your_db', host='localhost')
    return conn

# Async function to update stock
async def update_stock(product_id: int, quantity: int):
    conn = await get_db_connection()
    query = "UPDATE products SET stock = $1 WHERE id = $2"
    await conn.execute(query, quantity, product_id)
    await conn.close()

# Usage example
async def update_product_stock():
    await update_stock(1, 20)

# Run the async function
if __name__ == "__main__":
    asyncio.run(update_product_stock())
