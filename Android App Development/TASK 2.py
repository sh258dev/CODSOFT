#Required Installation (Run this first in terminal):
# pip install customtkinter requests pyperclip
# If you don't have customtkinter, requests, or pyperclip installed, run the
# following command in your terminal:
# pip install customtkinter requests pyperclip
import customtkinter as ctk
import tkinter.messagebox as mb
from tkinter import Toplevel, Text
import random
import datetime
import json
import os
import requests
import pyperclip
import webbrowser

QUOTES_FILE = "quotes.json"
FAVORITES_FILE = "favorites.json"
LAST_QUOTE_FILE = "last_quote.json"

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Quote of the Day")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.quotes = self.load_local_quotes()
        self.favorites = self.load_favorites()
        self.current_quote = ""

        self.setup_ui()
        self.load_daily_quote()
        self.schedule_refresh()

    def setup_ui(self):
        self.quote_label = ctk.CTkLabel(self.root, text="", wraplength=550, font=("Arial", 16), justify="center")
        self.quote_label.pack(pady=30)

        btn_frame = ctk.CTkFrame(self.root)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="🌅 New Quote", command=self.new_quote).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="💾 Save Favorite", command=self.save_favorite).grid(row=0, column=1, padx=10)
        ctk.CTkButton(btn_frame, text="📋 Copy Quote", command=self.copy_to_clipboard).grid(row=0, column=2, padx=10)
        ctk.CTkButton(btn_frame, text="⭐ Favorites", command=self.show_favorites).grid(row=0, column=3, padx=10)

        share_frame = ctk.CTkFrame(self.root)
        share_frame.pack(pady=10)

        ctk.CTkButton(share_frame, text="🐦 Share to Twitter", command=self.share_to_twitter).grid(row=0, column=0, padx=10)
        ctk.CTkButton(share_frame, text="📱 Share to WhatsApp", command=self.share_to_whatsapp).grid(row=0, column=1, padx=10)

    def load_local_quotes(self):
        if os.path.exists(QUOTES_FILE):
            with open(QUOTES_FILE, "r") as f:
                return json.load(f)
        return ["Stay motivated!", "Keep going!"]

    def load_favorites(self):
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, "r") as f:
                return json.load(f)
        return []

    def save_favorite(self):
        if self.current_quote and self.current_quote not in self.favorites:
            self.favorites.append(self.current_quote)
            with open(FAVORITES_FILE, "w") as f:
                json.dump(self.favorites, f, indent=2)
            mb.showinfo("Saved", "Quote saved to favorites!")
        else:
            mb.showwarning("Warning", "Already in favorites or empty.")

    def copy_to_clipboard(self):
        if self.current_quote:
            pyperclip.copy(self.current_quote)
            mb.showinfo("Copied", "Quote copied to clipboard!")

    def show_favorites(self):
        top = Toplevel(self.root)
        top.title("⭐ Favorite Quotes")
        top.geometry("500x400")
        text = Text(top, wrap="word", font=("Arial", 12))
        text.pack(expand=True, fill="both")
        text.insert("end", "\n\n".join(self.favorites))
        text.config(state="disabled")

    def new_quote(self):
        try:
            quote = self.fetch_online_quote()
        except:
            quote = random.choice(self.quotes)
        self.current_quote = quote
        self.quote_label.configure(text=self.current_quote)
        self.save_last_quote()

    def fetch_online_quote(self):
        url = "https://zenquotes.io/api/random"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()[0]
            return f"{data['q']} – {data['a']}"
        raise Exception("API failed")

    def save_last_quote(self):
        today = str(datetime.date.today())
        with open(LAST_QUOTE_FILE, "w") as f:
            json.dump({"date": today, "quote": self.current_quote}, f)

    def load_daily_quote(self):
        today = str(datetime.date.today())
        if os.path.exists(LAST_QUOTE_FILE):
            with open(LAST_QUOTE_FILE, "r") as f:
                data = json.load(f)
                if data["date"] == today:
                    self.current_quote = data["quote"]
                    self.quote_label.configure(text=self.current_quote)
                    return
        self.new_quote()

    def schedule_refresh(self):
        now = datetime.datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        delay_ms = int((midnight - now).total_seconds() * 1000)
        self.root.after(delay_ms, self.new_quote)

    def share_to_twitter(self):
        if self.current_quote:
            text = self.current_quote.replace(" ", "%20")
            url = f"https://twitter.com/intent/tweet?text={text}"
            webbrowser.open(url)

    def share_to_whatsapp(self):
        if self.current_quote:
            text = self.current_quote.replace(" ", "%20")
            url = f"https://api.whatsapp.com/send?text={text}"
            webbrowser.open(url)

if __name__ == "__main__":
    root = ctk.CTk()
    app = QuoteApp(root)
    root.mainloop()
# This code is a simple quote application that fetches quotes from an online API, allows users to save favorites, copy quotes, and share them on social media platforms.
# It uses customtkinter for the GUI and supports features like daily quote refresh, favorites management, and sharing options.

