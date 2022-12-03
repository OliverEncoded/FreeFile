import sys
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import threading
import socketConnection


window = tk.Tk()
window.title("Free File")
window.geometry("180x85")
window.maxsize(180,85)
window.minsize(180,85)

window.attributes('-topmost',True)

running = False

def sendFile():
    if not running:
        t = threading.Thread(target=sendFile_thread, daemon=True)
        t.start()
def sendFile_thread():
    global running
    running = True

    file_path = filedialog.askopenfilename()
    print(file_path)
    code = socketConnection.sndFile(file_path, pb = progressBar, lb = label)
    progressBar['value'] = 0
    entry.delete(0, tk.END)
    entry.insert(0, code)

    running = False

def rcvFile():
    global running
    if not running:
        t = threading.Thread(target=rcvFile_thread, daemon=True)
        t.start()
def rcvFile_thread():
    global running
    running = True

    code = entry.get()
    file_name = socketConnection.getFileName(code)
    if file_name == -1 or file_name == -2 or file_name == -3:
        entry['bg'] = "red"
        time.sleep(0.1)
        entry['bg'] = "cornsilk3"
        time.sleep(0.1)
        entry['bg'] = "red"
        time.sleep(0.1)
        entry['bg'] = "cornsilk3"
        running = False
        return

    whole_file_path = filedialog.asksaveasfile(initialfile=file_name)

    file_path = os.path.dirname(whole_file_path.name)
    file_name = os.path.basename(whole_file_path.name)

    socketConnection.rcvFile(code, file_path, file_name, pb = progressBar, lb = label)
    progressBar['value'] = 0

    running = False

def cancel():
    global running
    if running:
        running = False
        sys.exit()

codeLabel = tk.Label(
    text = "Code:",
    fg="Black")
codeLabel.place(x=5,y=5)

entry = tk.Entry(
    fg="black",
    bg="cornsilk3",
    width=12)
entry.place(x=50,y=5)

sendButton = tk.Button(
    text="Upload",
    bg="white",
    fg="black",
    width=3,
    command=sendFile)
sendButton.place(x=0, y=35)

getButton = tk.Button(
    text="Download",
    bg="white",
    fg="black",
    width=4,
    command=rcvFile)
getButton.place(x=60,y=35)

cancelButton = tk.Button(
    text="Stop",
    bg="white",
    fg="black",
    width=2,
    command=cancel)
cancelButton.place(x=128, y=35)

label = tk.Label(
    text = "0%",
    fg="Black")
label.place(x=5,y=62)
#label.grid(column=0,row=2, columnspan=1)

progressBar = ttk.Progressbar(
    orient='horizontal',
    mode='determinate',
    length=110,
maximum=100)
progressBar.place(x=50,y=65)
#progressBar.grid(column=1,row=2,columnspan=1)

window.mainloop()