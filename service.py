import threading
import time
import pyautogui
import pyperclip

class Service:
    def __init__(self, root=None):
        self.root = root
        self.script_text = ""
        self.interval_s = 0.0

        # Abort-Flag for Threads
        self.abort_flag = threading.Event()
        self.running = False

        # Options
        self.letter_by_letter = False
        self.press_enter = False

        # Timer and Worker
        self._timer = None
        self._worker = None

    # Set the script text to be executed
    def set_script(self, text: str):
        self.script_text = text

    # Set the interval for the timer
    def set_interval(self, minutes: int, seconds: int):
        """Legt das Intervall fest."""
        self.interval_s = minutes * 60 + seconds

    # Enable or disable letter-by-letter typing
    def enable_letter_by_letter(self, enabled: bool):
        self.letter_by_letter = enabled

    # Enable or disable pressing Enter after the script
    def enable_press_enter(self, enabled: bool):
        self.press_enter = enabled

    # Start the Program, if not already running
    def start(self):

        if self.running:
            return
        self.abort_flag.clear()
        self.running = True

        # First run through
        self._schedule_next()

    # Stop the Program, if running
    def stop(self):

        # Stops the service and cancels the timer.
        if not self.running:
            return
        self.abort_flag.set()
        self.running = False
        if self._timer:
            self._timer.cancel()

    # Schedule the next execution of the script
    def _schedule_next(self):

        # Stops, if the service is not running or if abort_flag is set
        if not self.running:
            return

        # Start the worker thread to execute the script
        self._worker = threading.Thread(target=self._execute_script, daemon=True)
        self._worker.start()

        # Schedule the next execution
        self._timer = threading.Timer(self.interval_s, self._schedule_next)
        self._timer.daemon = True
        self._timer.start()

    def _execute_script(self):

        # Executes the script text, either letter-by-letter or in bulk
        if self.abort_flag.is_set():
            return
        if self.letter_by_letter:
            for ch in self.script_text:
                if self.abort_flag.is_set():
                    return
                pyautogui.write(ch)
                time.sleep(0.05)
            if self.press_enter and not self.abort_flag.is_set():
                pyautogui.press('enter')
        else:

            # Bulk-Paste
            pyperclip.copy(self.script_text)
            if self.abort_flag.is_set():
                return
            pyautogui.hotkey('ctrl', 'v')
            if self.press_enter and not self.abort_flag.is_set():
                time.sleep(0.05)
                if not self.abort_flag.is_set():
                    pyautogui.press('enter')
