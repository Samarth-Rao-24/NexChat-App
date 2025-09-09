# NexChat 🗨️

A simple, judge-friendly chat app built with Python and Tkinter. It supports Firebase login, real-time messaging, offline queueing, emoji support, and a polished UI with theme toggling.

---

## Features

- 🔐 Login with Firebase  
- 💬 Real-time chat using Firebase Realtime DB  
- 📦 Offline message queue (auto-send when online)  
- 🎨 Light/Dark theme toggle  
- 😄 Emoji bar for quick reactions  
- ✍️ Typing indicator  
- 🧱 Modular codebase for easy updates

---

## Setup Instructions

1. **Clone the repo**
   git clone https://github.com/Samarth-Rao-24/NexChat-App.git
   cd NexChat-App

- Install dependencies
    pip install -r requirements.txt

- Add Firebase confi
    - Create a .env file and add your Firebase keys (keep this file private

- Run the app
    python main.py

Folder Structure
    ├── main.py
    ├── firebase_config.py
    ├── features/
    ├── assets/
    ├── splash.py
    ├── ui_utils.py
    ├── requirements.txt
    └── README.md


Notes

- Secrets like .env and firebase_key.json are ignored via .gitignore
- Designed for hackathons and demos — clean UI, reproducible setup
- Screenshots and demo GIFs coming soon!


Author
    Bult by Samarth H Rao