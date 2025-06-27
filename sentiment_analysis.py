import streamlit as st
import numpy as np
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

import nltk
from nltk.corpus import stopwords,wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer as wnl
import pickle


stop_word = set(stopwords.words('english'))
lemmatizer = wnl()

with open("tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)

model = load_model("Sentiment_analysis2.keras")


def preprocess_text(text):
    text = re.sub(r"[^a-zA-Z\s]", "", text.lower()) 
    words = word_tokenize(text) 
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_word] 
    return " ".join(words)


def predict_sentiment(text):
    text = preprocess_text(text)
    sequence = tokenizer.texts_to_sequences([text])  
    padded_sequence = pad_sequences(sequence, maxlen=80, padding="post")  
    prediction = model.predict(padded_sequence)
    sentiment = np.argmax(prediction) 
    labels = ["Positive", "Negative", "Neutral"]
    return labels[sentiment]


def show_sentiment_analysis():
    st.image("image3.png")
    
    news = st.text_input("Enter news related to any stock:")  

    if news: 
        sentiment = predict_sentiment(news)
        st.success(f"📢 This is **{sentiment}** news!") 
    else:
        st.warning("⚠️ Please enter some news!")


