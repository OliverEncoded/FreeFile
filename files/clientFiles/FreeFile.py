import sys
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import threading
import socketConnection




def sendFile():
    global running, running_thread
    if not running:
        running_thread = threading.Thread(target=sendFile_thread, daemon=True)
        running_thread.start()
def sendFile_thread():
    global running, running_thread
    running = True

    file_path = filedialog.askopenfilename()
    print(file_path)
    code = socketConnection.sndFile(file_path, pb = progressBar, lb = label)
    entry.delete(0, tk.END)
    entry.insert(0, code)

    running = False

def rcvFile():
    global running, running_thread
    if not running:
        running_thread = threading.Thread(target=rcvFile_thread, daemon=True)
        running_thread.start()
def rcvFile_thread():
    global running, running_thread
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
    if not whole_file_path:
        running = False
        return

    file_path = os.path.dirname(whole_file_path.name)
    file_name = os.path.basename(whole_file_path.name)

    socketConnection.rcvFile(code, file_path, file_name, pb = progressBar, lb = label)

    running = False

def cancel():
    global running, running_thread, kill
    if running:
        sys.exit()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Free File")
    window.geometry("180x85")
    window.maxsize(180, 85)
    window.minsize(180, 85)

    window.attributes('-topmost', True)
    window.attributes('-toolwindow', True)

    running = False
    kill = False
    running_thread = -1


    codeLabel = tk.Label(
        text = "Code:",
        fg="Black")
    codeLabel.place(x=5,y=5)

    entry = tk.Entry(
        fg="black",
        bg="cornsilk3",
        width=18)
    entry.place(x=50,y=5)

    sendButton = tk.Button(
        text="Upload",
        bg="white",
        fg="black",
        command=sendFile)
    sendButton.place(x=5, y=30)

    getButton = tk.Button(
        text="Download",
        bg="white",
        fg="black",
        command=rcvFile)
    getButton.place(x=62,y=30)

    cancelButton = tk.Button(
        text="Stop",
        bg="white",
        fg="black",
        command=cancel)
    cancelButton.place(x=135,y=30)

    label = tk.Label(
        text = "0%",
        fg="Black")
    label.place(x=5,y=62)

    progressBar = ttk.Progressbar(
        orient='horizontal',
        mode='determinate',
        length=130,
        maximum=100,)
    progressBar.place(x=40,y=60)

    window.mainloop()