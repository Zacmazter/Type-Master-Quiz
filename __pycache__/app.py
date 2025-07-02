import tkinter as tk
from tkinter import messagebox
import random

from quiz import TYPE_CHART, TYPE_COLORS, calculate_multiplier

ALL_TYPES = list(TYPE_CHART.keys())
ANSWER_CHOICES = [4, 2, 1, 0.5, 0.25, 0]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Type Master - By Isaac McGowan")
        self.root.geometry("600x400") # Increased width for the new layout
        self.root.configure(bg="#1C1C1E")

        self.score = 0
        self.question_count = 0

        self.create_menu()
        
        # --- Create the new, structured question display ---
        self._create_question_display()

        # --- Button Frame remains the same ---
        self.button_frame = tk.Frame(root, bg="#1C1C1E")
        self.button_frame.pack(pady=20)
        self.answer_buttons = []
        for i, choice in enumerate(ANSWER_CHOICES):
            button = tk.Button(self.button_frame, text=f"{choice}x", font=("Helvetica", 14, "bold"),
                               width=8, bg="#3A3A3C", fg="white", command=lambda c=choice: self.check_answer(c))
            row, col = i // 3, i % 3
            button.grid(row=row, column=col, padx=10, pady=10)

        # --- Score Label remains the same ---
        self.score_label = tk.Label(root, text="Score: 0/0", font=("Helvetica", 12), bg="#1C1C1E", fg="white")
        self.score_label.pack(pady=20)

        self.next_question()

    def _create_question_display(self):
        """Creates a Frame to hold all parts of the question for clean formatting."""
        self.question_frame = tk.Frame(self.root, bg="#1C1C1E")
        self.question_frame.pack(pady=20, padx=10)

        # Define styles for reuse
        plain_style = {"bg": "#1C1C1E", "fg": "white", "font": ("Helvetica", 16)}
        pill_style = {"fg": "white", "font": ("Helvetica", 14, "bold"), "relief": "raised", "borderwidth": 2}

        # Create all the label widgets once
        self.q_text_1 = tk.Label(self.question_frame, text="What is the multiplier for a ", **plain_style)
        self.q_attack_type = tk.Label(self.question_frame, **pill_style)
        self.q_text_2 = tk.Label(self.question_frame, text=" attack vs. ", **plain_style)
        self.q_def_type1 = tk.Label(self.question_frame, **pill_style)
        self.q_slash = tk.Label(self.question_frame, text=" / ", **plain_style)
        self.q_def_type2 = tk.Label(self.question_frame, **pill_style)
        self.q_mark = tk.Label(self.question_frame, text="?", **plain_style)

        # Pack them in order
        self.q_text_1.pack(side=tk.LEFT)
        self.q_attack_type.pack(side=tk.LEFT, padx=3)
        self.q_text_2.pack(side=tk.LEFT)
        self.q_def_type1.pack(side=tk.LEFT, padx=3)
        # The slash and second type will be managed by display_question
        self.q_mark.pack(side=tk.LEFT)

    def display_question(self, attack, defense1, defense2):
        """Configures the labels in the question_frame to show the current question."""
        # Configure the attack type pill
        self.q_attack_type.config(text=f" {attack} ", background=TYPE_COLORS[attack])
        
        # Configure the first defense type pill
        self.q_def_type1.config(text=f" {defense1} ", background=TYPE_COLORS[defense1])

        # Handle the optional second defense type
        if defense2:
            self.q_def_type2.config(text=f" {defense2} ", background=TYPE_COLORS[defense2])
            # If it's a dual type, make sure the slash and second pill are visible and in order
            self.q_slash.pack(side=tk.LEFT)
            self.q_def_type2.pack(side=tk.LEFT, padx=3)
        else:
            # If it's a single type, hide the slash and second pill
            self.q_slash.pack_forget()
            self.q_def_type2.pack_forget()
        
        # Ensure the question mark is always at the end
        self.q_mark.pack(side=tk.LEFT)

    def create_menu(self):
        """Creates the main menu bar for the application."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="View Type Chart", command=self.show_type_chart)

    def generate_question(self):
        is_dual_type = random.choice([True, False, True])
        attack_type = random.choice(ALL_TYPES)
        defense_type1 = random.choice(ALL_TYPES)
        defense_type2 = None
        if is_dual_type:
            defense_type2 = random.choice(ALL_TYPES)
            while defense_type1 == defense_type2:
                defense_type2 = random.choice(ALL_TYPES)
        return attack_type, defense_type1, defense_type2

    def next_question(self):
        attack, defense1, defense2 = self.generate_question()
        self.correct_answer = calculate_multiplier(attack, defense1, defense2)
        self.display_question(attack, defense1, defense2)
        self.score_label.config(text=f"Score: {self.score}/{self.question_count}")

    def check_answer(self, selected_answer):
        self.question_count += 1
        if selected_answer == self.correct_answer:
            self.score += 1
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showerror("Result", f"Incorrect! The answer was {self.correct_answer}x.")
        self.next_question()

    def show_type_chart(self):
        """Creates a new Toplevel window to display the full type chart."""
        # Sort ALL_TYPES alphabetically for a clean, predictable chart layout
        sorted_types = sorted(ALL_TYPES)

        chart_window = tk.Toplevel(self.root)
        chart_window.title("Type Effectiveness Chart")
        chart_window.configure(bg="#1C1C1E")
        header = tk.Label(chart_window, text="Attacking → / Defending ↓", bg="#1C1C1E", fg="white", font=("Helvetica", 12, "bold"))
        header.grid(row=0, column=0, padx=5, pady=5)
        
        for i, type_name in enumerate(sorted_types):
            col_header = tk.Label(chart_window, text=type_name, bg=TYPE_COLORS[type_name], fg="white", font=("Helvetica", 10, "bold"), width=7, relief="ridge")
            col_header.grid(row=0, column=i + 1, padx=1, pady=1)
            row_header = tk.Label(chart_window, text=type_name, bg=TYPE_COLORS[type_name], fg="white", font=("Helvetica", 10, "bold"), width=7, relief="ridge")
            row_header.grid(row=i + 1, column=0, padx=1, pady=1)

        for r, def_type in enumerate(sorted_types):
            for c, atk_type in enumerate(sorted_types):
                multiplier = calculate_multiplier(atk_type, def_type)
                text = f"{multiplier}x".replace(".5", "½").replace(".25", "¼")
                cell_bg = "#3A3A3C"
                if multiplier == 2: cell_bg = "#4CAF50"
                elif multiplier == 0.5 or multiplier == 0.25: cell_bg = "#f44336"
                elif multiplier == 0: cell_bg = "#607D8B"
                cell = tk.Label(chart_window, text=text, bg=cell_bg, fg="white", font=("Helvetica", 10), width=7, relief="ridge")
                cell.grid(row=r + 1, column=c + 1, padx=1, pady=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()