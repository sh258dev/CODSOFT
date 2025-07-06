#Requirements (Install these first)
# Required Installation (Run this first in terminal):
# pip install customtkinter playsound
# If you don't have customtkinter or playsound installed, run the
# following command in your terminal:
# python -m pip install --upgrade pip
# or
# pip install --upgrade pip 
# pip install customtkinter playsound
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import threading
import time
import json
import os
from playsound import playsound

ALARM_FILE = "alarms.json"
DEFAULT_TONE = "tone1.mp3"  # Add tone1.mp3, tone2.mp3 etc. in the same directory

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("⏰ Alarm Clock App")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.alarms = self.load_alarms()
        self.active_threads = []

        self.setup_ui()
        self.update_clock()
        self.check_alarms_loop()

    def setup_ui(self):
        self.time_label = ctk.CTkLabel(self.root, text="", font=("DS-Digital", 40))
        self.time_label.pack(pady=20)

        # Add Alarm Section
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10)

        self.hour = ctk.CTkEntry(frame, width=50, placeholder_text="HH")
        self.minute = ctk.CTkEntry(frame, width=50, placeholder_text="MM")
        self.ampm = ctk.CTkOptionMenu(frame, values=["AM", "PM"])
        self.ampm.set("AM")
        self.tone = ctk.CTkOptionMenu(frame, values=["tone1.mp3", "tone2.mp3"])
        self.tone.set(DEFAULT_TONE)

        self.hour.grid(row=0, column=0, padx=5)
        self.minute.grid(row=0, column=1, padx=5)
        self.ampm.grid(row=0, column=2, padx=5)
        self.tone.grid(row=0, column=3, padx=5)

        ctk.CTkButton(frame, text="➕ Set Alarm", command=self.set_alarm).grid(row=0, column=4, padx=5)

        # Alarms List
        self.alarm_list_frame = ctk.CTkScrollableFrame(self.root, width=450, height=250)
        self.alarm_list_frame.pack(pady=20)
        self.refresh_alarm_list()

    def update_clock(self):
        now = datetime.now().strftime("%I:%M:%S %p\n%A, %d %B %Y")
        self.time_label.configure(text=now)
        self.root.after(1000, self.update_clock)

    def set_alarm(self):
        h = self.hour.get().zfill(2)
        m = self.minute.get().zfill(2)
        ampm = self.ampm.get()
        tone = self.tone.get()

        if not (h.isdigit() and m.isdigit()):
            messagebox.showerror("Invalid Input", "Please enter valid time.")
            return

        alarm_time = f"{h}:{m} {ampm}"
        self.alarms.append({"time": alarm_time, "tone": tone, "active": True})
        self.save_alarms()
        self.refresh_alarm_list()

    def refresh_alarm_list(self):
        for widget in self.alarm_list_frame.winfo_children():
            widget.destroy()

        for index, alarm in enumerate(self.alarms):
            text = f"{alarm['time']} ({alarm['tone']})"
            switch = ctk.CTkSwitch(self.alarm_list_frame, text=text, command=lambda i=index: self.toggle_alarm(i))
            switch.select() if alarm['active'] else switch.deselect()
            switch.pack(pady=5)

    def toggle_alarm(self, index):
        self.alarms[index]['active'] = not self.alarms[index]['active']
        self.save_alarms()

    def save_alarms(self):
        with open(ALARM_FILE, "w") as f:
            json.dump(self.alarms, f, indent=2)

    def load_alarms(self):
        if os.path.exists(ALARM_FILE):
            with open(ALARM_FILE, "r") as f:
                return json.load(f)
        return []

    def check_alarms_loop(self):
        def check():
            while True:
                now = datetime.now().strftime("%I:%M %p")
                for alarm in self.alarms:
                    if alarm["time"] == now and alarm["active"]:
                        alarm["active"] = False  # Auto-disable
                        self.save_alarms()
                        threading.Thread(target=self.ring_alarm, args=(alarm["tone"],)).start()
                time.sleep(30)

        thread = threading.Thread(target=check, daemon=True)
        thread.start()

    def ring_alarm(self, tone):
        popup = ctk.CTkToplevel(self.root)
        popup.geometry("300x180")
        popup.title("🔔 Alarm!")

        label = ctk.CTkLabel(popup, text="⏰ Wake up!", font=("Arial", 20))
        label.pack(pady=15)

        btn_frame = ctk.CTkFrame(popup)
        btn_frame.pack(pady=10)

        def dismiss():
            popup.destroy()

        def snooze():
            new_time = (datetime.now() + timedelta(minutes=5)).strftime("%I:%M %p")
            self.alarms.append({"time": new_time, "tone": tone, "active": True})
            self.save_alarms()
            self.refresh_alarm_list()
            popup.destroy()

        ctk.CTkButton(btn_frame, text="Dismiss", command=dismiss).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="Snooze 5 min", command=snooze).grid(row=0, column=1, padx=10)

        try:
            playsound(tone)
        except Exception as e:
            messagebox.showerror("Sound Error", f"Failed to play tone: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = AlarmClock(root)
    root.mainloop()
# This code implements a simple alarm clock application using customtkinter.
# It allows users to set alarms with a specific time and tone, view active alarms, and manage them.
# The application also features a real-time clock display and plays the selected tone when an alarm goes