import threading

class StatusUpdater:
    def __init__(self, step_label, details_label, progress_bar):
        self.step_label = step_label
        self.details_label = details_label
        self.progress_bar = progress_bar
        self.lock = threading.Lock()

    def update_status(self, step_text, details_text, progress_value):
        with self.lock:
            # Use `after` to schedule updates on the Tkinter main thread
            self.step_label.after(0, self.step_label.config, {"text": step_text})
            self.details_label.after(0, self.details_label.config, {"text": details_text})
            self.progress_bar.after(0, self.progress_bar.config, {"value": progress_value})
