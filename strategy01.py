from ib_insync import *
import pandas as pd

print("[DEBUG] Starting script...")

# Connect to IB Gateway or TWS
ib = IB()
print("[DEBUG] Connecting to IB Gateway/TWS...")
ib.connect('127.0.0.1', 7497, clientId=1)
print("[DEBUG] Connected.")

# Define the stock contract
contract = Stock('AAPL', 'SMART', 'USD')
print("[DEBUG] Contract defined.")

# Request 1 day bars for the last 30 days
print("[DEBUG] Requesting historical data...")
bars = ib.reqHistoricalData(
    contract,
    endDateTime='',
    durationStr='30 D',
    barSizeSetting='1 day',
    whatToShow='ADJUSTED_LAST',
    useRTH=True,
    formatDate=1
)
print(f"[DEBUG] Historical data received: {len(bars)} bars.")

# Convert to DataFrame
df = util.df(bars)
print("[DEBUG] Data converted to DataFrame.")

# Calculate 20-day moving average
df['20_MA'] = df['close'].rolling(window=20).mean()
print("[DEBUG] 20-day moving average calculated.")

print(df[['date', 'close', '20_MA']])

ib.disconnect()
print("[DEBUG] Disconnected from IB Gateway/TWS.")