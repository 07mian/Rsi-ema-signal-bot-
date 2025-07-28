import numpy as np
import random

def generate_candle_data(length=100):
    base_price = 1.1200
    return base_price + np.cumsum(np.random.normal(0, 0.0008, length))

def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    gains = np.maximum(deltas, 0)
    losses = -np.minimum(deltas, 0)

    avg_gain = np.convolve(gains, np.ones(period), 'valid') / period
    avg_loss = np.convolve(losses, np.ones(period), 'valid') / period

    rs = avg_gain[-1] / avg_loss[-1] if avg_loss[-1] != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def calculate_ema(prices, period=20):
    weights = np.exp(np.linspace(-1., 0., period))
    weights /= weights.sum()
    ema = np.convolve(prices, weights, mode='valid')[-1]
    return round(ema, 5)

def get_signal(pair):
    prices = generate_candle_data(100)
    last_price = prices[-1]

    rsi = calculate_rsi(prices)
    ema = calculate_ema(prices)

    trend_up = last_price > ema
    trend_down = last_price < ema

    signal = f"⏳ No Clear Signal for {pair} (RSI: {rsi}, EMA: {ema})"

    if rsi > 67 and trend_down:
        signal = f"🔻 SELL Signal for {pair} (RSI: {rsi}, EMA: {ema})"
    elif rsi < 33 and trend_up:
        signal = f"🔺 BUY Signal for {pair} (RSI: {rsi}, EMA: {ema})"
    elif 64 < rsi <= 67 and trend_down:
        signal = f"⚠️ Weak SELL Signal for {pair} (RSI: {rsi}, EMA: {ema})"
    elif 33 < rsi < 36 and trend_up:
        signal = f"⚠️ Weak BUY Signal for {pair} (RSI: {rsi}, EMA: {ema})"

    return signal
