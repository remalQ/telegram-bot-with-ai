from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    return {"status": "Bot is running"}