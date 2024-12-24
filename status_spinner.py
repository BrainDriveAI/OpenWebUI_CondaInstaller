import tkinter as tk
from threading import Thread
import time

class StatusSpinner:
    def __init__(self, parent, step_label):
        """
        Initializes the spinner with a label to display the spinning animation.
        :param parent: The parent frame to attach the spinner.
        :param step_label: The label next to which the spinner appears.
        """
        self.parent = parent
        self.step_label = step_label
        self.spinner_label = tk.Label(parent, text="", font=("Arial", 12), bg="lightgrey")
        self.active = False
        self.symbols = ["|", "/", "-", "\\"]
        self.colors = ["black", "black", "black", "black"]

    def start(self):
        """Starts the spinner animation and repositions the step label."""
        if not self.active:
            self.active = True
            # Move the step label to the right
            self.step_label.pack_configure(padx=(25, 10))  # Add left padding to create space

            # Center the spinner vertically with respect to the step label
            self.parent.update_idletasks()  # Ensure geometry info is updated
            step_label_y = self.step_label.winfo_y()
            step_label_height = self.step_label.winfo_height()
            spinner_label_height = self.spinner_label.winfo_reqheight()  # Requested height of spinner
            spinner_y = step_label_y + (step_label_height - spinner_label_height) // 2

            # Position spinner near the step label
            self.spinner_label.place(x=10, y=spinner_y)

            Thread(target=self._animate, daemon=True).start()

    def stop(self):
        """Stops the spinner animation and resets the step label position."""
        self.active = False
        # Reset the step label position
        self.step_label.pack_configure(padx=10)  # Restore original padding
        self.spinner_label.place_forget()  # Hide the spinner label

    def _animate(self):
        """Handles the spinner animation loop."""
        idx = 0
        while self.active:
            # Update the spinner symbol and color on the main thread
            self.spinner_label.after(
                0,
                lambda symbol=self.symbols[idx % len(self.symbols)],
                color=self.colors[idx % len(self.colors)]:  # Correctly closed with )
                self.spinner_label.config(text=symbol, fg=color)
            )
            idx += 1
            time.sleep(0.1)

