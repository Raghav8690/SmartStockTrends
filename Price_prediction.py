import streamlit as st
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
 

def show_prediction():


    def set_model_choice(choice):
        st.session_state.selected_model = choice

    # Initialize session state
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None

    st.title("Stock Price Prediction")

    st.button("Using LSTM Model With One Feature (Closing Price)", on_click=set_model_choice, args=("one_feature",))
    st.button("Using LSTM Model With Multiple Features (Only for NHPC.NS)", on_click=set_model_choice, args=("multi_feature",))


    def predict_future_values(model1, recent_data, scaler, timesteps, num_predictions):
        predictions = []
        for _ in range(num_predictions):
            scaled_recent_data = scaler.fit_transform(recent_data)
            scaled_recent_data = scaled_recent_data.reshape((1, timesteps, 1))
            scaled_prediction = model1.predict(scaled_recent_data)
            prediction = scaler.inverse_transform(scaled_prediction)
            predictions.append(prediction[0][0])
            new_data_point = np.array([[prediction[0][0]]])
            recent_data = np.append(recent_data[1:], new_data_point, axis=0)
        return np.mean(predictions)
    

    if st.session_state.selected_model == "one_feature":
        user_input = st.text_input("Enter a stock ticker:", 'NHPC.NS')

        if user_input == 'SUZLON.NS':
            model = load_model('stock_price_lstm_model.keras')
        else:
            model = load_model('model4_lstm.keras')

        scaler = MinMaxScaler(feature_range=(0,1))

        def data_loading(ticker):
            end_date = datetime.today()
            start_date = '2010-10-01'

            d = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

            recent_d = d.tail(80)

            if not recent_d.empty:
                recent_d_value = np.array(recent_d['Close']).reshape(-1,1)
                predict = predict_future_values(model, recent_d_value, scaler, 80, 10)
                st.write(f'Tomorrow’s predicted price: {predict}')
            else:
                st.warning("Enter a valid stock ticker!")

        data_loading(user_input)

    elif st.session_state.selected_model == "multi_feature":

        user_input = st.text_input("Enter a stock ticker:", 'NHPC.NS')

        model1 = load_model('model1_multifeature_lstm.keras')
        scaler = MinMaxScaler(feature_range=(0,1))

        data = yf.download(user_input, start="2010-01-01", end=datetime.today(),auto_adjust=False)

        data['50sma'] = data['Close'].rolling(window=50).mean()
        data['200sma'] = data['Close'].rolling(window=200).mean()


        def calculate_rsi(data, window=14):
            delta = data.diff()
            gain = (delta.where(delta > 0, 0)).fillna(0)
            loss = (-delta.where(delta < 0, 0)).fillna(0)
            avg_gain = gain.rolling(window=window).mean()
            avg_loss = loss.rolling(window=window).mean()
            rs = avg_gain / avg_loss
            return 100 - (100 / (1 + rs))
        

        data['14rsi'] = calculate_rsi(data['Close'], window=14)

        recent_data = data.tail(80).reset_index()

        features = ['Open', 'High', 'Low', 'Close', 'Volume', '50sma', '200sma', '14rsi']

        scaled_data = scaler.fit_transform(recent_data[features])
        scaled_data = scaled_data.reshape(1,80,8)

        prediction1 = model1.predict(scaled_data)

        latest_features = scaled_data[-1, -1, :]

        p = prediction1[0][0]

        latest_features[3] = p

        latest_features_reshaped = latest_features.reshape(1, -1)

        predicted_features_unscaled = scaler.inverse_transform(latest_features_reshaped)

        predicted_close = predicted_features_unscaled[0, 3]

        st.write(f"Predicted closing price for tomorrow: {predicted_close}")

    else:
        st.write("Please select a model.")

        
