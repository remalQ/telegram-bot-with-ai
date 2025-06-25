import requests
import os
from dotenv import load_dotenv

load_dotenv()

ENV_PATH = ".env"
OAUTH_TOKEN = os.getenv("YC_OAUTH_TOKEN")


def update_iam_token():
    if not OAUTH_TOKEN:
        raise ValueError("Отсутствует YC_OAUTH_TOKEN в .env")

    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    response = requests.post(url, json={"yandexPassportOauthToken": OAUTH_TOKEN})

    if response.status_code != 200:
        raise Exception(f"Ошибка получения IAM токена: {response.text}")

    iam_token = response.json()["iamToken"]

    # Перезаписываем токен в .env
    lines = []
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("YC_IAM_TOKEN="):
                lines.append(f"YC_IAM_TOKEN={iam_token}\n")
            else:
                lines.append(line)

    if not any(line.startswith("YC_IAM_TOKEN=") for line in lines):
        lines.append(f"YC_IAM_TOKEN={iam_token}\n")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print("✅ IAM токен успешно обновлён.")
    return iam_token
