import os
import sys
import threading
import time
import urllib.request
import subprocess
from tkinter import messagebox
from base_card import BaseCard
import tkinter as tk
from PIL import Image, ImageTk
import socket
from ButtonStateManager import ButtonStateManager
from DiskSpaceChecker import DiskSpaceChecker

class Ollama(BaseCard):
    def __init__(self):
        super().__init__(
            name="Ollama",
            description="Ollama allows you to download and run AI models on your computer to use with your AI system privately and securely",
            size="3.5"
        )
        self.installed = False

    def is_port_open(self, port=11434):
        """
        Check if a specific port is open.
        :param port: Port number to check (default is 11434).
        :return: True if the port is open, False otherwise.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Timeout for the connection attempt
            result = sock.connect_ex(('127.0.0.1', port))
            return result == 0  # 0 means the port is open

    def install(self, status_updater=None):
        """Handle the installation of Ollama."""
        def ollama_install_task():
            try:
                self.config.status_updater.update_status(
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

                self.config.status_updater.update_status(
                        "Step: [2/3] Running Installer...",
                        "Running the Ollama installer. Follow the on-screen instructions.",
                        50,
                    )

                # Run the installer
                subprocess.Popen(installer_path, shell=True)

                self.config.status_updater.update_status(
                        "Step: [3/3] Ollama Installation Started",
                        "The Ollama install inferface should be visible soon.",
                        100,
                    )
                self.installed = True

            except Exception as e:
                self.config.status_updater.update_status(
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

    def monitor_port_and_update_button(self, button_name):
        """
        Continuously checks the port status and updates the button state.
        :param button_name: The unique name of the button in the ButtonStateManager.
        """
        def task():
            button_manager = ButtonStateManager()
            disk_checker = DiskSpaceChecker()
            while True:
                if self.is_port_open():
                    # Port is open, disable the install button
                    button_manager.disable_buttons(button_name)
                else:
                    if disk_checker.has_enough_space(self.size):
                        button_manager.enable_buttons(button_name)
                    else:
                        button_manager.disable_buttons(button_name)
                time.sleep(1)  # Check every second

        threading.Thread(target=task, daemon=True).start()
        

    def display(self, parent_frame, status_updater):
        """
        Displays the card UI within the given Tkinter frame.
        """
        button_manager = ButtonStateManager()

        self.set_parent_frame(parent_frame)
        card_frame = tk.Frame(parent_frame, relief=tk.GROOVE, bd=2)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            image_path = os.path.join(base_path, 'ollama.png')
            card_image = Image.open(image_path)
        except Exception as e:
            print(f"Failed to load the image: {e}")


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

        size_label = tk.Label(card_frame, text=f"Size: {self.size}GB", font=("Arial", 9))
        size_label.place(x=10, rely=1.0, anchor="sw", y=-10)

        install_button = tk.Button(
            card_frame,
            text="Install",
            command=lambda: self.install(status_updater)
        )
        install_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        button_manager.register_button("install_ollama", install_button)

        self.monitor_port_and_update_button("install_ollama")

        # uninstall_button = tk.Button(card_frame, text="Uninstall", command=self.uninstall)
        # uninstall_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        status_button = tk.Button(
            card_frame,
            text="Status",
            command=lambda: print(self.get_status())
        )
        # status_button.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)    

