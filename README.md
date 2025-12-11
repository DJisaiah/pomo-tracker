# Pomo-Tracker

## 🚀 Overview
- Pomo-Tracker is a simple, intuitive Pomodoro timer application built with Flet. 
    - It aims to help users boost productivity by adhering to the Pomodoro Technique with additional features like: 
        - **Custom timers** *go beyond 25mins*
        - **Stopwatch modes** *for sessions where you just want to keep going*
        - **Comprehensive productivity tracking** *actually informative graphs and other tracking*
        - **Feed Platform** *the ability to keep up with friends on studies/study habits and their stats.*
        - **Cross-Platform Stats Syncing** *sync data between other clients (desktop, mobile)*
        - **Discord Rich Presence** *so your other friends can see your grind*

## ✨ Features

### Current Features
* **Basic Pomodoro Timer:** A functional 25-minute Pomodoro timer.
* **Clean UI:** Simple and clear display of the remaining time.
* **Navigation:** Basic navigation tabs for Timer, Stats, Rankings, and Settings sections.
* **Subject Tracker:** Basic subject/task tracking for stats
    - Heatmap
    - Subject Hour Tracking
* **Timer Sound Effects**
* **Discord RPC** Allow friends to see your study habits

Screenshots:
<img width="731" height="734" alt="image" src="https://github.com/user-attachments/assets/ed0908e7-b4d6-4c66-b29f-8297d7e33c61" />
<img width="726" height="741" alt="image" src="https://github.com/user-attachments/assets/4a0c8b81-ec04-46b0-8851-25102a795b9f" />
<img width="423" height="178" alt="image" src="https://github.com/user-attachments/assets/7f90879f-bce3-4f80-b24c-0725fed1743a" />
<img width="322" height="134" alt="image" src="https://github.com/user-attachments/assets/929e63d6-587c-4522-a1fa-4e43817af033" />


### Todo:
* Implement Settings Page
* User Custom Themes
* Implement Rankings Page With Remote Database
* Release on Windows
* Release on Linux
* Release on macOS
* Release on Android

## 🛠 Technologies Used
* **Flet:** GUI
* **Python:** The Core Language
* **SQLite** Local Database for Stats and Settings 
* **pypresence** Discord RPC

## 💻 Setup
**This project is under active development, and features are subject to change**
To get Pomo-Tracker up and running on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DJisaiah/pomo-tracker.git
    cd pomo-tracker
    ```

2.  **Install Flet:**
    If you don't have Flet installed, you can install it via pip:
    ```bash
    pip install flet
    ```

3.  **Run the application:**
    ```bash
    flet run
    ```

## 💡 Usage
Once the application is running, you will see the main timer screen.
* Click the **Play button** (▶️) to start the Pomodoro timer.
* Click the **Stop button** (⏹️) to pause/stop the timer.
* Explore the navigation tabs at the top (Timer, Stats, Rankings, Settings) to see future planned sections.

## 📄 License
This project is licensed under the MIT License - see the `LICENSE` file for details.
