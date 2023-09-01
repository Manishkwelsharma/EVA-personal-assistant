import aiml
import pyttsx3

# Create the kernel
kernel = aiml.Kernel()

# Load AIML files
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

# Initialize pyttsx3 Text-to-Speech engine
engine = pyttsx3.init()

# Get all available voices
voices = engine.getProperty('voices')

# Find the Jarvis voice
eva_voice = None
for voice in voices:
    if voice.name == 'Microsoft Zira Desktop - English (United States)':
        eva_voice = voice
        break

# Set the voice of the engine to Jarvis
if eva_voice is not None:
    engine.setProperty('voice', eva_voice.id)

# Define the speak function
def speak(text):
    print("EVA:", text)
    engine.say(text)
    engine.runAndWait()



# Define a user input loop
while True:
    # Get user input
    user_input = input("User:")

    # Pass user input to the kernel for a response
    bot_response = kernel.respond(user_input)

    # Print the bot's response
    print("EVA:", bot_response)

    # Speak the bot's response using pyttsx3
    engine.say(bot_response)
    engine.runAndWait()
