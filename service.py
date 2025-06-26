
import threading
import time
import pyautogui  # Neu: Für globales Tippen

class Service:
    def __init__(self, root):
        self.root = root
        self.script_text = ""
        self.interval_ms = 0
        self.running = False
        self.abort_flag = threading.Event()
        self._after_id = None

    def set_script(self, text: str):
        self.script_text = text

    def set_interval(self, minutes: int, seconds: int):
        total_seconds = minutes * 60 + seconds
        self.interval_ms = total_seconds * 1000

    def start(self):
        if self._after_id:
            self.root.after_cancel(self._after_id)
        self.abort_flag.clear()
        self.running = True
        threading.Thread(target=self._run_script, daemon=True).start()

    def stop(self):
        self.abort_flag.set()
        self.running = False
        if self._after_id:
            self.root.after_cancel(self._after_id)

    def _run_script(self):
        while not self.abort_flag.is_set():
            # 1. Text abtippen
            for ch in self.script_text:
                if self.abort_flag.is_set():
                    break
                pyautogui.typewrite(ch)
                time.sleep(0.05)
            # 2. Timer abwarten
            if self.abort_flag.is_set():
                break
            sleep_time = self.interval_ms / 1000
            for _ in range(int(sleep_time)):
                if self.abort_flag.is_set():
                    break
                time.sleep(1)
            if self.abort_flag.is_set():
                break
        self.running = False