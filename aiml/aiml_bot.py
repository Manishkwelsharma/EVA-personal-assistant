import aiml
import pyttsx3

def initialize_aiml_bot():
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

    return kernel, engine

def chat_with_aiml(kernel, engine):
    while True:
        user_input = input("User: ")

        if user_input.lower() == 'exit':
            break

        # Pass user input to the kernel for a response
        bot_response = kernel.respond(user_input)

        # Print the bot's response
        print("EVA:", bot_response)

        # Speak the bot's response using pyttsx3
        engine.say(bot_response)
        engine.runAndWait()
