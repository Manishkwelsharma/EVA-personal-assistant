import webbrowser
import requests
import openai
import datetime
import wikipedia
import random
import openai

class Websearch():
    # Function to search Google 
    def search_google(query):
        query = query.replace(' ', '+')
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

    # Define a function to play a song on YouTube
    def play_song(song_name):
        query = song_name.replace(' ', '+')
        url = f"https://www.youtube.com/results?search_query={query}"
        response = requests.get(url)
        search_results = response.text
        
        # Find the first video link from the search results
        video_link_start = search_results.find('/watch?v=')
        if video_link_start != -1:
            video_link_end = search_results.find('"', video_link_start)
            video_link = search_results[video_link_start:video_link_end]
            video_url = f"https://www.youtube.com{video_link}"
            webbrowser.open(video_url)

class API():

    # Define a function to generate a response using ChatGPT
    def generate_chatgpt_response(user_input):
        response = openai.Completion.create(
            engine='davinci',
            prompt=f'User: {user_input}\nChatbot:',
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.8,
        )
        return response.choices[0].text.strip()
    
    # function for getting news API
    def get_news(query):
        API_KEY = '7819c885b0ef4c659fb719c35170a211'  # Replace with your actual API key
        url = f"https://newsAPI.org/v2/everything?q={query}&APIKey={API_KEY}"
        response = requests.get(url)
        news_data = response.json()
        articles = news_data['articles']
        if len(articles) > 0:
            num_articles = min(3, len(articles))
            news_list = []
            for article in range(num_articles):
                article =  articles[article]
                title = article['title']
                description = article['description']
                source = article['source']['name']
                news_list.append({
                    'title': title,
                    'description': description,
                    'source': source
                })
                return news_list
        else:
            print("No news articles found.")

class Management():

    tasks = []

    def to_do_list():
        if Management.tasks:
            return "\n".join(Management.tasks)
        else:
            return "The to-do list is empty."

        # Function to extract and remove an item from the list
    def extract_item(words, idx):
        if idx < len(words):
            if words[idx] == "and":
                return Management.extract_item(words, idx + 1)
            return words[idx], words[:idx] + words[idx + 1:]
        return None, words
    
#Function fornumber to word
    def word_to_number(word):
        word = word.lower()
        numbers = {
            'one': 1,
            'first': 1,
            'two': 2,
            'second': 2,
            'three': 3,
            'third': 3,
            'four': 4,
            'fourth': 4,
            'five': 5,
            'fifth': 5,
            'six': 6,
            'sixth': 6,
            'seven': 7,
            'seventh': 7,
            'eight': 8,
            'eighth': 8,
            'nine': 9,
            'ninth': 9,
        }
        return numbers.get(word, -1)  # Return -1 if not found
    
    def add_task(user_input):
        task = user_input.replace("add", "").strip()
        if task:
            Management.tasks.extend(task)
            return f"Added '{task}' to the to-do list."
        else:
            Management.tasks.append(task)
            return f"'{task}' is already in the to-do list."
    
    def view_task(user_input):
        if len(Management.tasks) > 0:
            print("Bot: To-do list:")
            for idx, item in enumerate(Management.tasks, start=1):
                print(f"{idx}. {item}")
        else:
            print("Bot: The to-do list is empty.")

# Function to delete items from the list
    def delete_item(item):
        if item in Management.tasks:
            Management.tasks.remove(item)
            print(f"Deleted: {item}")
        else:
            print(f"{item} not found in the list.")

    def remove_task(user_input):
        words = user_input.replace("remove", "").strip().lower()
        if len(words) > 1:
            target = words[1].strip()
            target_num = Management.word_to_number(target)  # Convert word to number
            if target.isdigit():  # Check if the input is a number
                index = int(target) - 1
                if 0 <= index < len(Management.tasks):
                    Management.delete_item(Management.tasks[index])
                else:
                    print("Invalid item index.")
            elif target_num != -1:  # Check if the word represents a valid number
                if 1 <= target_num <= len(Management.tasks):
                    Management.delete_item(Management.tasks[target_num - 1])
                else:
                    print("Invalid position.")
            else:
                deleted = False
                for item in Management.tasks[:9]:
                    if target in item.lower():
                        Management.delete_item(item)
                        deleted = True
                        break
                if not deleted:
                    print(f"{target} not found in the list.")
        else:
            print("Invalid input for deletion.")
        
    

class Command():

    dialogues = {}

    def wishMe():
        hour=datetime.datetime.now().hour
        if hour>=0 and hour<12:
            return "Hello Sir, Good Morning"
        elif hour>=12 and hour<18:
            return "Hello Sir, Good Afternoon"
        else:
            return "Hello Sir, Good Evening"
    
    def timeMe():
        hour=datetime.datetime.now().hour
        if hour>=0 and hour<12:
            return "Good Morning"
        elif hour>=12 and hour<18:
            return "Good Afternoon"
        else:
            return "Good Evening"
        

    def get_wikipedia_info(query):
        try:
            results = wikipedia.summary(query, sentences=2)
            return "According to Wikipedia\n" + results
        except wikipedia.exceptions.PageError:
            return "Sorry, I couldn't find any information on that topic."
