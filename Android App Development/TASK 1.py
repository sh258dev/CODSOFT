import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.tasks = []

        self.setup_ui()
        self.load_tasks()

    def setup_ui(self):
        # Input Fields
        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.grid(row=0, column=0, padx=10, pady=5)

        self.priority_var = tk.StringVar()
        self.priority_menu = ttk.Combobox(self.root, textvariable=self.priority_var, values=["High", "Medium", "Low"])
        self.priority_menu.set("Medium")
        self.priority_menu.grid(row=0, column=1)

        self.date_entry = tk.Entry(self.root, width=15)
        self.date_entry.insert(0, "YYYY-MM-DD")
        self.date_entry.grid(row=0, column=2)

        tk.Button(self.root, text="Add Task", command=self.add_task).grid(row=0, column=3, padx=10)

        # Task List
        self.tree = ttk.Treeview(self.root, columns=("Priority", "Due", "Status"), show='headings')
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due", text="Due Date")
        self.tree.heading("Status", text="Status")
        self.tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Buttons
        tk.Button(self.root, text="Edit Task", command=self.edit_task).grid(row=2, column=0)
        tk.Button(self.root, text="Mark Complete", command=self.mark_complete).grid(row=2, column=1)
        tk.Button(self.root, text="Delete Task", command=self.delete_task).grid(row=2, column=2)

    def add_task(self):
        title = self.task_entry.get()
        priority = self.priority_var.get()
        due_date = self.date_entry.get()

        if not title.strip():
            messagebox.showwarning("Input Error", "Task title is required.")
            return

        try:
            if due_date != "YYYY-MM-DD":
                datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Date Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        task = {
            "title": title,
            "priority": priority,
            "due_date": due_date if due_date != "YYYY-MM-DD" else "",
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_task_list()

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            return

        index = self.tree.index(selected[0])
        task = self.tasks[index]

        new_title = simpledialog.askstring("Edit Task", "New title:", initialvalue=task["title"])
        if new_title:
            task["title"] = new_title
            self.save_tasks()
            self.refresh_task_list()

    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            return

        index = self.tree.index(selected[0])
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.save_tasks()
        self.refresh_task_list()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            return

        index = self.tree.index(selected[0])
        del self.tasks[index]
        self.save_tasks()
        self.refresh_task_list()

    def refresh_task_list(self):
        self.tree.delete(*self.tree.get_children())
        for task in self.tasks:
            status = "✔️ Done" if task["completed"] else "❌ Active"
            self.tree.insert("", "end", values=(task["priority"], task["due_date"], status))

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                self.tasks = json.load(f)
            self.refresh_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
