import random
import time
from datetime import datetime
import threading
from threading import Thread
import nltk
from nltk.corpus import wordnet
import customtkinter as ttk

ttk.set_appearance_mode("dark")
ttk.set_default_color_theme("dark-blue")

def get_words_from_synsets():
    nltk.download('wordnet')
    synsets = list(wordnet.all_synsets())
    words = set()

    for synset in synsets:
        for lemma in synset.lemmas():
            words.add(lemma.name().lower())

    words = [word.replace("_", " ") for word in words]

    with open("words.txt", "w") as f:
        f.write("\n".join(words))

    return


def get_sentence():
    try:
        with open("words.txt", "r") as f:
            words = f.read().splitlines()
    except FileNotFoundError:
        get_words_from_synsets()
        return get_sentence()
    else:
        return" ".join(random.choices(words, k=random.randint(1, 2)))

class App:
    def __init__(self, root):
        self.root = root
        self.frame = ttk.CTkFrame(root)
        self.frame.grid(row=0, column=0)
        self.running = False
        self.time_counter = 0
        self.speeds = []

        self.title_label = ttk.CTkLabel(master=self.frame, text="Speed Type", font=('Helvetica', 42, 'bold'))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # getting the typing text from random words of dictionary
        self.sentence = get_sentence()
        self.text_label = ttk.CTkLabel(master=self.frame, text=self.sentence, wraplength=1000, font=('Helvetica', 24))
        self.text_label.grid(row=1, column=0, columnspan=3, padx=10, pady=60)

        self.entry = ttk.CTkEntry(master=self.frame, width=800, font=('Helvetica', 18))
        self.entry.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.entry.bind("<KeyRelease>", self.start_app)
        self.entry.bind("<Return>", self.get_new_test)
        self.entry.focus()

        self.speed_label = ttk.CTkLabel(master=self.frame, text="Typing Speed:\n0.00 CPM\n0.00 WPM", font=('Helvetica', 24))
        self.speed_label.grid(row=3, column=0, padx=10, pady=10)

        self.reset_button = ttk.CTkButton(master=self.frame, text="Reset", command=self.reset, font=('Helvetica', 20))
        self.reset_button.grid(row=3, column=2, padx=10, pady=10)

        speed_history = self.get_speed_history()
        self.speed_history = ttk.CTkLabel(master=self.frame, text=speed_history, font=  ('Helvetica', 20))
        self.speed_history.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        

    def start_app(self, event):
        if not self.running and event.keycode not in [36, 15, 16, 17]:
            self.running = True
            self.thread = Thread(target=self.time_thread)
            self.thread.start()

        if not self.text_label.cget("text").startswith(self.entry.get()):
            self.entry.configure(text_color="red")
        else:
            self.entry.configure(text_color=("black", "white"))

        if self.entry.get() == self.text_label.cget("text"):
            self.entry.configure(text_color="green")
            self.running = False
        

    def reset(self):
        print("Resetting the app...")
        self.running = False
        if self.entry.get() == self.text_label.cget("text"):
            self.store_speed()
        self.entry.delete(0, ttk.END)
        self.text_label.configure(text=get_sentence())
        self.speed_label.configure(text="Typing Speed:\n0.00 CPM\n0.00 WPM")
        self.time_counter = 0

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.time_counter += 0.1
            try:
                self.cpm = (len(self.entry.get()) / self.time_counter) * 60
                self.wpm = (len(self.entry.get().split(" ")) / self.time_counter) * 60
            except ZeroDivisionError:
                continue
            self.speed_label.configure(text=f"Typing Speed:\n {self.cpm:0.02f} CPM\n{self.wpm:.02f} WPM")
        
        if not self.running and not len(self.entry.get()):
            self.speed_label.configure(text="Typing Speed:\n0.00 CPM\n0.00 WPM")
            self.time_counter = 0
    

    def get_new_test(self, event):
        if self.entry.get() == self.text_label.cget("text"):
            self.reset()
            
    def store_speed(self):
        speed = {"time": datetime.now().strftime("%H:%M:%S"), "cpm": self.cpm, "wpm": self.wpm}
        self.speeds.append(speed)
        self.speeds = sorted(self.speeds, key=lambda k: k["wpm"], reverse=True)
        self.speeds = self.speeds[:10]
        self.speed_history.configure(text="Top 10 Speeds\n" + self.get_speed_history())

    def get_speed_history(self):
        speed_history = ""
        for speed in self.speeds:
            speed_history += f"Time:{speed['time']}\t Speed:\t{speed['cpm']:0.02f} CPM \t {speed['wpm']:0.02f} WPM\n"
        
        return speed_history
    

    

def main():
    root = ttk.CTk()
    root.title("Speed Type")
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
