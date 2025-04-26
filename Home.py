import streamlit as st
import Stock_Analysis
import price_prediction
import sentiment_analysis

st.set_page_config(page_title="Multi-Page App", page_icon="🌗", layout="wide")

if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

def toggle_theme():
    st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"

st.sidebar.button("🌗 Toggle Theme", on_click=toggle_theme)

dark_mode_css = """
<style>
    body {
        background-color: #121212;
        color: white;
    }
    .stApp {
        background-color: #121212;
        color: white;
    }
</style>
"""

light_mode_css = """
<style>
    body {
        background-color: white;
        color: black;
    }
    .stApp {
        background-color: white;
        color: black;
    }
</style>
"""

if st.session_state["theme"] == "dark":
    st.markdown(dark_mode_css, unsafe_allow_html=True)
else:
    st.markdown(light_mode_css, unsafe_allow_html=True)


page = st.sidebar.selectbox("Select a page", ["Home", "Stock Analysis","Price prediction","Sentiment Analysis",])
st.sidebar.slider("slider")


if page=="Stock Analysis":
    Stock_Analysis.Show_Analysis()
elif page=="Price prediction":
    price_prediction.show_prediction()
elif page=="Sentiment Analysis":
    sentiment_analysis.show_sentiment_analysis()
else:
    st.markdown(""" # *Stock Analysis and Prediction App* """)
    st.sidebar.title("About")
    st.sidebar.markdown("### ⚡ Built With:")
    st.sidebar.markdown("- **Python & Streamlit** for web development")
    st.sidebar.markdown("- **LSTM & BiLSTM** for stock analysis")
    st.sidebar.markdown("- **Matplotlib & Plotly** for interactive graphs")
    st.sidebar.markdown("- **News Sentiment Analysis** for understanding market trends")

    st.sidebar.markdown("📩 Have feedback? Reach out to us!")
    st.sidebar.markdown("Email ID : rajrahul32686@gmail.com")
    st.sidebar.markdown("Contact No. : 8690616629")
    st.sidebar.markdown("## **Social Media**")
    
    st.sidebar.markdown("[Instagram]()  \n"
    "  [Linkedin](www.linkedin.com/in/rahul-singh-rajpurohit-27bb3a289)")



    col1,col2,col3 = st.columns([1,1,1])
    with col1:
        st.image("image.jpg")
    with col2:
        st.image("image.jpg")
    with col3:
        st.image("image.jpg")


    st.markdown("""
    ### 📈 Welcome to the Stock Analysis and Prediction App!

    This platform provides advanced tools for **analyzing stock market data**, predicting future prices using Deep Learning models, and performing **sentiment analysis** based on market news. Whether you're an investor, trader, or enthusiast, this app helps you understand stock movements through interactive charts and prediction models.

    #### 🔍 Features of the App:

    - **📊 Stock Data Visualization**: 
        - **Closing Price vs Time Chart**
        - **Moving Averages Chart**
        - **Bollinger Bands**
        - **Relative Strength Index (RSI)**
        - **Volume Chart**
        - **Heat Map for Correlation Analysis**

    - **✅ Price Prediction with LSTM Models**:
        - **Single Feature LSTM**: Predict stock prices using only one feature (Closing Price).
        - **Multiple Feature LSTM**: Predict stock prices using various features (Open, High, Low, Close, Volume, 50sma, 200sma, 14rsi).

    - **📰 Sentiment Analysis**:
        - Predict stock sentiment using **BiLSTM** based on news articles and social media data, helping you understand market sentiment.

    #### How Does It Work?
    1. **Select a Stock**: Choose any stock symbol (e.g., AAPL, TSLA, etc.).
    2. **Visualize Data**: View charts and graphs that represent stock trends, volume, and key technical indicators.
    3. **Predict Price**: Get price predictions using the LSTM models.
    4. **Sentiment Analysis**: Understand the mood of the market through sentiment analysis using BiLSTM.

    #### Why Use This App?
    This app empowers you with the tools to analyze the stock market, forecast trends, and make informed investment decisions based on **data-driven insights**.

    ---
    """)
    st.markdown("""
    ### Ready to dive in? 

    Start analyzing stock data and make predictions using the tools available. Simply click on the options in the sidebar to begin your analysis!
    """)
