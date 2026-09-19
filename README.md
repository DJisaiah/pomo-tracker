<div align="center">
  <img width="700" alt="hero1" src=".github/hero_design/hero1.png" />
  <h1>Pomo-Tracker</h1>
  <p><b>A modern, intuitive Pomodoro timer & productivity tracker with rich statistics and Discord presence.</b></p>

  <p>
    <a href="https://github.com/DJisaiah/pomo-tracker/releases"><img src="https://img.shields.io/github/v/release/DJisaiah/pomo-tracker?color=orange&style=flat-square" alt="Release" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License" /></a>
    <a href="#installation"><img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square" alt="Platforms" /></a>
    <a href="https://flet.dev/"><img src="https://img.shields.io/badge/Built%20with-Flet%20(Python)-blueviolet?style=flat-square" alt="Flet" /></a>
  </p>
  <sub><i>Windows (Microsoft Store & Executable) ⋅ Linux (AUR, AppImage, Executable) ⋅ macOS (Executable)</i></sub>
</div>

## Overview
- **Pomo-Tracker** is a simple, intuitive Pomodoro timer application built with Flet. 
    - It aims to help users boost productivity by adhering to the Pomodoro Technique with additional features like: 
        - **Custom timers** Ranging from 5mins to 8hrs
        - **Stopwatch modes** for sessions where you just want to work without a set time in mind
        - **Comprehensive productivity tracking**  for actually informative graphs and other tracking
        - **Discord Rich Presence** so your other friends can see your grind
        - **Feed Platform** to provide the ability to keep up with friends on studies/study habits and their stats.
            - See friend activity
            - Rankings to compete with your friends 
        - **Cross-Platform Stats Syncing** between other clients (desktop, mobile)

## Features

| Current Features: Timer Page | Current Features: Stats Page | Upcoming: Platforms & Sync | Upcoming: App Features |
| :--- | :--- | :--- | :--- |
| • Functional custom Pomodoro timer | • 365-day activity heatmap | • Cross-Platform Sync | • Rankings / Feed Page |
| • Implemented sound effects | • Subject time tracking graph (Daily, Weekly, Monthly, Yearly) | • Release on Android | • Settings Page |
| • Add & select tracking subjects | • Partial Feed Page | | • Custom User Themes |
| • Discord Rich Presence integration | | | |

> Besides new features coming in, old features will also be enhanced.    
   
### Screenshots

<div align="center">
    <img width="700" alt="Hero 2" src=".github/hero_design/hero2.png" />
</div>

<details>
  <summary><b>More Screenshots</b></summary>
  <br>
  
  <div align="center">
    <img width="48%" alt="Timer Page" src="screenshots/timer page.png" />
    <img width="48%" alt="Stats Page 1" src="screenshots/stats page 1.png" />
    <img width="60%" alt="Stats Page 2" src="screenshots/stats page 2.png" />
    <br><br>
    <b>Discord Rich Presence</b><br>
    <img width="320" alt="RPC 1" src="screenshots/new rpc1.png" />
    <img width="320" alt="RPC 2" src="screenshots/new rpc2.png" />
    <br>
    <img width="320" alt="RPC 3" src="screenshots/new rpc3.png" />
    <img width="320" alt="RPC 4" src="screenshots/new rpc4.png" />
  </div>
</details>

<details>
  <summary><b>Other Hero Images</b></summary>
  <br>
  <div align="center">
    <img width="700" alt="Hero 2" src=".github/hero_design/hero2.png" />
    <br><br>
    <img width="700" alt="Hero 3" src=".github/hero_design/hero3.png" />
  </div>
</details>

## Installation

> This project is under active development, and features are subject to change. If you find bugs/issues, kindly raise an issue with the `bug` or `feature` tag.

| Platform | Distribution Method | Quick Link / Command |
| :--- | :--- | :--- |
| **Windows** | Microsoft Store | [<img src="https://get.microsoft.com/images/en-us%20dark.svg" width="140" alt="Get it from Microsoft" />](https://get.microsoft.com/installer/download/9N5Z286TKJQ5?referrer=appbadge) |
| **Windows, Linux, macOS** | GitHub Releases | [Download Latest Binaries](https://github.com/DJisaiah/pomo-tracker/releases/latest) |
| **Arch Linux** | AUR (`pomo-tracker-bin`) | `paru -S pomo-tracker-bin` or `yay -S pomo-tracker-bin` |

<details>
  <summary><b>Arch Linux (AUR) Detailed Guide</b></summary>

You can install `pomo-tracker-bin` from the Arch User Repository using an AUR helper:

```bash
# Using paru
paru -S pomo-tracker-bin

# Using yay
yay -S pomo-tracker-bin
```

#### Manual Installation

If you prefer building manually without an AUR helper:

```bash
git clone https://aur.archlinux.org/pomo-tracker-bin.git
cd pomo-tracker-bin
makepkg -si
```

</details>

## Technologies Used
* **Flet**: GUI
* **Python**: The Core Language
* **SQLite**: Local Database for Stats and Settings 
* **pypresence**: Discord RPC
* **Subject Icons Images**: [Undraw Open Source Illustrations](https://undraw.co/)

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

```mermaid
timeline
    title Pomo-Tracker Roadmap
    v0.3.0 Polish and Stronger Foundation : Fully functional mobile build
                                 : Desktop notifications and pause alerts
                                 : More stats features (streaks, heatmap hover)
                                 : List completed tasks in a session
                                 : Bug Fixes
                                 : Quality of Life
    v0.4.0 Desktop Companion     : Deskmate mini-timer window
                                 : Floating desktop ticket widget
                                 : Centralized settings page
                                 : State-listener architecture refactor
                                 : Consider untracked time
    v0.5.0 Advanced Tracking     : Macro buttons per subject
                                 : Nested sub-subjects and archiving
                                 : Comparative stats and target lines
                                 : Auto-continue break detection
    v0.6.0 Productivity Hub      : First-time onboarding flow
                                 : Modular home and timer widgets
                                 : Built-in scheduler page
	Uncertain 					           : Cross-platform Sync
								                 : Full Feed Page
																 : Play Store release
																 : Custom themes
																 : Group Study Sessions & Quizzes
```
