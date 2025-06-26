
import tkinter as tk
from tkinter import messagebox
from service import Service
import keyboard

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Presser with Timer")
        self.root.geometry("480x450")

        self.service = Service(root)
        self.start_key = 'F2'
        self.listening = False
        self.hotkey_handle = None

        tk.Label(root, text="Write Script", font= ("Helvetica", 16)).pack(pady=(10, 0))
        self.text = tk.Text(root, height=10, width=30, font=("Helvetica", 16))
        self.text.pack(pady=(0, 10))
        self.text.focus_set()


        frame = tk.Frame(root)
        frame.pack(pady=(0, 10))

        def only_numbers(char):
            return char.isdigit() or char == ""

        vcmd = (root.register(only_numbers), "%P")

        tk.Label(frame, text="Minutes:", font=("Helvetica", 16)).grid(row=0, column=0)
        self.minutes_var = tk.StringVar(value="0")
        tk.Entry(frame, textvariable=self.minutes_var, width=5, validate="key", font = ("Helvetica", 16), validatecommand=vcmd).grid(row=0,
                                                                                                           column=1)
        tk.Label(frame, text="Seconds:", font=("Helvetica", 16)).grid(row=0, column=2)
        self.seconds_var = tk.StringVar(value="0")
        tk.Entry(frame, textvariable=self.seconds_var, width=5, validate="key", font = ("Helvetica", 16), validatecommand=vcmd).grid(row=0,
                                                                                                           column=3)

        tk.Label(root, text="Set Your Key to Start the Script", font = ("Helvetica", 16)).pack(pady=(10, 0))
        self.key_button = tk.Button(root, text=self.start_key,width = 15, height = 1, font = ("Helvetica", 13),
                                    command=self.listen_key)
        self.key_button.pack(pady=(0, 10))


        self.register_hotkey()

    def register_hotkey(self):
        if self.hotkey_handle:
            keyboard.remove_hotkey(self.hotkey_handle)
        self.hotkey_handle = keyboard.add_hotkey(self.start_key, self.toggle_script)

    def listen_key(self):
        if self.listening:
            return
        self.listening = True
        self.key_button.config(text="Press any key...")
        self.root.bind('<Key>', self.set_key)

    def set_key(self, event):
        if not self.listening:
            return
        self.start_key = event.keysym
        self.key_button.config(text=self.start_key)
        self.register_hotkey()
        self.root.unbind('<Key>')
        self.listening = False

    def toggle_script(self, event=None):
        if self.service.running:
            self.service.stop()
        else:
            script = self.text.get("1.0", tk.END)
            try:
                minutes = int(self.minutes_var.get())
                seconds = int(self.seconds_var.get())
            except ValueError:
                messagebox.showerror("Invalid input", "Minutes and seconds must be integers.")
                return

            self.service.set_script(script)
            self.service.set_interval(minutes, seconds)
            self.service.start()

    def run(self):
        self.root.mainloop()

def run():
    root = tk.Tk()
    app = App(root)
    app.run()