import tkinter as tk
from tkinter import ttk, messagebox
import random
import os

# --- Optional Dependency for Sound ---
try:
    from playsound import playsound
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False
# ------------------------------------

# Import the entire quiz module to access its functions and data
import quiz

# Constants are now managed in quiz.py, we just use them here.
ANSWER_CHOICES = [4, 2, 1, 0.5, 0.25, 0]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Type Master")
        self.root.geometry("700x600") # Increased height for new option
        self.root.configure(bg="#1C1C1E")
        self.root.resizable(False, False)

        # Game state variables
        self.game_state = "MENU"
        self.score = 0
        self.question_count = 0
        self.time_left = 60
        self.timer_id = None
        
        # This variable will store the user's generation choice
        self.generation_var = tk.StringVar(value="Modern")
        self.high_score = 0 # Will be loaded based on generation choice

        # --- Create UI Frames ---
        self.start_frame = tk.Frame(root, bg="#1C1C1E")
        self.quiz_frame = tk.Frame(root, bg="#1C1C1E")
        
        self._create_quiz_ui()
        self._create_start_menu()

        # Set the initial state and load the correct high score
        self._on_generation_change()

    # --- UI Creation Methods ---

    def _create_start_menu(self):
        self.start_frame.pack(fill="both", expand=True)

        tk.Label(self.start_frame, text="Type Master", font=("Helvetica", 48, "bold"), bg="#1C1C1E", fg="#FFFFFF").pack(pady=(40, 10))
        tk.Label(self.start_frame, text="The Pokémon Type-Matchup Quiz", font=("Helvetica", 16), bg="#1C1C1E", fg="#CCCCCC").pack(pady=(0, 20))

        # --- Generation Selection ---
        gen_frame = tk.Frame(self.start_frame, bg="#1C1C1E")
        gen_frame.pack(pady=10)
        tk.Label(gen_frame, text="Select Chart:", font=("Helvetica", 12), bg="#1C1C1E", fg="white").pack(side="left", padx=(0,10))
        s = ttk.Style()
        s.configure('TRadiobutton', background="#1C1C1E", foreground="white", font=("Helvetica", 11))
        ttk.Radiobutton(gen_frame, text="Modern (Gen 6+)", variable=self.generation_var, value="Modern", command=self._on_generation_change).pack(side="left", padx=5)
        ttk.Radiobutton(gen_frame, text="Classic (Gen 3)", variable=self.generation_var, value="Gen3", command=self._on_generation_change).pack(side="left", padx=5)

        self.high_score_label_menu = tk.Label(self.start_frame, text="", font=("Helvetica", 14, "italic"), bg="#1C1C1E", fg="#FFD700")
        self.high_score_label_menu.pack(pady=20)

        button_style = {"font": ("Helvetica", 14), "width": 25, "pady": 10, "bg": "#3A3A3C", "fg": "white"}
        
        tk.Button(self.start_frame, text="Endless Mode", **button_style, command=self._start_endless_mode).pack(pady=8)
        tk.Button(self.start_frame, text="Timed Challenge (60s)", **button_style, command=self._start_timed_mode).pack(pady=8)
        tk.Button(self.start_frame, text="10 Question Challenge", **button_style, command=self._start_challenge_mode).pack(pady=8)
        tk.Button(self.start_frame, text="View Type Chart", **button_style, command=self.show_type_chart).pack(pady=8)
        
    def _create_quiz_ui(self):
        self._create_question_display()
        self.breakdown_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 12), bg="#1C1C1E", fg="#BBBBBB", wraplength=650)
        self.breakdown_label.pack(pady=(5, 15))
        self.button_frame = tk.Frame(self.quiz_frame, bg="#1C1C1E")
        self.button_frame.pack(pady=10)
        self.answer_buttons = {}
        for i, choice in enumerate(ANSWER_CHOICES):
            button = tk.Button(self.button_frame, text=f"{choice}x", font=("Helvetica", 14, "bold"), width=8, bg="#3A3A3C", fg="white", command=lambda c=choice: self.check_answer(c))
            row, col = i // 3, i % 3
            button.grid(row=row, column=col, padx=10, pady=10)
            self.answer_buttons[choice] = button
        status_frame = tk.Frame(self.quiz_frame, bg="#1C1C1E")
        status_frame.pack(pady=20, fill="x", padx=50)
        self.timer_label = tk.Label(status_frame, text="", font=("Helvetica", 14), bg="#1C1C1E", fg="white")
        self.timer_label.pack(side="left")
        self.score_label = tk.Label(status_frame, text="Score: 0/0", font=("Helvetica", 14), bg="#1C1C1E", fg="white")
        self.score_label.pack(side="right")
        self.progress_bar = ttk.Progressbar(self.quiz_frame, orient="horizontal", length=400, mode='determinate')

    def _create_question_display(self):
        self.question_frame = tk.Frame(self.quiz_frame, bg="#1C1C1E")
        self.question_frame.pack(pady=(30, 5), padx=10)
        plain_style = {"bg": "#1C1C1E", "fg": "white", "font": ("Helvetica", 16)}
        pill_style = {"fg": "white", "font": ("Helvetica", 14, "bold"), "relief": "raised", "borderwidth": 2, "padx": 5, "pady": 3}
        self.q_text_1 = tk.Label(self.question_frame, text="What is the multiplier for a ", **plain_style)
        self.q_attack_type = tk.Label(self.question_frame, **pill_style)
        self.q_text_2 = tk.Label(self.question_frame, text=" attack vs. ", **plain_style)
        self.q_def_type1 = tk.Label(self.question_frame, **pill_style)
        self.q_slash = tk.Label(self.question_frame, text=" / ", **plain_style)
        self.q_def_type2 = tk.Label(self.question_frame, **pill_style)
        self.q_mark = tk.Label(self.question_frame, text="?", **plain_style)
        self.q_text_1.pack(side=tk.LEFT)
        self.q_attack_type.pack(side=tk.LEFT)
        self.q_text_2.pack(side=tk.LEFT)
        self.q_def_type1.pack(side=tk.LEFT)
        self.q_mark.pack(side=tk.LEFT)

    # --- Game Mode Start Methods ---
    def _start_game(self):
        self.start_frame.pack_forget()
        self.quiz_frame.pack(fill="both", expand=True)
        self.score = 0
        self.question_count = 0
        self.progress_bar.pack_forget()
        self.timer_label.config(text="")
        self.next_question()

    def _start_endless_mode(self):
        self.game_state = "ENDLESS"
        self._start_game()

    def _start_timed_mode(self):
        self.game_state = "TIMED"
        self.time_left = 60
        self.progress_bar.pack(pady=5)
        self.progress_bar["maximum"] = 60
        self._start_game()
        self._update_timer()

    def _start_challenge_mode(self):
        self.game_state = "CHALLENGE"
        self.progress_bar.pack(pady=5)
        self.progress_bar["maximum"] = 10
        self._start_game()
        
    # --- Core Game Logic ---
    def next_question(self):
        self.breakdown_label.config(text="")
        for btn in self.answer_buttons.values():
            btn.config(bg="#3A3A3C", state="normal")
        if self.game_state == "CHALLENGE":
            self.progress_bar["value"] = self.question_count
        elif self.game_state == "TIMED":
            self.progress_bar["value"] = self.time_left
        attack, defense1, defense2 = self.generate_question()
        self.current_attack, self.current_def1, self.current_def2 = attack, defense1, defense2
        self.correct_answer = quiz.calculate_multiplier(attack, defense1, defense2)
        self.display_question(attack, defense1, defense2)
        self._update_score_label()

    def check_answer(self, selected_answer):
        for btn in self.answer_buttons.values():
            btn.config(state="disabled")
        self.question_count += 1
        correct_button = self.answer_buttons[self.correct_answer]
        selected_button = self.answer_buttons[selected_answer]
        if selected_answer == self.correct_answer:
            self.score += 1
            selected_button.config(bg="#4CAF50")
            self._play_sound("correct.wav")
            self._flash_score("#4CAF50")
        else:
            selected_button.config(bg="#f44336")
            correct_button.config(bg="#2196F3")
            self._play_sound("incorrect.wav")
            self._flash_score("#f44336")
        self.breakdown_label.config(text=self._get_calculation_breakdown())
        self._update_score_label()
        if self.game_state == "CHALLENGE" and self.question_count >= 10:
            self.root.after(1500, self._end_game)
        else:
            self.root.after(1500, self.next_question)
            
    def _end_game(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        final_message = ""
        if self.game_state == "TIMED":
            final_message = f"Time's up! You scored {self.score}."
            if self.score > self.high_score:
                final_message += "\nNew High Score!"
                self.high_score = self.score
                self._save_high_score()
        elif self.game_state == "CHALLENGE":
            final_message = f"Challenge complete! You scored {self.score}/10."
        self.quiz_frame.pack_forget()
        self.start_frame.pack(fill="both", expand=True)
        self._on_generation_change() # Refresh high score on menu
        messagebox.showinfo("Game Over", final_message)

    # --- Helper & Utility Methods ---
    def _on_generation_change(self):
        """Called when the user clicks a radio button."""
        gen_name = self.generation_var.get()
        quiz.set_active_generation(gen_name)
        self.high_score = self._load_high_score()
        self.high_score_label_menu.config(text=f"60s High Score: {self.high_score}")

    def generate_question(self):
        all_types = quiz.ActiveGameData['types_list']
        is_dual_type = random.choice([True, False, True, True])
        attack_type = random.choice(all_types)
        defense_type1 = random.choice(all_types)
        defense_type2 = None
        if is_dual_type:
            defense_type2 = random.choice(all_types)
            while defense_type1 == defense_type2:
                defense_type2 = random.choice(all_types)
        return attack_type, defense_type1, defense_type2
        
    def display_question(self, attack, defense1, defense2):
        type_colors = quiz.ActiveGameData['colors']
        self.q_attack_type.config(text=f" {attack} ", background=type_colors[attack])
        self.q_def_type1.config(text=f" {defense1} ", background=type_colors[defense1])
        if defense2:
            self.q_def_type2.config(text=f" {defense2} ", background=type_colors[defense2])
            self.q_slash.pack(side=tk.LEFT)
            self.q_def_type2.pack(side=tk.LEFT)
        else:
            self.q_slash.pack_forget()
            self.q_def_type2.pack_forget()
        self.q_mark.pack(side=tk.LEFT)

    def _get_calculation_breakdown(self):
        attack, defense1, defense2 = self.current_attack, self.current_def1, self.current_def2
        mult1 = quiz.calculate_multiplier(attack, defense1)
        if not defense2:
            return f"{attack} → {defense1} is a {mult1}x multiplier."
        mult2 = quiz.calculate_multiplier(attack, defense2)
        total_mult = mult1 * mult2
        return (f"{attack} → {defense1} ({mult1}x)   ×   "
                f"{attack} → {defense2} ({mult2}x)   =   "
                f"Total Multiplier: {total_mult}x")

    def _update_score_label(self):
        if self.game_state == "ENDLESS":
            self.score_label.config(text=f"Score: {self.score}/{self.question_count}")
        elif self.game_state == "TIMED":
             self.score_label.config(text=f"Score: {self.score}")
        elif self.game_state == "CHALLENGE":
             self.score_label.config(text=f"Score: {self.score}/{self.question_count}")

    def _update_timer(self):
        self.time_left -= 1
        self.timer_label.config(text=f"Time: {self.time_left}s")
        self.progress_bar["value"] = self.time_left
        if self.time_left > 0:
            self.timer_id = self.root.after(1000, self._update_timer)
        else:
            self._end_game()

    def _flash_score(self, color):
        original_color = self.score_label.cget("fg")
        self.score_label.config(fg=color)
        self.root.after(500, lambda: self.score_label.config(fg=original_color))
        
    def _play_sound(self, sound_file):
        if SOUND_ENABLED:
            try:
                from threading import Thread
                sound_thread = Thread(target=lambda: playsound(sound_file), daemon=True)
                sound_thread.start()
            except Exception as e:
                print(f"Could not play sound {sound_file}: {e}")

    def _load_high_score(self):
        filename = f"highscore_{self.generation_var.get()}.txt"
        try:
            with open(filename, "r") as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_high_score(self):
        filename = f"highscore_{self.generation_var.get()}.txt"
        with open(filename, "w") as f:
            f.write(str(self.high_score))

    def show_type_chart(self):
        try:
            chart_window = tk.Toplevel(self.root)
            chart_window.title(f"Type Chart - {quiz.ActiveGameData['name']}")
            chart_window.configure(bg="#1C1C1E")
            chart_window.transient(self.root)
            chart_window.grab_set()
            
            type_colors = quiz.ActiveGameData['colors']
            sorted_types = sorted(quiz.ActiveGameData['types_list'])

            header = tk.Label(chart_window, text="Attacking → / Defending ↓", bg="#1C1C1E", fg="white", font=("Helvetica", 12, "bold"))
            header.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            
            for i, type_name in enumerate(sorted_types):
                col_header = tk.Label(chart_window, text=type_name, bg=type_colors[type_name], fg="white", font=("Helvetica", 10, "bold"), width=7, relief="ridge")
                col_header.grid(row=0, column=i + 1, padx=1, pady=1)
                row_header = tk.Label(chart_window, text=type_name, bg=type_colors[type_name], fg="white", font=("Helvetica", 10, "bold"), width=7, relief="ridge")
                row_header.grid(row=i + 1, column=0, padx=1, pady=1)

            for r, def_type in enumerate(sorted_types):
                for c, atk_type in enumerate(sorted_types):
                    multiplier = quiz.calculate_multiplier(atk_type, def_type)
                    text = f"{multiplier}x".replace(".5", "½").replace(".25", "¼")
                    cell_bg = "#3A3A3C"
                    if multiplier > 1: cell_bg = "#4CAF50"
                    elif 0 < multiplier < 1: cell_bg = "#f44336"
                    elif multiplier == 0: cell_bg = "#607D8B"
                    cell = tk.Label(chart_window, text=text, bg=cell_bg, fg="white", font=("Helvetica", 10), width=7, relief="ridge")
                    cell.grid(row=r + 1, column=c + 1, padx=1, pady=1)
        except tk.TclError:
            print("Chart window is already open.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()