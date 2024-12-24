import os
import sys
import threading
from ButtonStateManager import ButtonStateManager
from base_card import BaseCard
import tkinter as tk
from PIL import Image, ImageTk

from installer_miniconda import MinicondaInstaller
from installer_openwebui import OpenWebUIInstaller
from installer_pipelines import PipelinesInstaller
from DiskSpaceChecker import DiskSpaceChecker

class OpenWebUIPipelines(BaseCard):
    def __init__(self):
        super().__init__(name="Open WebUI Pipelines", description="Pipelines allow you to extend your AI with additional features and functionality", 
        size="2.0")
        self.installed = False

    def install(self, status_updater=None):
        """
        Install Open WebUI, ensuring prerequisites like Miniconda are installed.
        """
        def installation_task():
            button_manager = ButtonStateManager()
            button_manager.disable_buttons(["start_open_webui", "install_open_webui", "update_open_webui", "install_open_webui_pipelines", "update_open_webui_pipelines"])

            try:
                self.config.start_spinner()
                # Ensure Miniconda is installed
                miniconda_installer = MinicondaInstaller(status_updater)
                miniconda_installer.install()

                # Check if Miniconda installation is successful
                if not miniconda_installer.check_installed():
                    if status_updater:
                        status_updater.update_status(
                            "Error: Miniconda Installation Failed.",
                            "Cannot proceed with Open WebUI installation.",
                            0,
                        )
                    return


                # Set up Pipelines
                # pipeline_installer = PipelinesInstaller(status_updater)
                try:
                    if status_updater:
                        status_updater.update_status(
                            "Step: [1/6] Pipelines Environment Setup is starting",
                            "Environment is being installed.",
                            0,
                        )                  
                    miniconda_installer.setup_environment("env_pipelines", packages=["git"])

                    if status_updater:
                        status_updater.update_status(
                            "Step: [2/6] Pipelines Environment Complete.",
                            "Environment installed successfully.",
                            25,
                        )
                except Exception as e:
                    if status_updater:
                        status_updater.update_status(
                            "Error: Pipelines Setup Failed.",
                            f"An error occurred: {e}",
                            0,
                        )
                    return

                # Set up Pipelines
                pipeline_installer = PipelinesInstaller(status_updater)
                try:
                    if status_updater:
                        status_updater.update_status(
                            "Step: [3/6] Starting Pipelines Instalation.",
                            "Pipelines Installing",
                            50,
                        )                    
                    pipeline_installer.install()

                    if status_updater:
                        status_updater.update_status(
                            "Step: [6/6] Pipelines Install Complete.",
                            "Pipelines installed successfully.",
                            100,
                        )
                except Exception as e:
                    if status_updater:
                        status_updater.update_status(
                            "Error: Pipelines Setup Failed.",
                            f"An error occurred: {e}",
                            0,
                        )
                    return

            finally:
                # Ensure the button is always re-enabled at the end
                webui_installer = OpenWebUIInstaller(status_updater)
                if webui_installer.check_installed():
                    button_manager.enable_buttons("start_open_webui")
                self.config.stop_spinner()


        # Run installation in a separate thread
        threading.Thread(target=installation_task, daemon=True).start()

    def uninstall(self):
        """
        Implements the uninstallation logic for Open WebUI Pipelines.
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
        Returns the installation status of Open WebUI Pipelines.
        """
        return f"{self.name} is {'installed' if self.installed else 'not installed'}."

    def display(self, parent_frame, status_updater):
        """
        Displays the card UI within the given Tkinter frame.
        """

        self.set_parent_frame(parent_frame)
        card_frame = tk.Frame(parent_frame, relief=tk.GROOVE, bd=2)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            image_path = os.path.join(base_path, 'openwebui.png')
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

        disk_checker = DiskSpaceChecker()
        button_manager = ButtonStateManager()

        auto_button = tk.Button(card_frame, text="Auto", state=tk.DISABLED)
        # auto_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        install_button = tk.Button(card_frame, text="Install", command=lambda: self.install(status_updater))
        install_button.place(relx=1.0, rely=1.0, anchor="se", x=-70, y=-10)
        install_button.config(state="disabled")
        button_manager.register_button("install_open_webui_pipelines", install_button)

        update_button = tk.Button(card_frame, text="Update", command=lambda: self.update(status_updater))
        update_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        update_button.config(state="disabled")
        button_manager.register_button("update_open_webui_pipelines", update_button)

        webui_installer = OpenWebUIInstaller(status_updater)
        pipeline_installer = PipelinesInstaller(status_updater)
        if webui_installer.check_installed() and not pipeline_installer.check_installed():
            if disk_checker.has_enough_space(self.size):
                button_manager.enable_buttons("install_open_webui_pipelines")
            else:
                button_manager.disable_buttons("install_open_webui_pipelines")
                self.config.status_updater.update_status(
                    "Error - Open WebUI Pipelines",
                    "Not enough disk space",
                    0,
                ) 




        
    