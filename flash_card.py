from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("data/not_learnt_yet.csv")
except (FileNotFoundError, pandas.errors.EmptyDataError):
    data = pandas.read_csv("data/eng_to_urdu.csv")
words_data_list = data.to_dict(orient="records")
urdu_word = ""
english_word = ""
learned_data_list = []

def remember():
    learnt = {"English": english_word, "Urdu": urdu_word}
    words_data_list.remove(learnt)
    d_frame = pandas.DataFrame(words_data_list)
    d_frame.to_csv("data/not_learnt_yet.csv", index=False)

    global learned_data_list
    try:
        learned_data = pandas.read_csv("data/learned_sentences.csv")
    except (FileNotFoundError, pandas.errors.EmptyDataError):
        learned_data = pandas.DataFrame(columns=["English", "Urdu"])
        learned_data.to_csv("data/learned_sentences.csv", index=False)
    learned_data_list = learned_data.to_dict(orient="records")
    learned_data_list.append(learnt)
    data_frame = pandas.DataFrame(learned_data_list)
    data_frame.to_csv("data/learned_sentences.csv", index=False)

    get_next_card()

def not_remember():
    get_next_card()

def get_next_card():
    global urdu_word, english_word
    word = random.choice(words_data_list)
    english_word = word["English"]
    urdu_word = word["Urdu"]

    if len(english_word) > 20:
        canvas.itemconfig(canvas_word, font=("Arial", 40, "bold"))
    else:
        canvas.itemconfig(canvas_word, font=("Arial", 50, "bold"))
    canvas.itemconfig(canvas_title, text="English", fill="black")
    canvas.itemconfig(canvas_word, text=english_word, fill="black")
    canvas.itemconfig(new_image, image=front_card)

    right_button.config(state="disabled")
    wrong_button.config(state="disabled")
    window.after(3000, func=flip_card)

def flip_card():
    right_button.config(state="normal")
    wrong_button.config(state="normal")
    canvas.itemconfig(canvas_title, text="Urdu", fill="white")
    canvas.itemconfig(canvas_word, text=urdu_word.split(" ")[::-1], fill="white")
    canvas.itemconfig(new_image, image=back_card)


window = Tk()
window.title("Flash Card App")
window.config(padx=100, pady=80, bg=BACKGROUND_COLOR)
canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
front_card = PhotoImage(file='images/card_front.png')
back_card = PhotoImage(file='images/card_back.png')   # canvas image can't be created in function
new_image = canvas.create_image(400, 263, image=front_card)
canvas_title = canvas.create_text(400, 200, text="English", font=("Arial", 36, "italic"))
canvas_word = canvas.create_text(400, 300, text="AB", font=("Arial", 50, "bold"))
canvas.grid(row=0, column=0, columnspan=2)
window.after(3000, func=flip_card)

# Create right wrong button images
cross_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=cross_image, highlightthickness=0, borderwidth=0, command=not_remember)
wrong_button.grid(row=1, column=0, pady=20)
tick_image = PhotoImage(file="images/right.png")
right_button = Button(image=tick_image, highlightthickness=0, borderwidth=0, command=remember)
right_button.grid(row=1, column=1, pady=20)
get_next_card()
window.mainloop()
