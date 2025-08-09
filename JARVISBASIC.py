import speech_recognition as sr
import pyttsx3
import os
import datetime
import subprocess
import sys
import pywhatkit
import webbrowser
import requests
import pyautogui
import time
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Weather API Key
WEATHER_API_KEY = "2aaf165581a4befd70fa64b979b724e6"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def google_search(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    speak(f"Searching Google for {query}")

def get_weather(city):
    try:
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
        response = requests.get(base_url, params=params)
        data = response.json()
        if data["cod"] != "404":
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            speak(f"The weather in {city} is {temp} degrees Celsius with {description}")
        else:
            speak("City not found.")
    except Exception:
        speak("Sorry, I couldn't get the weather right now.")

def open_path(path):
    try:
        if os.path.exists(path):
            os.startfile(path)
            speak(f"Opened {path}")
        else:
            speak("Path not found.")
    except Exception:
        speak("Sorry, I couldn't open the path.")

def take_screenshot():
    filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    pyautogui.screenshot().save(filename)
    speak(f"Screenshot saved as {filename}")

def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level, None)
        speak(f"Volume set to {int(level*100)} percent")
    except Exception:
        speak("Sorry, I couldn't change the volume.")

def open_calendar():
    webbrowser.open("https://calendar.google.com/")
    speak("Opening Google Calendar")

def open_software(software_name):
    if 'chrome' in software_name:
        speak('Opening Chrome...')
        program = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([program])
    elif 'microsoft edge' in software_name:
        speak('Opening Microsoft Edge...')
        program = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        subprocess.Popen([program])
    elif 'play' in software_name:
        song = software_name.replace('play', '').strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
        time.sleep(5)  # Wait for YouTube page to load
        pyautogui.press('space')  # Press space to play video
    elif 'notepad' in software_name:
        speak('Opening Notepad...')
        subprocess.Popen(['notepad.exe']) 
    elif 'calculator' in software_name:
        speak('Opening Calculator...')
        subprocess.Popen(['calc.exe'])
    else:
        speak(f"I couldn't find the software {software_name}")

def close_software(software_name):
    if 'chrome' in software_name:
        speak('Closing Chrome...')
        os.system("taskkill /f /im chrome.exe")
    elif 'microsoft edge' in software_name:
        speak('Closing Microsoft Edge...')
        os.system("taskkill /f /im msedge.exe")
    elif 'notepad' in software_name:
        speak('Closing Notepad...')
        os.system("taskkill /f /im notepad.exe")
    elif 'calculator' in software_name:
        speak('Closing Calculator...')
        os.system("taskkill /f /im calculator.exe")
    else:
        speak(f"I couldn't find any open software named {software_name}")

def listen_for_wake_word():
    with sr.Microphone() as source:
        print('Listening for wake word...')
        while True:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            recorded_audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(recorded_audio, language='en_US').lower()
                if 'hey jarvis' in text:
                    print('Wake word detected!')
                    speak('welcome back thujee')
                    return True
                elif 'jarvis' in text:
                    print('Wake word detected!')
                    speak('Hi thujee, How can I assist you?')
                    return True
            except:
                pass

def get_basic_response(text):
    # Knowledge base for various topics
    knowledge_base = {
        # Personal and Identity
        'how are you': "I'm doing well, thank you for asking! How can I assist you today?",
        'who are you': "I am JARVIS, your advanced AI assistant. I'm designed to help you with various tasks and answer your questions.",
        'what is your name': "My name is JARVIS, which stands for Just A Rather Very Intelligent System.",
        'what can you do': "I can help you with many things like: answering questions, checking weather, opening apps, searching the web, telling time, and much more!",
        'your creator': "I was created as your personal AI assistant to help make your daily tasks easier.",
        
        # Greetings and Casual
        'hello': "Hello! I'm ready to help you with anything you need!",
        'hi': "Hi there! How may I assist you today?",
        'good morning': "Good morning! Ready to start the day?",
        'good afternoon': "Good afternoon! How can I help you?",
        'good evening': "Good evening! What can I do for you?",
        'bye': "Goodbye! Have a wonderful day!",
        'thank you': "You're welcome! I'm always happy to help!",
        
        # Technical Capabilities
        'help': "I can: \n1. Open/close applications\n2. Check weather\n3. Tell time\n4. Take screenshots\n5. Control volume\n6. Search the web\n7. Answer questions\n8. Play music\nJust ask me what you need!",
        'what is your purpose': "I'm your AI assistant, designed to help with tasks, answer questions, and make your interaction with technology smoother and more efficient.",
        
        # Science and Nature
        'what is gravity': "Gravity is a fundamental force of nature that attracts objects with mass towards each other. On Earth, it's what keeps us on the ground!",
        'what is space': "Space is the boundless expanse beyond Earth's atmosphere, containing planets, stars, galaxies, and other cosmic objects.",
        'what are planets': "Planets are celestial bodies that orbit stars. In our solar system, there are 8 planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.",
        
        # Technology
        'what is ai': "AI (Artificial Intelligence) is technology that enables computers to simulate human intelligence, learning from experience and performing human-like tasks.",
        'what is internet': "The Internet is a global network of connected computers that allows people worldwide to communicate and share information.",
        'what is computer': "A computer is an electronic device that processes data to perform various tasks like calculations, storing information, and running programs.",
        
        # Life and Biology
        'what is life': "Life is characterized by growth, reproduction, response to environment, and the ability to maintain internal balance. It comes in many forms on Earth.",
        'human body': "The human body is a complex organism with multiple systems working together, including the nervous, circulatory, respiratory, and digestive systems.",
        
        # Mathematics
        'what is math': "Mathematics is the science of numbers, quantities, and shapes. It's used to solve problems and understand patterns in the world.",
        
        # General Knowledge
        'what is time': "Time is a measure of events from past through present to future. It's how we track the sequence of events and organize our lives.",
        'what is money': "Money is a medium of exchange used to buy and sell goods and services. It can be physical (like coins) or digital.",
        'what is language': "Language is a structured system of communication using words, sounds, or gestures to express meaning between people.",
        
        # Fun Facts
        'tell me a fact': "Here's a cool fact: The human brain can process images seen for as little as 13 milliseconds!",
        'another fact': "Did you know? Honey never spoils. Archaeologists have found 3000-year-old honey in ancient Egyptian tombs, and it's still perfectly edible!"
    }
    
    text = text.lower()
    
    # Check for question types
    if 'what is' in text or 'who is' in text or 'how' in text or 'why' in text:
        # Extract the main topic from the question
        for key in knowledge_base:
            if key in text:
                return knowledge_base[key]
        
        # Handle calculations
        if 'calculate' in text or any(op in text for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided']):
            try:
                # Convert text to mathematical expression
                expression = text.replace('what is', '').replace('calculate', '').replace('plus', '+').replace('minus', '-').replace('times', '*').replace('divided by', '/').strip()
                # Safely evaluate the expression
                result = eval(expression)
                return f"The result is {result}"
            except:
                pass
    
    # Check for commands and statements
    for key in knowledge_base:
        if key in text:
            return knowledge_base[key]
    
    # Handle general knowledge queries
    if 'tell me about' in text:
        topic = text.replace('tell me about', '').strip()
        return f"Let me tell you what I know about {topic}. Would you like me to search the web for more detailed information?"
    
    # If no direct match found, provide a helpful response
    return "I understand you're asking about " + text + ". While I don't have specific information about that, I can:\n1. Search the web for you\n2. Try to break down the question\n3. Help you rephrase it\nWhat would you like me to do?"

def get_response(question):
    # Use our built-in knowledge base for responses
    return get_basic_response(question)

def cmd():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print('Ask me anything...')
        recorded_audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(recorded_audio, language='en_US').lower()
        print('Your message:', text)
    except Exception as ex:
        print(ex)
        return

    if 'stop' in text:
        speak('Stopping the program. Goodbye!')
        sys.exit()

    if 'open' in text:
        software_name = text.replace('open', '').strip()
        open_software(software_name)
    elif 'close' in text:
        software_name = text.replace('close', '').strip()
        close_software(software_name)
    elif 'time' in text:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(current_time)
    elif 'who is god' in text:
        speak('Ajitheyyy Kadavuleyy')
    elif 'what is your name' in text:
        speak('My name is Jack, your Artificial Intelligence')
    elif 'search about' in text:
        query = text.replace('search about', '').strip()
        google_search(query)
    elif "what's the weather in" in text or "weather in" in text:
        city = text.replace("what's the weather in", '').replace('weather in', '').strip()
        get_weather(city)
    elif 'open folder' in text or 'open file' in text:
        path = text.replace('open folder', '').replace('open file', '').strip()
        open_path(path)
    elif 'take screenshot' in text:
        take_screenshot()
    elif 'set volume to' in text:
        try:
            percent = int(text.replace('set volume to', '').replace('%', '').strip())
            set_volume(percent / 100)
        except:
            speak("Please say the volume as a number between 0 and 100.")
    elif 'open calendar' in text:
        open_calendar()
    else:
        # Use our knowledge base for responses
        response = get_response(text)
        if response:
            speak(response)

while True:
    if listen_for_wake_word():
        while True: 
            if cmd():
                break
 