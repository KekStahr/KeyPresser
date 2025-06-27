import tkinter as tk
from tkinter import messagebox
from service import Service
import keyboard

class App:
    # The App itself
    def __init__(self, root):
        self.root = root
        self.root.title("Key Presser with Timer")
        self.root.geometry("480x500")

        self.service = Service(root)
        self.start_key = 'F2'     # Default hotkey to start the script
        self.listening = False    # Flag to check if we are listening for a key press
        self.hotkey_handle = None # Handle for the hotkey

        # Script-text field
        tk.Label(root, text="Write Script", font=("Helvetica", 16)).pack(pady=(10, 0))
        self.text = tk.Text(root, height=10, width=30, font=("Helvetica", 16))
        self.text.pack(pady=(0, 10))
        self.text.focus_set()

        # Options for letter-by-letter typing and pressing Enter
        self.var_letter = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Letter by Letter", variable=self.var_letter,
                       font=("Helvetica", 14)).pack(pady=(0,5))

        self.var_enter = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Press Enter at End", variable=self.var_enter,
                       font=("Helvetica", 14)).pack(pady=(0,10))

        # Set the timer
        frame = tk.Frame(root)
        frame.pack(pady=(0, 10))

        # Validate function to ensure only numbers are entered
        def only_numbers(char):
            return char.isdigit() or char == ""

        vcmd = (root.register(only_numbers), "%P")

        tk.Label(frame, text="Minutes:", font=("Helvetica", 16)).grid(row=0, column=0)
        self.minutes_var = tk.StringVar(value="0")
        tk.Entry(frame, textvariable=self.minutes_var, width=5, validate="key",
                 font=("Helvetica", 16), validatecommand=vcmd).grid(row=0, column=1)

        tk.Label(frame, text="Seconds:", font=("Helvetica", 16)).grid(row=0, column=2)
        self.seconds_var = tk.StringVar(value="0")
        tk.Entry(frame, textvariable=self.seconds_var, width=5, validate="key",
                 font=("Helvetica", 16), validatecommand=vcmd).grid(row=0, column=3)

        # Hotkey-Einstellung
        tk.Label(root, text="Set Your Key to Start the Script", font=("Helvetica", 16)).pack(pady=(10, 0))
        self.key_button = tk.Button(root, text=self.start_key, width=15, height=1,
                                    font=("Helvetica", 13), command=self.listen_key)
        self.key_button.pack(pady=(0, 10))

        self.register_hotkey()

    # Register the hotkey for starting the script
    def register_hotkey(self):
        if self.hotkey_handle:
            keyboard.remove_hotkey(self.hotkey_handle)
        self.hotkey_handle = keyboard.add_hotkey(self.start_key, self.toggle_script)

    # Listen for a key press to set the hotkey
    def listen_key(self):
        if self.listening:
            return
        self.listening = True
        self.key_button.config(text="Press any key...")
        self.root.bind('<Key>', self.set_key)

    # Set the key for the hotkey when a key is pressed
    def set_key(self, event):
        if not self.listening:
            return
        self.start_key = event.keysym
        self.key_button.config(text=self.start_key)
        self.register_hotkey()
        self.root.unbind('<Key>')
        self.listening = False

    # Toggle the script on or off
    def toggle_script(self, event=None):
        if self.service.running:
            self.service.stop()
        else:
            # Read the script and timer values
            script = self.text.get("1.0", tk.END)
            try:
                minutes = int(self.minutes_var.get())
                seconds = int(self.seconds_var.get())
            except ValueError:
                messagebox.showerror("Invalid input", "Minutes and seconds must be integers.")
                return

            # Check if script is empty
            self.service.set_script(script)
            self.service.set_interval(minutes, seconds)

            # Enable options based on user selection
            self.service.enable_letter_by_letter(self.var_letter.get())
            self.service.enable_press_enter(self.var_enter.get())

            # Start or stop the service
            self.service.start()


    def run(self):
        self.root.mainloop()


def run():
    root = tk.Tk()
    app = App(root)
    app.run()