# yagpt_include.py

import os
import asyncio
import aiohttp
from dotenv import load_dotenv
import json
from bot.iam_token_updater import update_iam_token


async def periodic_iam_update(interval_hours=10):
    while True:
        try:
            update_iam_token()
        except Exception as e:
            print(f"Ошибка при обновлении IAM токена: {e}")
        await asyncio.sleep(interval_hours * 3600)

load_dotenv()

YC_IAM_TOKEN = os.getenv("YC_IAM_TOKEN")  # IAM-токен (альтернатива API-ключу)
YC_FOLDER_ID = os.getenv("YC_FOLDER_ID")
YC_MODEL = "general"  # Базовая модель YandexGPT


async def ask_yagpt(question: str, retries=3) -> str:
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Bearer {YC_IAM_TOKEN}",
        "x-folder-id": YC_FOLDER_ID,
        "Content-Type": "application/json"
    }
    data = {
        "modelUri": f"gpt://{YC_FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "temperature": 0.7,
            "maxTokens": "1000"
        },
        "messages": [
            {
                "role": "user",
                "text": question
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        for attempt in range(retries):
            try:
                async with session.post(url, headers=headers, json=data) as resp:
                    if resp.status == 200:
                        response = await resp.json()
                        return response['result']['alternatives'][0]['message']['text']
                    elif resp.status == 429:
                        wait_time = 2 ** attempt
                        await asyncio.sleep(wait_time)
                    else:
                        error = await resp.text()
                        return f"Ошибка YandexGPT (HTTP {resp.status}): {error}"
            except Exception as e:
                return f"Ошибка соединения: {str(e)}"

    return "Слишком много запросов. Попробуйте позже."
