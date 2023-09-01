import openai
import random
import autocorrect_py as autocorrect
from task_bot.task_bot import Websearch, API, Management, Command
from task_bot.function_bot import functions, music_recommender
import speech_recognition as sr
import pyttsx3
import datetime
from task_bot.model import predict_intent
from aiml.aiml_bot import initialize_aiml_bot, chat_with_aiml

# Set up your OpenAI API credentials
openai.api_key = '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'

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# Set up a flag to indicate whether speech recognition is active
speech_recognition_active = False

voices = engine.getProperty('voices')
eva_voice = None

# Find the eva voice
for voice in voices:
    if voice.name == 'Microsoft Zira Desktop - English (United States)':
        eva_voice = voice
        break

# Set the voice of the engine to eva
if eva_voice is not None:
    engine.setProperty('voice', eva_voice.id)

# Define the chatbot's responses
GREETINGS = ["Hello! Sir", "How may I help you Sir?", "Hi Sir, welcome back!", "Hello Sir, I was waiting for you to join!"]
question = ["Hi there! As an AI language model, I don't have the ability to do things like humans do. However, I'm always here and ready to chat with you and assist you in any way I can. Is there something specific you would like to talk about or ask me?", "I'm a AI assiatance that will help you in doing tasks"]
GOODBYES = ["Goodbye!", "See you later!", "Farewell!"]
HELP_RESPONSE = "You can ask me to add tasks, list tasks, remove tasks, search on Google, or get news."
features = ['Creating to-do-list', 'Search on google', 'playing songs', 'Get news']
intro = ['hi', 'hey', 'hello', "hhat up"]
info = ['information', 'info', 'tell', 'what is']
exit_keywords = ["exit", "quit", "goodbye", "bye", "sleep", "end", "close", "stop", "finish", "terminate"]
exit_responses = [
    "Goodbye!",
    "See you later!",
    "Farewell!",
    "If you have any more questions in the future, don't hesitate to return. Goodbye!",
    "Until next time!",
    "Take care!",
    "Have a great day!",
    "Thanks for chatting with me. Goodbye!",
    "It's been a pleasure assisting you. Goodbye!",
    "Remember, I'm just a message away if you need help later. Goodbye!",]

# Define the speak function
def speak(text):
    print("EVA:", text)
    engine.say(text)
    engine.runAndWait()


# Define a function to generate a response from the chatbot
def generate_response(user_input):

    user_input = autocorrect(user_input)
    # Command to generate a response
    user_input = user_input.lower()
    intent = predict_intent(user_input)

    # first interaction with bot
    if any(word in user_input for word in intro):
        return speak(random.choice(GREETINGS))
    
    # answer for whatever
    elif 'what' in user_input:
        return speak(random.choice(question))
    
# greeting
    elif "good morning" in user_input:
        current_hour = datetime.datetime.now().hour
        if current_hour < 12:
            return speak("Good Morning")
        else:
            return speak("Sorry, it's not morning anymore\n" + Command.wishMe())

    elif "good afternoon" in user_input:
        current_hour = datetime.datetime.now().hour
        if 12 <= current_hour < 18:
            return speak("Good Afternoon")
        else:
            return speak("Sorry, it's not afternoon anymore\n" + Command.wishMe())

    elif "good evening" in user_input:
        current_hour = datetime.datetime.now().hour
        if current_hour >= 18:
            return speak("Good Evening")
        else:
            return speak("Sorry, it's not evening yet\n" + Command.wishMe())


# info about time
    elif "time" in user_input:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return speak(f"The current time is {current_time}...\n{Command.timeMe()} Sir")

# searching for info
    elif any(word in user_input.lower() for word in info):
        query = intent.replace("info", "").strip()
        if query:
            response = Command.get_wikipedia_info(query)
            speak("Searching Wikipedia for information...")
            speak(response)
            return response
        else:
            return speak("Please provide a query for information.")
        
# listing bot features
    elif "feature" in user_input or "features" in user_input:
        features_list = '\n'.join([f"{i+1}. {feature}" for i, feature in enumerate(features)])
        return f"The available features are:\n{features_list}", speak(f"The available features are:\n{features_list}")
    
# get out from bot saying goodbye
    elif "goodbye" in user_input or "bye" in user_input:
        return random.choice(GOODBYES), speak(f"Goodbye")
    
    # help area
    elif "help" in user_input:
        return HELP_RESPONSE, speak(HELP_RESPONSE)
    
    elif intent == "add":
        return speak(Management.add_task(user_input))
    elif intent == "view":
        return speak(Management.view_task())
    elif intent == "list":
        return speak(Management.to_do_list())
    elif intent == "remove":
        return speak(Management.remove_task(user_input))

# search in google
    elif intent == "search":
        query = user_input.replace("search", "").strip()
        if query:
            Websearch.search_google(query)
            return f"Searching Google for '{query}'...", speak(f"Searching Google for '{query}'...")
        else:
            return "Please provide a query to search on Google.", speak("Please provide a query to search on Google.")

    elif intent == "news":
        query = user_input.replace("news", "").strip()
        if query:
            news_articles = API.get_news(query)
            if news_articles:
                response = "Here are some news articles:\n\n"
                for article in news_articles:
                    response += f"Title: {article['title']}\nDescription: {article['description']}\nSource: {article['source']}\n\n"
                speak(response)
            else:
                response = "No news articles found."
                speak(response)
            return response
        else:
            return "Please provide a query to get news."
        
    elif intent == "play":
        song_name = user_input.replace("play", "").strip()
        if song_name:
            Websearch.play_song(song_name)
            return f"Playing '{song_name}' on YouTube...", speak(f"Playing '{song_name}' on YouTube...")
        else:
            return "Please provide the name of the song to play.", speak("Please provide the name of the song to play.")
    
    elif intent == "recommend":
        recommendations = music_recommender(user_input)
        response = "Here are some recommended songs:\n"
        for idx, track in enumerate(recommendations, start=1):
            response += f"{idx}. {track['Track']} by {track['Artist']}\n"
        return response

    # maths operations
    math_action, operand1, operand2 = functions.process_math_question(user_input)

    if math_action and operand1 is not None and operand2 is not None:
        if math_action == 'addition':
            result = functions.perform_addition(operand1, operand2)
        elif math_action == 'subtraction':
            result = function.perform_subtraction(operand1, operand2)
        elif math_action == 'multiplication':
            result = function.perform_multiplication(operand1, operand2)
        elif math_action == 'division':
            result = function.perform_division(operand1, operand2)
        print(f"The result of {operand1} {math_action} {operand2} is {result}")
    elif operand1 is not None and operand2 is None:
        print(f"Please specify the operation for {operand1}")


# AIML responses for general chat
    aiml_response = chat_with_aiml(kernel, aiml_engine, user_input)
    if aiml_response:
        speak(aiml_response)
        return


        #response = API.generate_chatgpt_response(user_input)
        #response_choice = random.choice(response.split('\n'))
        #speak(response_choice)
        #return response_choice

# Initialize AIML bot and engine
kernel, aiml_engine = initialize_aiml_bot()

# Start the chatbot
speak(f"{Command.wishMe()}\nEVA is here for your service. What you like to Do today?")
while True:
    user_input = input("User: ")
    if user_input in exit_keywords:
        codeout = exit_responses
        print(codeout)
    else: response = generate_response(user_input)
    
    
    # Print bot's response
    print("EVA:", response)
