from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"

# languages_dict = {
#     "french": "data/french_words.csv",
#     "japanese": "data/japanese_words.csv",
#     "spanish": "data/spanish_words.csv"
# }

try:
    data = pandas.read_csv("data/words_to_learn.csv")
    to_learn = data.to_dict(orient="records")

except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
    to_learn = data.to_dict(orient="records")


# def input_window():
#
#     input = Tk()
#     input.title("Language?")
#     input.config(padx=50, pady=50)
#     input_canvas = Canvas(width=200, height=200)
#     input_canvas.grid()
#     input_entry = Entry()
#     input_entry.grid(column=0, row=1)
#     input.mainloop()


def next_card():

    global english_word, flip_timer, word_pair

    window.after_cancel(flip_timer)
    canvas.itemconfig(card, image=card_front)
    word_pair = random.choice(to_learn)
    french_word = word_pair["French"]
    english_word = word_pair["English"]
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=f"{french_word}", fill="black")
    canvas.update()
    flip_timer = window.after(3000, func=show_answer)


def show_answer():

    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=f"{english_word}", fill="white")


def is_known():

    to_learn.remove(word_pair)
    next_card()
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)

# input_window()


window = Tk()
window.title("Thunderclap and Flash Cards")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=show_answer)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text=f"Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text=f"Word", font=("Ariel", 60, "bold"))

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()
