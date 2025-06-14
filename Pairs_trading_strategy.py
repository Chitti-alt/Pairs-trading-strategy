import pandas as pd

# Load your stock data
df = pd.read_csv("train_data.csv")  # Replace with your path

# Ensure Signal column is present
df['Signal'] = 0
current_position = 0  # 0 = neutral, 1 = long, -1 = short

# Compute 5-row rolling averages for Close and Volume
df['Avg_Close_5'] = df['Close'].ewm(3).mean()
df['Avg_Volume_5'] = df['Volume'].ewm(3).mean()

# Parameters (adjust to fit your needs)
VOLUME_MULTIPLIER = 1.22
PRICE_THRESHOLD1 = 0.025
PRICE_THRESHOLD2 = 0.022
BODY_STRENGTH_THRESHOLD= 0.6 # Ratio of body to range

for i in range(3, len(df)):
    row3=df.loc[i-3]
    row2=df.loc[i-2]
    row1=df.loc[i-1]# Start from 5 to ensure rolling average is valid
    row = df.loc[i]

    avg_close = row['Avg_Close_5']
    avg_volume = row['Avg_Volume_5']

    body = row['Close'] - row['Open']
    range_ = row['High'] - row['Low']
    if range_ == 0:
        continue  # skip bad data

    body_ratio = body / range_
    is_bullish_body = body_ratio > BODY_STRENGTH_THRESHOLD
    is_bearish_body = body_ratio < -BODY_STRENGTH_THRESHOLD

    signal = 0

    # Strong bullish case
    if row['Close'] > avg_close * (1 + PRICE_THRESHOLD1) and row['Volume'] > avg_volume * VOLUME_MULTIPLIER :
        if current_position == -1:
            signal = 2
            current_position = 1
        elif current_position == 0:
            signal = 1
            current_position = 1
    
        
    elif row['Close'] < avg_close * (1 - PRICE_THRESHOLD2) and row['Volume'] > avg_volume * VOLUME_MULTIPLIER :
        if current_position == 1:
            signal = -2
            current_position = -1
        elif current_position == 0:
            signal = -1
            current_position = -1
        
     # Strong bearish case
    elif row1['Low']>row['Close'] :
        if current_position == 1:
            signal = -2
            current_position = -1
        elif current_position == 0:
            signal = -1
            current_position = -1
    
    # Neutral case
    else:
        signal = 0

    df.loc[i, 'Signal'] = signal

# Save result
df.to_csv("trading_Signalv6.csv", index=False)

# Preview
print(df[['Close', 'High', 'Low', 'Open', 'Volume', 'Signal']].tail(10))