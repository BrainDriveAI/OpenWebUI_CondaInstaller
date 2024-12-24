import tkinter as tk
from tkinter import ttk

from status_spinner import StatusSpinner

class StatusDisplay:
    def __init__(self, parent):
        """
        Initializes the StatusDisplay and creates its components.
        """
        self.frame = tk.Frame(parent, height=100, bg="lightgrey")
        self.frame.pack(fill=tk.X, padx=10, pady=10)

        self.step_label = tk.Label(self.frame, text="Initializing...", font=("Arial", 12), bg="lightgrey")
        self.step_label.pack(anchor="w", padx=10, pady=5)

        self.spinner = StatusSpinner(self.frame, self.step_label)  # Pass step_label to the spinner

        self.details_label = tk.Label(
            self.frame,
            text="Gathering information about current setup.",
            font=("Arial", 10),
            wraplength=580,
            justify="left",
            bg="lightgrey",
        )
        self.details_label.pack(anchor="w", padx=10)

        self.progress_bar = ttk.Progressbar(self.frame, length=580, mode="determinate")
        self.progress_bar.pack(padx=10, pady=10)
        self.progress_bar['value'] = 50  # Initial progress value

    def get_components(self):
        """
        Returns the components needed for the StatusUpdater.

        :return: A tuple (step_label, details_label, progress_bar)
        """
        return self.step_label, self.details_label, self.progress_bar

