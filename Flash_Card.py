from tkinter import *
import random
import csv
import os
import sys

flip_timer = None
BACKGROUND_COLOR = "#B1DDC6"
# ---------------------------- DATA SETUP ------------------------------- #
def resource_path(relative_path):
    """Returns the absolute path to a resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def load_words():
    base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    words_to_learn_path = os.path.join(base_dir, "words_to_learn.csv")
    german_words_path = resource_path("data/german_words.csv")
    try:
        with open(words_to_learn_path, mode="r") as file:
            # create a list from each row
            reader = csv.reader(file)
            return [(row[0], row[1]) for row in reader]
    except FileNotFoundError:
        with open(german_words_path) as file:
            reader = csv.reader(file)
            # jump from first line(header)
            next(reader)
            return [(row[0], row[1]) for row in reader] # create a tuple from english and german word

german_word_list = load_words()
random_de_word, random_en_word = random.choice(german_word_list)
#lenght of total words
total_words = len(german_word_list)
# ---------------------------- FUNCTIONS ------------------------------- #
def save_words():
    # ذخیره در کنار فایل exe یا Flash_Card.py
    base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    words_to_learn_path = os.path.join(base_dir, "words_to_learn.csv")
    with open(words_to_learn_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(german_word_list)

def save_and_close():
    save_words()  # save words
    window.destroy()  # close window

def next_card():
    global random_de_word, random_en_word, flip_timer

    if flip_timer:
        window.after_cancel(flip_timer)

    if not german_word_list:
        canvas.itemconfig(card_title, text="Done!", fill="black")
        canvas.itemconfig(card_word, text="You've learned all words 🎉", fill="black")
        status_text.config(text="🎉 100% Completed")
        return

    random_de_word, random_en_word = random.choice(german_word_list)
    canvas.itemconfig(card_title, text="German", fill="black")
    canvas.itemconfig(card_word, text=random_de_word, fill="black")
    canvas.itemconfig(card_front_img_on_canvas, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

    # درصد پیشرفت
    learned_count = total_words - len(german_word_list)
    progress_percent = int((learned_count / total_words) * 100)
    status_text.config(text=f"Words Remaining: {len(german_word_list)} / {total_words}  |  ✅ {progress_percent}% Learned")

def flip_card():
    canvas.itemconfig(card_title, text="English",fill="white")
    canvas.itemconfig(card_word, text=random_en_word,fill="white")
    canvas.itemconfig(card_front_img_on_canvas, image=card_back_img)

def is_known():
    global random_de_word, random_en_word, german_word_list
    german_word_list.remove((random_de_word, random_en_word))  # حذف کلمه از لیست
    save_words()  # ذخیره‌سازی داده‌ها بعد از حذف کلمه
    next_card()  # نمایش کارت بعدی

def reset_words():
    global german_word_list, total_words
    base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    words_to_learn_path = os.path.join(base_dir, "words_to_learn.csv")
    # اگر فایل وجود داشت، حذفش کن
    if os.path.exists(words_to_learn_path):
        os.remove(words_to_learn_path)
        
    german_word_list = load_words()
    total_words = len(german_word_list)
    next_card()

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Word Wizard 🧙‍♂️")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# create canvas

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=40, pady=20)

# create front image
card_front_img = PhotoImage(file=resource_path("images/card_front.png"))
card_back_img = PhotoImage(file=resource_path("images/card_back.png"))
card_front_img_on_canvas = canvas.create_image(400,263,image=card_front_img)


#create text in canvas
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 36, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 48, "bold"))


# unknown button
unknown_button_img = PhotoImage(file=resource_path("images/wrong.png"))
unknown_button = Button(window, image=unknown_button_img, command=next_card,
                        bg=BACKGROUND_COLOR, highlightthickness=0)


# known button
known_button_img = PhotoImage(file=resource_path("images/right.png"))
known_button = Button(window, image=known_button_img, command=is_known,
                      bg=BACKGROUND_COLOR, highlightthickness=0)


# متن وضعیت پایین کارت
status_text = Label(window, text="", bg=BACKGROUND_COLOR, font=("Ariel", 16, "bold"))
status_text.grid(row=2, column=0, columnspan=2)

restart_button = Button(window, text="🔄 Restart", font=("Ariel", 14, "bold"),
                        command=reset_words, bg="#AED9E0")

# دکمه‌ها در یک ردیف با فاصله، وسط‌چین
button_frame = Frame(window, bg=BACKGROUND_COLOR)
button_frame.grid(row=1, column=0, columnspan=2, pady=10)

unknown_button = Button(button_frame, image=unknown_button_img, command=next_card,
                        bg=BACKGROUND_COLOR, highlightthickness=0)
unknown_button.grid(row=0, column=0, padx=10)

restart_button = Button(button_frame, text="🔄 Restart", font=("Ariel", 12, "bold"),
                        command=reset_words, bg="#AED9E0")
restart_button.grid(row=0, column=1, padx=10)

known_button = Button(button_frame, image=known_button_img, command=is_known,
                      bg=BACKGROUND_COLOR, highlightthickness=0)
known_button.grid(row=0, column=2, padx=10)

# اندازه حداقلی برای پنجره
window.minsize(900, 600)

# تنظیم تایمر اولیه
flip_timer = window.after(3000, func=flip_card)

# ---------------------------- EVENT HANDLING ------------------------------- #

# Add event for window closing
window.protocol("WM_DELETE_WINDOW", save_and_close)

next_card()

window.mainloop()