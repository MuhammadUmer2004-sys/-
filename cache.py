import redis
from fastapi import FastAPI

app = FastAPI()
cache = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.get("/get-stock/{product_id}")
async def get_stock(product_id: int):
    stock = cache.get(f"stock:{product_id}")
    if stock:
        return {"product_id": product_id, "stock": int(stock)}
    else:
        stock = await fetch_from_db(product_id)  # Your function to fetch from DB
        cache.set(f"stock:{product_id}", stock)
        return {"product_id": product_id, "stock": stock}
