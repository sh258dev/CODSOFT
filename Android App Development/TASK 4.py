#Requirements (Install Before Running)
# Required Installation (Run this first in terminal):
# pip install customtkinter json random os
# If you don't have customtkinter, json, random, or os installed, run the
# following command in your terminal:
# python -m pip install --upgrade pip
# or
# pip install --upgrade pip
# Required Installation (Run this first in terminal):
import customtkinter as ctk
from tkinter import messagebox
import json
import random
import os

QUIZ_FILE = "quizzes.json"  # You can define multiple quizzes here

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Quiz App")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.quiz_data = self.load_quizzes()
        self.selected_quiz = None
        self.question_index = 0
        self.score = 0
        self.user_answers = []

        self.main_menu()

    def load_quizzes(self):
        if os.path.exists(QUIZ_FILE):
            with open(QUIZ_FILE, "r") as f:
                return json.load(f)
        else:
            return {
                "General Knowledge": [
                    {
                        "question": "What is the capital of France?",
                        "options": ["Berlin", "Madrid", "Paris", "Lisbon"],
                        "answer": "Paris"
                    },
                    {
                        "question": "Who wrote 'Romeo and Juliet'?",
                        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Leo Tolstoy"],
                        "answer": "William Shakespeare"
                    }
                ],
                "Science": [
                    {
                        "question": "What is the chemical symbol for water?",
                        "options": ["H2O", "O2", "CO2", "NaCl"],
                        "answer": "H2O"
                    },
                    {
                        "question": "Which planet is known as the Red Planet?",
                        "options": ["Venus", "Earth", "Mars", "Saturn"],
                        "answer": "Mars"
                    }
                ]
            }

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.root, text="🧠 Quiz App", font=("Arial", 28))
        title.pack(pady=20)

        subtitle = ctk.CTkLabel(self.root, text="Select a Quiz", font=("Arial", 16))
        subtitle.pack(pady=10)

        for quiz_title in self.quiz_data:
            btn = ctk.CTkButton(self.root, text=quiz_title, command=lambda qt=quiz_title: self.start_quiz(qt))
            btn.pack(pady=5)

        ctk.CTkButton(self.root, text="🎲 Random Quiz", command=self.start_random_quiz).pack(pady=15)

    def start_quiz(self, title):
        self.selected_quiz = self.quiz_data[title]
        self.current_title = title
        self.question_index = 0
        self.score = 0
        self.user_answers = []
        self.show_question()

    def start_random_quiz(self):
        title = random.choice(list(self.quiz_data.keys()))
        self.start_quiz(title)

    def show_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.question_index >= len(self.selected_quiz):
            self.show_result()
            return

        question = self.selected_quiz[self.question_index]
        q_text = question["question"]
        options = question["options"]

        ctk.CTkLabel(self.root, text=f"{self.current_title} - Question {self.question_index+1}/{len(self.selected_quiz)}", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(self.root, text=q_text, font=("Arial", 18), wraplength=500).pack(pady=20)

        self.selected_option = ctk.StringVar()

        for opt in options:
            btn = ctk.CTkRadioButton(self.root, text=opt, variable=self.selected_option, value=opt)
            btn.pack(anchor="w", padx=80, pady=5)

        ctk.CTkButton(self.root, text="Submit Answer", command=self.check_answer).pack(pady=20)

    def check_answer(self):
        selected = self.selected_option.get()
        if not selected:
            messagebox.showwarning("No selection", "Please select an option.")
            return

        correct = self.selected_quiz[self.question_index]["answer"]
        if selected == correct:
            self.score += 1
            feedback = "✅ Correct!"
        else:
            feedback = f"❌ Incorrect! Correct: {correct}"

        self.user_answers.append({"question": self.selected_quiz[self.question_index]["question"],
                                  "your_answer": selected, "correct_answer": correct})

        self.question_index += 1

        messagebox.showinfo("Feedback", feedback)
        self.show_question()

    def show_result(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.root, text="📊 Quiz Result", font=("Arial", 22)).pack(pady=20)
        ctk.CTkLabel(self.root, text=f"Your Score: {self.score} / {len(self.selected_quiz)}", font=("Arial", 18)).pack(pady=10)

        result_frame = ctk.CTkScrollableFrame(self.root, width=500, height=250)
        result_frame.pack(pady=15)

        for qa in self.user_answers:
            q_label = ctk.CTkLabel(result_frame, text=f"Q: {qa['question']}\nYour Answer: {qa['your_answer']}\nCorrect Answer: {qa['correct_answer']}", anchor="w", justify="left", wraplength=480)
            q_label.pack(pady=5)

        ctk.CTkButton(self.root, text="🏠 Home", command=self.main_menu).pack(pady=20)

if __name__ == "__main__":
    root = ctk.CTk()
    app = QuizApp(root)
    root.mainloop()
# This code implements a quiz application using customtkinter. It allows users to select quizzes, answer questions, and view results.
# The quizzes are loaded from a JSON file, and users can also take a random quiz.   
# Ensure you have the required files (quizzes.json) in the same directory as this script.
# You can add more quizzes by updating the `quizzes.json` file with new questions and
# options.
# The application features a user-friendly interface with buttons for navigation and feedback on answers.
# Ensure you have the required files (quizzes.json) in the same directory as this script.
# You can run this script to launch the application.
# You can add more quizzes by updating the `quizzes.json` file with new questions and   
# options.

