import streamlit as st # type: ignore
import yfinance as yf # type: ignore
import pandas as pd # type: ignore
import plotly.graph_objects as go # type: ignore
from datetime import datetime, timedelta 

# Set page configuration
st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

# Sidebar - Configuration & Stock Selection
st.sidebar.header("Settings")
available_stocks = (
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'LLY', 'V', 'TSM',
    'UNH', 'AVGO', 'NVO', 'JPM', 'WMT', 'XOM', 'MA', 'JNJ', 'PG', 'ORCL', 'HD',
    'ADBE', 'ASML', 'CVX', 'COST', 'TM', 'MRK', 'KO', 'ABBV', 'BAC', 'PEP', 'FMX',
    'CRM', 'SHEL', 'ACN', 'NFLX', 'MCD', 'AMD', 'LIN', 'NVS', 'AZN', 'CSCO', 'TMO',
    'DIS', 'PFE', 'INTC', 'SBUX', 'GS', 'GE', 'IBM', 'C', 'BA', 'HON', 'CAT'
)
selected_stocks = st.sidebar.multiselect("Select Stocks to Compare", available_stocks, default=['AAPL', 'MSFT', 'GOOGL']) 
period = st.sidebar.selectbox("Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "max"])
moving_avg_short = st.sidebar.number_input("Short Moving Average (days)", value=50, min_value=1, step=1)
moving_avg_long = st.sidebar.number_input("Long Moving Average (days)", value=100, min_value=1, step=1)

# Additional Technical Indicators Selection
st.sidebar.header("Additional Indicators")
show_rsi = st.sidebar.checkbox("Relative Strength Index (RSI)", value=True)
show_macd = st.sidebar.checkbox("Moving Average Convergence Divergence (MACD)", value=True)

# Tab Setup for Stock Analysis Sections
st.title("Stock Market Dashboard 📈")
tabs = st.tabs(["Stock Data", "Trend Analysis", "Volume Analysis", "Comparative Analysis"])

# Function to get and clean stock data
@st.cache_data
def get_stock_data(ticker, period):
    data = yf.Ticker(ticker).history(period=period)
    data.dropna(inplace=True)  # Data cleaning step
    return data[['Close', 'Volume']]

# Function to add technical indicators
def add_indicators(data):
    data['SMA_Short'] = data['Close'].rolling(window=moving_avg_short).mean()
    data['SMA_Long'] = data['Close'].rolling(window=moving_avg_long).mean()
    if show_rsi:
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
    if show_macd:
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = exp1 - exp2
        data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    return data 

# Function to plot stock price with indicators
def plot_stock_price(data, stock, key):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name="Close Price"))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_Short'], mode='lines', name=f"{moving_avg_short}-day SMA"))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_Long'], mode='lines', name=f"{moving_avg_long}-day SMA"))
    if show_rsi and 'RSI' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name="RSI"))
    fig.update_layout(title=f"{stock} Stock Price", xaxis_title="Date", yaxis_title="Price (USD)")
    st.plotly_chart(fig, key=key)

# Function to plot volume
def plot_volume(data, stock, key):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name="Volume"))
    fig.update_layout(title=f"{stock} Volume", xaxis_title="Date", yaxis_title="Volume")
    st.plotly_chart(fig, key=key)

# Display Stock Data Tab
with tabs[0]:
    st.header("Stock Data")
    for i, stock in enumerate(selected_stocks):
        st.subheader(f"{stock} Stock Data")
        data = get_stock_data(stock, period)
        data = add_indicators(data)
        
        # Display latest price and stock data
        st.metric("Latest Price", f"{data['Close'].iloc[-1]:.2f} USD")
        st.dataframe(data.tail())
        plot_stock_price(data, stock, key=f"stock_data_{i}")
 
# Display Trend Analysis Tab
with tabs[1]:
    st.header("Trend Analysis")
    for i, stock in enumerate(selected_stocks):
        data = get_stock_data(stock, period)
        data = add_indicators(data)
        st.subheader(f"{stock} Trend Analysis")
        plot_stock_price(data, stock, key=f"trend_analysis_{i}")

# Display Volume Analysis Tab
with tabs[2]:
    st.header("Volume Analysis")
    for i, stock in enumerate(selected_stocks):
        data = get_stock_data(stock, period)
        st.subheader(f"{stock} Volume Analysis")
        plot_volume(data, stock, key=f"volume_analysis_{i}")

# Display Comparative Analysis Tab
with tabs[3]:
    st.header("Comparative Analysis")
    fig = go.Figure()
    for i, stock in enumerate(selected_stocks):
        data = get_stock_data(stock, period)
        data = add_indicators(data)
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=stock))
    fig.update_layout(title="Comparative Stock Performance", xaxis_title="Date", yaxis_title="Price (USD)")
    st.plotly_chart(fig, key="comparative_analysis")

# Download Button for Combined Data
st.sidebar.header("Download Options")
combined_data = pd.concat([get_stock_data(stock, period).assign(Stock=stock) for stock in selected_stocks])
st.sidebar.download_button(label="Download Data as CSV", data=combined_data.to_csv().encode('utf-8'), file_name="stock_data.csv", mime='text/csv')
