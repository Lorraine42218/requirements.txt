import os
import requests

# 1. 從環境變數讀取 Telegram 機密資訊
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 以桃園 (緯度 24.9937, 經度 121.301) 為例，可依需求調整 lat/lon
LATITUDE = 24.9937
LONGITUDE = 121.301

def get_max_pop():
    # 呼叫 Open-Meteo API 取得今日最高降雨機率 (precipitation_probability_max)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": "precipitation_probability_max",
        "timezone": "Asia/Taipei"
    }
    
    response = requests.get(url, params=params) # FIX: Pass the params to the request
    response.raise_for_status()
    data = response.json()
    
    # 取出今天的最高降雨機率 (%)
    today_max_pop = data["daily"]["precipitation_probability_max"][0]
    return today_max_pop

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("未設定 TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID 環境變數！")
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

def main():
    pop = get_max_pop()
    print(f"今日最高降雨機率為: {pop}%")
    
    if pop > 60:
        message = f"🌧️ 今天桃園最高降雨機率達 {pop}%，超過 60%，記得帶傘喔！"
    else:
        message = f"☀️ 今天桃園最高降雨機率為 {pop}%，未超過 60%，出門不用帶傘！"
    
    send_telegram_message(message)
    print("已成功發送 Telegram 通知！")

if __name__ == "__main__":
    main()
