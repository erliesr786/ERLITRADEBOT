import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import matplotlib.pyplot as plt  # <-- Add this import

print("[DEBUG] Starting script...")

# Load API key from .env
load_dotenv()
api_key = os.getenv("POLYGON_API_KEY")
if not api_key:
    raise ValueError("POLYGON_API_KEY not found in environment variables.")

symbol = "AAPL"
print(f"[DEBUG] Using symbol: {symbol}")

# Calculate date range for last 30 days (Polygon expects YYYY-MM-DD)
end_date = datetime.now()
start_date = end_date - timedelta(days=60)
start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")
print(f"[DEBUG] Date range: {start_str} to {end_str}")

# Polygon.io endpoint for daily bars
url = (
    f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/"
    f"{start_str}/{end_str}?adjusted=true&sort=asc&apiKey={api_key}"
)
print(f"[DEBUG] Requesting data from Polygon.io: {url}")

response = requests.get(url)
if response.status_code != 200:
    print(f"[ERROR] Failed to fetch data: {response.status_code} {response.text}")
    exit(1)

data = response.json()
if "results" not in data or not data["results"]:
    print("[ERROR] No historical data received from Polygon.io.")
    exit(1)

print(f"[DEBUG] Historical data received: {len(data['results'])} bars.")

# Convert to DataFrame
df = pd.DataFrame(data["results"])
df["date"] = pd.to_datetime(df["t"], unit="ms")
df = df.rename(columns={"c": "close"})
print("[DEBUG] Data converted to DataFrame.")

# Calculate 20-day moving average
df['20_MA'] = df['close'].rolling(window=20).mean()
print("[DEBUG] 20-day moving average calculated.")

# Calculate 20-day exponential moving average
df['20_EMA'] = df['close'].ewm(span=20, adjust=False).mean()
print("[DEBUG] 20-day exponential moving average calculated.")

print(df[['date', 'close', '20_MA', '20_EMA']])

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['close'], label='Close Price')
plt.plot(df['date'], df['20_MA'], label='20-Day MA', linestyle='--')
plt.plot(df['date'], df['20_EMA'], label='20-Day EMA', linestyle=':')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title(f'{symbol} Close Price, 20-Day MA, and 20-Day EMA')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()