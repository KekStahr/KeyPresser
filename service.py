import threading
import time
import pyautogui
import pyperclip

class Service:
    def __init__(self, root=None):

        self.root = root
        self.script_text = ""
        self.interval_s = 0.0

        # Flag für sofortigen Abbruch
        self.abort_flag = threading.Event()

        # Status-Flag
        self.running = False

        # Timer-Handles
        self._timer = None
        self._paste_timer = None
        self._enter_timer = None

        # Optionen
        self.letter_by_letter = False
        self.press_enter = False

    def set_script(self, text: str):
        self.script_text = text

    def set_interval(self, minutes: int, seconds: int):
        self.interval_s = minutes * 60 + seconds

    def enable_letter_by_letter(self, enabled: bool):
        self.letter_by_letter = enabled

    def enable_press_enter(self, enabled: bool):
        self.press_enter = enabled

    def start(self):
        if self.running:
            return

        # Abbruch-Flag löschen und Timer starten
        self.abort_flag.clear()
        self.running = True
        self._schedule_next()

    def stop(self):
        if not self.running:
            return

        # Setze Abbruch-Flag, cancelle alle Timer und Status zurücksetzen
        self.abort_flag.set()
        self.running = False
        for t in (self._timer, self._paste_timer, self._enter_timer):
            if t:
                t.cancel()
        self._timer = None
        self._paste_timer = None
        self._enter_timer = None

    def _schedule_next(self):
        if self.abort_flag.is_set():
            return

        # 1. Script tippen
        if self.letter_by_letter:
            for ch in self.script_text:
                if self.abort_flag.is_set():
                    return
                pyautogui.write(ch)
                time.sleep(0.05)
            if self.press_enter and not self.abort_flag.is_set():
                pyautogui.press('enter')
        else:
            if self.abort_flag.is_set():
                return
            pyperclip.copy(self.script_text)

            # Paste nach kurzer Verzögerung
            self._paste_timer = threading.Timer(0.1, self._paste_and_enter)
            self._paste_timer.daemon = True
            self._paste_timer.start()

        # 2. Nächsten Lauf planen
        if not self.abort_flag.is_set():
            self._timer = threading.Timer(self.interval_s, self._schedule_next)
            self._timer.daemon = True
            self._timer.start()

    def _paste_and_enter(self):
        if self.abort_flag.is_set():
            return
        pyautogui.hotkey('ctrl', 'v')
        if self.press_enter and not self.abort_flag.is_set():
            # Enter nach Paste
            self._enter_timer = threading.Timer(0.05, self._conditional_press_enter)
            self._enter_timer.daemon = True
            self._enter_timer.start()

    def _conditional_press_enter(self):
        if not self.abort_flag.is_set():
            pyautogui.press('enter')
