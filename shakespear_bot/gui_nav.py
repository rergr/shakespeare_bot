import tkinter as tk
from tkinter import *
from consts import SP_DIR, SP_GIF_DIR, ONE_STEP_DIR, LOGSH_DIR, LOG_DIR
import tensorflow as tf

# loads the one step model
one_step_reloaded = tf.saved_model.load(ONE_STEP_DIR)
padding = 5

root = tk.Tk()
root.option_add('*Font', 'Helvetica 15')
root.title('Shakespeare Bot')
root.geometry("1100x700")
icon = PhotoImage(file=SP_DIR)
root.iconphoto(False, icon)
root['background'] = '#dbe9ef'


def generate_text():
    outputfield.delete("1.0", "end")
    outputfield.insert(tk.END, "Loading...\n")
    outputfield.see(tk.END)
    outputfield.update()
    states = None
    input = inputfield.get()
    text_range = int(rangefield.get())
    if not isinstance(text_range, int):
        outputfield.insert(tk.END, "Please enter a number for the range field\n")
        return

    next_char = tf.constant([input])
    result = [next_char]

    # text is generate
    for n in range(text_range):
        next_char, states = one_step_reloaded.generate_one_step(next_char, states=states)
        result.append(next_char)

    # text is saved in logs and read to give the effect of live generation
    written_txt = tf.strings.join(result)[0].numpy().decode("utf-8")

    with open(LOG_DIR, 'w') as log:
        log.write(written_txt)

    outputfield.delete("1.0", "end")

    with open(LOG_DIR, 'r') as log:
        for line in log:
            line = line.strip()
            outputfield.insert(tk.END, line + '\n')
            outputfield.see(tk.END)
            outputfield.update()
            outputfield.after(100)

    # all text is saved in a log history file logsh
    with open(LOGSH_DIR, 'a') as logsh:
        logsh.write(written_txt)


frames = [tk.PhotoImage(file=SP_GIF_DIR, format=f'gif -index {i}') for i in range(12)]


# plays the gif
def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == 12:
        ind = 0
    button1.configure(image=frame)
    root.after(100, update, ind)


root.after(0, update, 0)

# gui structure
root.columnconfigure(0, weight=1, uniform="group1")
root.columnconfigure(1, weight=1, uniform="group1")
root.columnconfigure(2, weight=1, uniform="group1")

root.rowconfigure(0, weight=3)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

button1 = tk.Button(root, command=generate_text, bg='#dbe9ef', highlightthickness=0, bd=0)
button1.grid(column=0, row=0, rowspan=3, stick=tk.W + tk.N + tk.NS, padx=padding, pady=padding)

inputfield = tk.Entry(root, highlightthickness=0, bd=0)
inputfield.grid(column=1, row=2, columnspan=2, stick=tk.EW + tk.NS, padx=padding, pady=padding)
inputfield.insert(0, 'input')
inputfield.bind("<FocusIn>", lambda args: inputfield.delete('0', 'end'))

rangefield = tk.Entry(root, highlightthickness=0, bd=0)
rangefield.grid(column=1, row=1, columnspan=2, stick=tk.S, padx=padding, pady=padding)
rangefield.insert(0, 'range')
rangefield.bind("<FocusIn>", lambda args: rangefield.delete('0', 'end'))

outputfield = tk.Text(root, highlightthickness=0, bd=0)
outputfield.grid(column=1, row=0, columnspan=2, stick=tk.NE + tk.EW + tk.NS, padx=padding, pady=padding)

root.mainloop()
