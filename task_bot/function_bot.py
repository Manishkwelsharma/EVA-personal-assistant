import os
import pickle
import nltk
import joblib
import pandas as pd
from nltk.tokenize import word_tokenize
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

# Define the configuration data
config = {
    "music_model_path": "C:\Users\manis\Downloads\Eva-main\task_bot\file\music_recommend_tfidf_vectorizer.pkl",
    "music_tfidf_vectorizer_path": "C:\Users\manis\Downloads\Eva-main\task_bot\file\music_recommendation_model.pkl",
    "model_path": "C:\Users\manis\Downloads\Eva-main\task_bot\file\eva_born_model.pkl",
    "tfidf_vectorizer_path": "C:\Users\manis\Downloads\Eva-main\task_bot\file\tfidf_vectorizer.pkl",
    "nltk_data_path": "tokenizers",
    "music_data_path": "C:\Users\manis\Downloads\Eva-main\task_bot\file\music_recommendation_dataset.csv",
}


# music files path
music_model = pickle.load(config["music_model_path"])
music_tfidf_vectorizer = joblib.load(config["music_tfidf_vectorizer_path"])

# model file path
model = pickle.load(config["model_path"])
tfidf_vectorizer = joblib.load(config["tfidf_vectorizer_path"])

nltk_data_path = config["nltk_data_path"]
nltk.data.path.append(nltk_data_path)

class functions():

    math_keywords = {
        'addition': {'plus', 'add', '+', 'sum'},
        'subtract': {'minus', 'subtract', '-', 'difference'},
        'multiply': {'times', 'multiply', '*', 'product'},
        'divide': {'divide', '/', 'over'}
    }

    def process_math_question(user_input):
        tokens = word_tokenize(user_input.lower())
        math_action = None
        operand1 = None
        operand2 = None

        for token in tokens:
            for operation, keywords in functions.math_keywords.items():
                if token in keywords:
                    math_action = operation
                    break
            try:
                token_value = float(token)
                if operand1 is None:
                    operand1 = token_value
                else:
                    operand2 = token_value
            except ValueError:
                pass

        return math_action, operand1, operand2

    # arithmetic.py
    def perform_addition(a, b):
        return a + b

    def perform_subtraction(a, b):
        return a - b

    def perform_multiplication(a, b):
        return a * b

    def perform_division(a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b
    
class music_recommender:
        # Spotify API integration
    data = pd.read_csv('music_recommender.csv')

    client_id = '4afb3295ce3b4efbb48a2862ad03a9d4'
    client_secret = '58c8a37749154466bcd2eb9116fe78cd'
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    # Function to recommend music based on user input
    def recommend_music(cls, user_input, music_tfidf_vectorizer, music_model):
        # Predict genre using the trained model
        input_message_tfidf = music_tfidf_vectorizer.transform([user_input])
        predicted_genre = music_model.predict(input_message_tfidf)[0]

        # Get Spotify recommendations based on predicted genre
        genre_mapping = {code: genre for code, genre in enumerate(cls.data['Genre'].unique())}
        predicted_genre_name = genre_mapping[predicted_genre]
        results = cls.sp.search(q=f"genre:{predicted_genre_name}", type='track', limit=10)

        recommendations = []
        for track in results['tracks']['items']:
            recommendations.append({
                'Track': track['name'],
                'Artist': track['artists'][0]['name']
            })
        
        return recommendations