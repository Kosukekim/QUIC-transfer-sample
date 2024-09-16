from fastapi import FastAPI,Query
import random
app = FastAPI()

@app.get("/")
async def show_random():
    value = random.random()
    print(value)
    return {"value":value}