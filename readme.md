# Deep IQ: The Wrath of Zorr - Digital Assistant

![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg) ![UI Framework](https://img.shields.io/badge/UI-PySide6-279624.svg) ![License](https://img.shields.io/badge/License-MIT-blue.svg)

This application is a desktop digital assistant for the "Deep IQ: The Wrath of Zorr" solo variant for Magic: The Gathering. It automates the AI's (Zorr's) turn by handling all the die rolls, table lookups, and advancement tracking, allowing you to focus on your own gameplay.

## 📸 Screenshot

_A screenshot of the application's user interface would go here._

## ✨ Features

- **Automated AI Turns:** Simply press a key to have the app perform all of Zorr's actions for the turn.
- **Full Table Implementation:** Includes all main tables, bonus tables, and the "Zorr's Wrath" chart from the rule document.
- **Automatic Advancement:** The app automatically tracks when Zorr "levels up" to the next table based on the roll results.
- **Clean, Readable Interface:** A modern, dark-themed UI with large fonts, making it easy to read from a distance during gameplay.
- **Simple Controls:** Intuitive keyboard controls for a seamless experience.
- **Standalone Executable:** No need to install Python or any libraries. Just run the `.exe` file (for Windows users).

## 🚀 Getting Started

There are two ways to get the application running: as a user (easiest) or as a developer.

### For Users (Windows)

1.  Navigate to the **Releases** section of this repository.
2.  Download the latest `WrathOfZorr.exe` file.
3.  Place the `.exe` file in any folder and double-click it to run. That's it!

### For Developers (Running from Source)

If you want to run the application from the source code or make modifications, you will need Python 3 installed on your system.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    - On Windows:
      ```bash
      python -m venv .venv
      .venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      python -m venv .venv
      source .venv/bin/activate
      ```

3.  **Install the required libraries:**
    ```bash
    pip install PySide6
    ```

4.  **Run the application:**
    ```bash
    python gui.py
    ```

## 🎮 How to Use

The application is designed to be as simple as possible.

- **Launch the application** by running the `.exe` or the `gui.py` script.
- **Press the `SPACEBAR`** to simulate Zorr's turn. The results will be displayed on the screen.
- **Press the `ESC` key** at any time to close the application.

## 📁 Project Structure

The project is organized into two main files to separate logic from the presentation:

- `main.py`: The backend of the application. It contains the `ZorrAI` class, which holds all the game rules, tables, and logic for handling a turn. It has no UI code.
- `gui.py`: The frontend of the application. It contains all the PySide6 code for building the user interface, handling user input (key presses), and displaying the data provided by `main.py`.

## 🛠️ Built With

*   [Python 3](https://www.python.org/) - The core programming language.
*   [PySide6](https://www.qt.io/qt-for-python) - The framework used for the graphical user interface (GUI).
*   [PyInstaller](https://pyinstaller.org/) - The tool used to package the application into a standalone `.exe` file.

## 🙏 Acknowledgments

This application is purely a fan-made digital assistant. The credit for the solo variant rules and design goes to its creators.

- **Deep IQ–2013** by **Bruce Richard**.
- **Deep IQ: The Wrath of Zorr** update by **Phill Webb**.

## 📄 License

This project is licensed under the MIT License.