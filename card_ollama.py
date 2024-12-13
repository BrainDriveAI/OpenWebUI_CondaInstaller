import os
import threading
import urllib.request
import subprocess
from tkinter import messagebox
from base_card import BaseCard
import tkinter as tk
from PIL import Image, ImageTk

class Ollama(BaseCard):
    def __init__(self):
        super().__init__(
            name="Ollama",
            description="Ollama facilitates streamlined operations by providing optimized modules for enhanced functionality and flexibility.",
            size="3.5GB"
        )
        self.installed = False

    def install(self, status_updater=None):
        """Handle the installation of Ollama."""
        def ollama_install_task():
            try:
                if status_updater:
                    status_updater.update_status(
                        "Step: [1/3] Downloading Ollama...",
                        "Downloading the Ollama installer. Please wait.",
                        0,
                    )

                # Define the URL and target path for the installer
                ollama_url = "https://ollama.com/download/OllamaSetup.exe"
                installer_name = "OllamaSetup.exe"
                installer_path = os.path.join(os.getcwd(), installer_name)  # Save in current directory

                # Download the installer
                with urllib.request.urlopen(ollama_url) as response, open(installer_path, 'wb') as out_file:
                    data = response.read()
                    out_file.write(data)

                if status_updater:
                    status_updater.update_status(
                        "Step: [2/3] Running Installer...",
                        "Running the Ollama installer. Follow the on-screen instructions.",
                        50,
                    )

                # Run the installer
                subprocess.Popen(installer_path, shell=True)

                if status_updater:
                    status_updater.update_status(
                        "Step: [3/3] Ollama Installation Started",
                        "The Ollama install inferface should be visible soon.",
                        100,
                    )
                self.installed = True

            except Exception as e:
                if status_updater:
                    status_updater.update_status(
                        "Error: Installation Failed",
                        f"Failed to install Ollama: {e}",
                        0,
                    )
                messagebox.showerror("Error", f"Failed to install Ollama: {e}")

        # Run the installation task in a separate thread
        threading.Thread(target=ollama_install_task, daemon=True).start()


    def uninstall(self):
        """
        Implements the uninstallation logic for Ollama.
        """
        if self.installed:
            print(f"Uninstalling {self.name}...")
            import time
            time.sleep(2)  # Simulate uninstallation time
            self.installed = False
            print(f"{self.name} uninstallation complete.")
        else:
            print(f"{self.name} is not installed.")

    def get_status(self):
        """
        Returns the installation status of Ollama.
        """
        return f"{self.name} is {'installed' if self.installed else 'not installed'}."
    
    def display(self, parent_frame, status_updater):
        """
        Displays the card UI within the given Tkinter frame.
        """
        self.set_parent_frame(parent_frame)
        card_frame = tk.Frame(parent_frame, relief=tk.GROOVE, bd=2)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        card_image = Image.open("ollama.png")
        card_image.thumbnail((50, 50))
        card_photo = ImageTk.PhotoImage(card_image)

        ollama_icon = tk.Label(card_frame, image=card_photo)
        ollama_icon.image = card_photo  # Keep a reference
        ollama_icon.place(x=10, y=10)


        card_label = tk.Label(card_frame, text=self.name, font=("Arial", 16))
        card_label.place(relx=0.5, y=20, anchor="center")

        card_info = tk.Label(
            card_frame,
            text=self.description,
            font=("Arial", 10),
            wraplength=350,
            justify="left"
        )
        card_info.place(x=10, y=70)

        size_label = tk.Label(card_frame, text=f"Size: {self.size}", font=("Arial", 9))
        size_label.place(x=10, rely=1.0, anchor="sw", y=-10)

        install_button = tk.Button(
            card_frame,
            text="Install",
            command=lambda: self.install(status_updater)
        )
        install_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)


        # uninstall_button = tk.Button(card_frame, text="Uninstall", command=self.uninstall)
        # uninstall_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        status_button = tk.Button(
            card_frame,
            text="Status",
            command=lambda: print(self.get_status())
        )
        # status_button.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)    

