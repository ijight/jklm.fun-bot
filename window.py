import asyncio
import tkinter as tk
from tkinter import ttk
import threading
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Function to update the Text widget content asynchronously
async def update_text_widget(text_widget, content):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, content)
    text_widget.config(state=tk.DISABLED)
    text_widget.config(height=1000)

def tkinter_thread(label_queue, loop_holder):
    # Set up the Tkinter window
    root = tk.Tk()
    agent = 1
    root.title(f"Agent {agent} window")
    root.geometry("600x1000")

    # Create a Text widget
    text_widget = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 14))
    text_widget.pack(pady=20, padx=10)
    text_widget.config(state=tk.DISABLED)

    # Create the asyncio event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop_holder["loop"] = loop

    # Run the Tkinter main loop and asyncio event loop together
    def run_event_loop():
        while True:
            loop.call_soon(loop.stop)
            loop.run_forever()
            root.update_idletasks()
            root.update()
            while not label_queue.empty():
                content = label_queue.get_nowait()
                loop.create_task(update_text_widget(text_widget, content))
            time.sleep(0.01)

    threading.Thread(target=run_event_loop, daemon=True).start()
    root.mainloop()

def start_tkinter_window():
    label_queue = asyncio.Queue()
    loop_holder = {}
    thread = threading.Thread(target=tkinter_thread, args=(label_queue, loop_holder), daemon=True)
    thread.start()
    while "loop" not in loop_holder:
        time.sleep(0.01)  # Wait for the loop to be set
    return label_queue, loop_holder["loop"]