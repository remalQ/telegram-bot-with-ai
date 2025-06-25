# run.py
import threading
import asyncio
from fastapi import FastAPI
import uvicorn
from bot.main import run_bot

app = FastAPI()


@app.get("/")
def home():
    return {"status": "Bot is running"}


def run_web_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    # Запуск веб-сервера в отдельном потоке
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    # Запуск бота в основном потоке
    asyncio.run(run_bot())