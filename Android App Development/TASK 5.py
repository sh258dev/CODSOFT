#Required Packages
#Install required packages before running:
# Required Installation (Run this first in terminal):
# pip install customtkinter sqlite3
# If you don't have customtkinter or sqlite3 installed, run the
# following command in your terminal:
# python -m pip install --upgrade pip
# or
# pip install --upgrade pip
# This code implements a simple university attendance application using customtkinter and SQLite.
# It allows students to mark attendance for courses and instructors to manage courses and view attendance records.
# The application features a login system for both students and instructors, with registration functionality.
# The UI includes buttons for navigation, input fields for course management, and attendance marking.
import customtkinter as ctk
import sqlite3
from tkinter import messagebox

DB_NAME = "university.db"

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x400")
        self.root.title("🎓 University Attendance App")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.init_db()
        self.user_role = None
        self.user_id = None

        self.login_screen()

    # ---------------- DATABASE ----------------
    def init_db(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT CHECK(role IN ('student', 'instructor'))
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                instructor_id INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                date TEXT
            )
        """)
        conn.commit()
        conn.close()

    def execute(self, query, params=(), fetch=False):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        data = cursor.fetchall() if fetch else None
        conn.close()
        return data

    # ---------------- LOGIN & REGISTRATION ----------------
    def login_screen(self):
        self.clear_screen()

        ctk.CTkLabel(self.root, text="🎓 Login", font=("Arial", 24)).pack(pady=20)

        self.username = ctk.CTkEntry(self.root, placeholder_text="Username")
        self.username.pack(pady=5)

        self.password = ctk.CTkEntry(self.root, placeholder_text="Password", show="*")
        self.password.pack(pady=5)

        self.role = ctk.CTkOptionMenu(self.root, values=["student", "instructor"])
        self.role.set("student")
        self.role.pack(pady=5)

        ctk.CTkButton(self.root, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(self.root, text="Register", command=self.register).pack()

    def login(self):
        uname = self.username.get().strip()
        pwd = self.password.get().strip()
        role = self.role.get()

        result = self.execute("SELECT id FROM users WHERE username=? AND password=? AND role=?", (uname, pwd, role), True)
        if result:
            self.user_id = result[0][0]
            self.user_role = role
            if role == "student":
                self.student_dashboard()
            else:
                self.instructor_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def register(self):
        uname = self.username.get().strip()
        pwd = self.password.get().strip()
        role = self.role.get()

        try:
            self.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (uname, pwd, role))
            messagebox.showinfo("Success", "Registered successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

    # ---------------- STUDENT PANEL ----------------
    def student_dashboard(self):
        self.clear_screen()
        ctk.CTkLabel(self.root, text="📚 Student Dashboard", font=("Arial", 20)).pack(pady=10)

        courses = self.execute("SELECT id, name FROM courses", fetch=True)
        for cid, cname in courses:
            btn = ctk.CTkButton(self.root, text=cname, command=lambda c=cid: self.mark_attendance(c))
            btn.pack(pady=5)

        ctk.CTkButton(self.root, text="🔙 Logout", command=self.login_screen).pack(pady=20)

    def mark_attendance(self, course_id):
        from datetime import date
        today = str(date.today())

        # Check if already marked
        check = self.execute("SELECT * FROM attendance WHERE student_id=? AND course_id=? AND date=?", 
                             (self.user_id, course_id, today), fetch=True)
        if check:
            messagebox.showinfo("Already Marked", "You have already marked attendance today.")
        else:
            self.execute("INSERT INTO attendance (student_id, course_id, date) VALUES (?, ?, ?)", 
                         (self.user_id, course_id, today))
            messagebox.showinfo("Success", "Attendance marked!")

    # ---------------- INSTRUCTOR PANEL ----------------
    def instructor_dashboard(self):
        self.clear_screen()
        ctk.CTkLabel(self.root, text="👨‍🏫 Instructor Dashboard", font=("Arial", 20)).pack(pady=10)

        self.course_name = ctk.CTkEntry(self.root, placeholder_text="New Course Name")
        self.course_name.pack(pady=5)

        ctk.CTkButton(self.root, text="➕ Add Course", command=self.add_course).pack(pady=5)

        courses = self.execute("SELECT id, name FROM courses WHERE instructor_id=?", (self.user_id,), fetch=True)
        for cid, cname in courses:
            btn = ctk.CTkButton(self.root, text=f"📖 {cname}", command=lambda c=cid: self.view_attendance(c))
            btn.pack(pady=5)

        ctk.CTkButton(self.root, text="🔙 Logout", command=self.login_screen).pack(pady=20)

    def add_course(self):
        name = self.course_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Course name cannot be empty.")
            return
        self.execute("INSERT INTO courses (name, instructor_id) VALUES (?, ?)", (name, self.user_id))
        messagebox.showinfo("Success", "Course added!")
        self.instructor_dashboard()

    def view_attendance(self, course_id):
        self.clear_screen()

        ctk.CTkLabel(self.root, text="📊 Attendance Report", font=("Arial", 18)).pack(pady=10)
        results = self.execute("""
            SELECT u.username, a.date FROM attendance a
            JOIN users u ON u.id = a.student_id
            WHERE a.course_id=?
            ORDER BY a.date DESC
        """, (course_id,), fetch=True)

        if not results:
            ctk.CTkLabel(self.root, text="No attendance records yet.").pack(pady=10)
        else:
            for uname, adate in results:
                ctk.CTkLabel(self.root, text=f"{uname} - {adate}").pack()

        ctk.CTkButton(self.root, text="🔙 Back", command=self.instructor_dashboard).pack(pady=20)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = ctk.CTk()
    app = AttendanceApp(root)
    root.mainloop()
# This code implements a simple university attendance application using customtkinter and SQLite.
# It allows students to mark attendance for courses and instructors to manage courses and view attendance records.
# The application features a login system for both students and instructors, with registration functionality.
# The UI includes buttons for navigation, input fields for course management, and attendance marking.
# Ensure you have the required packages installed before running this script.
# Required Installation (Run this first in terminal):
# pip install customtkinter sqlite3
# If you don't have customtkinter or sqlite3 installed, run the
# following command in your terminal:
# python -m pip install --upgrade pip
# or
# pip install --upgrade pip
# You can run this script to launch the application.
# Ensure you have the required database file (university.db) in the same directory as this script.
# The application will create the database and tables if they do not exist.
# You can add more courses and users by using the registration and course management features.
# Ensure you have the required database file (university.db) in the same directory as this script.
# The application will create the database and tables if they do not exist.
# You can add more courses and users by using the registration and course management features.
# Ensure you have the required database file (university.db) in the same directory as this script.
# The application will create the database and tables if they do not exist.

