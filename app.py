import tkinter as tk
from tkinter import messagebox
import random

from quiz import TYPE_CHART, calculate_multiplier

ALL_TYPES = list(TYPE_CHART.keys())
ANSWER_CHOICES = [4, 2, 1, 0.5, 0.25, 0]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Type Master - By Isaac McGowan")
        self.root.geometry("500x350")
        self.root.configure(bg="#1C1C1E")

        self.score = 0
        self.question_count = 0

        self.question_label = tk.Label(root, text="", font=("Helvetica", 16), wraplength=480, bg="#1C1C1E", fg="white")
        self.question_label.pack(pady=20)

        self.button_frame = tk.Frame(root, bg="#1C1C1E")
        self.button_frame.pack(pady=10)

        self.answer_buttons = []
        for i, choice in enumerate(ANSWER_CHOICES):
            button = tk.Button(self.button_frame, text=f"{choice}x", font=("Helvetica", 14, "bold"), width=8, bg="#3A3A3C", fg="white", command=lambda c=choice: self.check_answer(c))
            row, col = i // 3, i % 3
            button.grid(row=row, column=col, padx=10, pady=10)

        self.score_label = tk.Label(root, text="Score: 0/0", font=("Helvetica", 12), bg="#1C1C1E", fg="white")
        self.score_label.pack(pady=20)

        self.next_question()

    def generate_question(self):
        is_dual_type = random.choice([True, False, True]) # Skew towards dual-types
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
        if defense2:
            self.question_label.config(text=f"What is the multiplier for a {attack} attack vs. {defense1} / {defense2}?")
        else:
            self.question_label.config(text=f"What is the multiplier for a {attack} attack vs. {defense1}?")
        self.score_label.config(text=f"Score: {self.score}/{self.question_count}")

    def check_answer(self, selected_answer):
        self.question_count += 1
        if selected_answer == self.correct_answer:
            self.score += 1
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showerror("Result", f"Incorrect! The answer was {self.correct_answer}x.")
        self.next_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()