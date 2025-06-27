import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime


def Show_Analysis():
    st.image("image1.png")

    st.title("Stock Data Visualization")


    user_input = st.text_input("Enter a stock ticker:", 'AAPL')
    df = yf.download(user_input, start='2010-01-01', end= datetime.today().date(),auto_adjust=False)
    df.reset_index(inplace=True)  


    st.subheader(f'Data from 2010 to {datetime.today().date().year}')
    st.write(df.describe())

    st.markdown("""---""")


    today_date = datetime.today().date()
    start_date = st.date_input("Start Date", today_date, min_value=pd.to_datetime("2010-01-01"))
    end_date = st.date_input("End Date", today_date, max_value=today_date)


    filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]



    st.subheader('Closing Price vs Time Chart')
    fig = plt.figure(figsize=(12, 5))
    plt.plot(filtered_df['Date'], filtered_df['Close'], linestyle='-', color='b')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title('Closing Price vs Time')
    plt.grid(True)
    st.pyplot(fig)

    st.markdown("""---""")

    st.subheader('Stock Price with Moving Averages')
    if (end_date-start_date).days > 500: 
        sma50 = filtered_df['Close'].rolling(50).mean()
        sma200 = filtered_df['Close'].rolling(200).mean()
        fig1 = plt.figure(figsize=(12,5))
        plt.plot(filtered_df['Close'], label='Close Price')
        plt.plot(sma50, label='50-Day SMA', linestyle='dashed')
        plt.plot(sma200, label='200-Day SMA', linestyle='dotted')
        plt.xlabel('Date') 
        plt.ylabel('Price')
        plt.legend()
        plt.title('Stock Price with Moving Averages')
        st.pyplot(fig1)
    else:
        st.warning("Not enough data to calculate moving averages !!")



    window = 20
    ma20 = filtered_df['Close'].rolling(window).mean()
    Upper = ma20 + 2 * filtered_df['Close'].rolling(window).std()
    Lower = ma20 - 2 * filtered_df['Close'].rolling(window).std()

    Upper = Upper.squeeze().to_numpy().flatten()  # Ensure 1D
    Lower = Lower.squeeze().to_numpy().flatten()
    st.markdown("""---""")

    st.subheader('Bollinger Bands')

    fig2 = plt.figure(figsize=(12,5))
    plt.plot(filtered_df['Date'], filtered_df['Close'], label='Close Price')
    plt.plot(filtered_df['Date'], ma20, label='20-Day MA')
    plt.fill_between(filtered_df['Date'], Upper, Lower, color='gray', alpha=0.3, label='Bollinger Bands')
    plt.legend()
    plt.title('Bollinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Price')
    st.pyplot(fig2)


    window_length = 14
    delta = filtered_df['Close'].diff(1)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    gain = gain.squeeze()  # Ensures it's 1D
    loss = loss.squeeze()  # Ensures it's 1D
    avg_gain = pd.Series(gain).rolling(window=window_length).mean()
    avg_loss = pd.Series(loss).rolling(window=window_length).mean()


    RS = avg_gain / avg_loss
    RSI = 100 - (100 / (1 + RS))

    st.markdown("""---""")


    st.subheader('Relative Strength Index')

    fig3 = plt.figure(figsize=(12,5))
    plt.plot(filtered_df['Date'], RSI, label="RSI", color="purple")
    plt.axhline(70, color='red', linestyle='dashed', label="Overbought (70)")
    plt.axhline(30, color='green', linestyle='dashed', label="Oversold (30)")
    plt.legend()
    plt.title("Relative Strength Index (RSI)")
    plt.xlabel('Date')
    plt.ylabel('RSI')
    st.pyplot(fig3)

    st.markdown("""---""")

    st.subheader('Volume Chart')

    fig4 = plt.figure(figsize=(12,5))
    plt.bar(filtered_df['Date'], filtered_df['Volume'].squeeze(), color='blue', alpha=0.5)
    plt.title('Stock Trading Volume')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    st.pyplot(fig4)


    st.markdown("""---""")

    st.subheader("Stock Correlation Heatmap")
    count = st.number_input("Enter number of Stocks you want to anlyze for")
    ticker = []
    for i in range(int(count)):
        stock = st.text_input(f"Enter Stock {i+1} Ticker (e.g., AAPL, MSFT):")
        if stock:
            ticker.append(stock)


    if len(ticker) >1:
        data= yf.download(ticker,period="6mo",auto_adjust=False)['Close']
        corr = data.corr()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(corr, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
        st.pyplot(fig)
    elif len(ticker) == 1:
        st.warning("Please enter at least 2 stock tickers to calculate correlation.")
    else:
        st.info("Waiting for user input...")




