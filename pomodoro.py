from tkinter import *
from pygame import mixer
import math
import webbrowser

# ----- CONSTANTS ----- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#7a9d54"
YELLOW = "#f7f5dd"
FONT_NAME = "Helvetica"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ----- TIMER RESET ----- #

def reset_timer():
    """Resets timer to 0"""
    window.after_cancel(timer)
    canvas.itemconfig(timer_txt, text="00:00")
    title_label.config(text="Timer")
    check_mark.config(text="")
    global reps
    reps = 0

# ----- TIMER MECHANISM ----- #

def start_timer():
    """Starts timer"""
    global reps
    reps += 1
    mixer.init()
    sound = mixer.Sound("audio.wav")
    sound.play()

    work_time = WORK_MIN * 60
    short_break_time = SHORT_BREAK_MIN * 60
    long_break_time = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_time)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_time)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_time)
        title_label.config(text="Work", fg=GREEN)

# ----- COUNTDOWN MECHANISM ----- #
def count_down(count):
    """Count down"""

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_txt, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        count = 0
        for _ in range(math.floor(reps/2)):
            count += 1
        if count == 1:
            check_mark.config(text=f"{count} SESSION COMPLETED", font=(FONT_NAME, 14, "bold"))
        else:
            check_mark.config(text=f"{count} SESSIONS COMPLETED", font=(FONT_NAME, 14, "bold"))


# ----- ABOUT LINK ----- #
def about():
    """About button"""
    webbrowser.open("https://en.wikipedia.org/wiki/Pomodoro_Technique")

# ----- UI SETUP ----- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=200, pady=100, bg=YELLOW)


title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_txt = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_btn = Button(text="Start", command=start_timer)
start_btn.grid(column=0, row=2)

reset_btn = Button(text="Reset", command=reset_timer)
reset_btn.grid(column=2, row=2)

about_btn = Button(text="About", command=about)
about_btn.grid(column=1, row=4)

check_mark = Label(fg=GREEN, bg=YELLOW)
check_mark.grid(column=1, row=3)



window.mainloop()