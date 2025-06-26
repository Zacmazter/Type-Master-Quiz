# Type Master Quiz

A Python-based GUI quiz application designed to test and improve your knowledge of Pokémon type effectiveness. Challenge yourself with different game modes, learn from your mistakes with instant feedback, and track your high scores!

 
*(This is a sample screenshot. You can create your own and replace the link!)*

---

## Features

- **Modern & Clean UI:** A dark-themed interface built with Tkinter, featuring colored "pills" for Pokémon types.
- **Multiple Game Modes:** Choose from Endless, Timed, or Challenge modes to suit your playstyle.
- **Instant Feedback:** No more disruptive pop-ups! Get immediate color-coded feedback on your answers directly within the app.
- **Calculation Breakdown:** Understand *why* an answer is correct with a simple breakdown of the damage calculation for dual-type matchups.
- **High Score Tracking:** Your best score in the 60-second Timed Challenge is saved locally.
- **Built-in Type Chart:** Quickly reference a full, color-coded type effectiveness chart anytime.
- **Sound Effects:** Optional audio cues for correct and incorrect answers.
- **Standalone Executable:** Can be easily packaged into a single `.exe` file for distribution on Windows.

---

## Game Modes Explained

- **Endless Mode:** Play for as long as you want. The quiz continues indefinitely, tracking your score and the number of questions answered.
- **Timed Challenge (60s):** How many questions can you answer correctly in 60 seconds? This is where your high score is recorded!
- **10 Question Challenge:** A fixed-length quiz. At the end, you'll get your final score out of 10.

---

## Technologies Used

- **Python 3**
- **Tkinter** (for the Graphical User Interface)
- **Playsound** (for optional sound effects)
- **PyInstaller** (for creating the executable)

---

## How to Run from Source Code

To run this application from the source code, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Zacmazter/Type-Master-Quiz.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd Type-Master-Quiz
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

---

## Creating the Executable

You can package this application into a single, double-clickable `.exe` file using PyInstaller.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run the build command from the project directory:**
    ```bash
    pyinstaller --onefile --windowed --name="TypeMaster" --icon="path/to/your/icon.ico" app.py
    ```
    *(The `--icon` flag is optional but recommended for a professional look.)*

3.  Find your finished application inside the newly created `dist` folder.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details. *(You can add a LICENSE file to your repository if you wish.)*

---

Created by **Isaac McGowan**
