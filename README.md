# Voice Assistant - Jarvis

A simple Python-based voice assistant that listens for your commands and performs various tasks on your Windows laptop. It supports opening/closing software, playing YouTube videos, searching Google, checking weather, controlling system volume, taking screenshots, and more.

---

## Features

- Wake word detection: say **"Jarvis"** to activate.
- Open and close common applications (Chrome, Edge, Notepad, Calculator).
- Play songs or videos on YouTube automatically by voice command.
- Google search by voice.
- Get weather updates for any city.
- Open folders or files on your system.
- Take screenshots and save them automatically.
- Control system volume.
- Open Google Calendar in your default browser.
- Tell the current time.
- Respond to fun questions like "Who is god?" and "What is your name?".

---

## Requirements

- Python 3.7+
- Windows OS (tested on Windows 10/11)
- Microphone for voice input
- Internet connection (for search, weather, YouTube)

---

## Required Python Packages

Install dependencies using pip:

```bash
pip install speechrecognition pyttsx3 pywhatkit requests pyautogui pycaw comtypes
