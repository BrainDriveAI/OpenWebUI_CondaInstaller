import os
import sys
import psutil
import socket
import subprocess
import time
import webbrowser
from ButtonStateManager import ButtonStateManager
from base_card import BaseCard
import tkinter as tk
from PIL import Image, ImageTk
import threading
from installer_miniconda import MinicondaInstaller
from installer_openwebui import OpenWebUIInstaller
from installer_pipelines import PipelinesInstaller

class OpenWebUI(BaseCard):
    def __init__(self):
        super().__init__(name="Open WebUI", description="A robust tool for creating controlling and befeting from your own AI System", size="4.5GB")
        self.server_running = False  # Tracks if the server is running

    def install(self, status_updater=None):
        """
        Implements the installation logic for Open WebUI.
        Updates the status bar if a StatusUpdater instance is provided.
        """
        def installation_task():
            if status_updater:
                status_updater.update_status(
                    "Step: [1/3] Preparing Installation...",
                    "Initializing installation process for Open WebUI.",
                    0,
                )
            import time
            time.sleep(2)

            if status_updater:
                status_updater.update_status(
                    "Step: [2/3] Installing...",
                    "Installing Open WebUI. Please wait.",
                    50,
                )
            time.sleep(3)

            self.is_installed = True
            if status_updater:
                status_updater.update_status(
                    "Step: [3/3] Finalizing...",
                    "Installation complete for Open WebUI.",
                    100,
                )
            time.sleep(1)

            print(f"{self.name} installation complete.")

        # Run the installation task in a separate thread
        threading.Thread(target=installation_task, daemon=True).start()

    def install(self, status_updater=None):
        """
        Install Open WebUI, ensuring prerequisites like Miniconda are installed.
        """
        def installation_task():
            button_manager = ButtonStateManager()
            button_manager.disable_buttons("install_open_webui")
            try:
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

                # Proceed with Open WebUI installation
                if status_updater:
                    status_updater.update_status(
                        "Step: [1/3] Setting Up Environment...",
                        "Creating a Conda environment for Open WebUI.",
                        0,
                    )
                webui_installer = OpenWebUIInstaller(status_updater)

                # Use OpenWebUIInstaller to set up the environment and install Open WebUI
                try:
                    webui_installer.setup_environment("env")

                    if status_updater:
                        status_updater.update_status(
                            "Step: [3/3] Installation Complete.",
                            "Open WebUI installed successfully.",
                            100,
                        )
                except Exception as e:
                    if status_updater:
                        status_updater.update_status(
                            "Error: Installation Failed setting up environment.",
                            f"An error occurred: {e}",
                            0,
                        )
                    return

                # Install Open WebUI
                try:
                    webui_installer.install()

                    if status_updater:
                        status_updater.update_status(
                            "Step: [3/3] Installation Complete.",
                            "Open WebUI installed successfully.",
                            100,
                        )
                except Exception as e:
                    if status_updater:
                        status_updater.update_status(
                            "Error: Installation Failed.",
                            f"An error occurred: {e}",
                            0,
                        )
                    return

                # Set up Pipelines
                # pipeline_installer = PipelinesInstaller(status_updater)
                try:
                    miniconda_installer.setup_environment("env_pipelines", packages=["git"])

                    if status_updater:
                        status_updater.update_status(
                            "Step: [3/3] Pipelines Environment Complete.",
                            "Environment installed successfully.",
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

                # Set up Pipelines
                pipeline_installer = PipelinesInstaller(status_updater)
                try:
                    pipeline_installer.install()

                    if status_updater:
                        status_updater.update_status(
                            "Step: [3/3] Pipelines Install Complete.",
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
                
                # button_manager.enable_buttons("install_open_webui")

        # Run installation in a separate thread
        threading.Thread(target=installation_task, daemon=True).start()



    def start_server(self, status_updater=None):
        """
        Starts the Open WebUI server and Pipelines process.
        Leaves PID files for later shutdown.
        """
        def start_open_webui():
            """
            Start the Open WebUI server.
            """
            try:
                webui_installer = OpenWebUIInstaller(status_updater)
                if not webui_installer.check_installed():
                    if status_updater:
                        status_updater.update_status(
                            "Error: Open WebUI Not Installed.",
                            "Cannot start the server because Open WebUI is not installed.",
                            0,
                        )
                    return

                status_updater.update_status(
                    "Step: Starting Open WebUI...",
                    "Launching the Open WebUI server. Please wait.",
                    50,
                )
                conda_exe = webui_installer.conda_exe
                env_path = webui_installer.env_path
                open_webui_cmd = [
                    conda_exe,
                    "run",
                    "--prefix", env_path,
                    "open-webui", "serve"
                ]

                CREATE_NO_WINDOW = 0x08000000
                webui_process = subprocess.Popen(
                    open_webui_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=CREATE_NO_WINDOW
                )

                open_webui_pid_file = os.path.join(webui_installer.config.base_path, "open_webui.pid")
                with open(open_webui_pid_file, "w") as f:
                    f.write(str(webui_process.pid))

                status_updater.update_status(
                    "Step: Open WebUI Started.",
                    "Open WebUI server is now running.",
                    75,
                )
            except Exception as e:
                if status_updater:
                    status_updater.update_status(
                        "Error: Failed to Start Open WebUI.",
                        f"An error occurred: {e}",
                        0,
                    )

        def start_pipelines():
            """
            Start the Pipelines process.
            """
            try:
                pipeline_installer = PipelinesInstaller(status_updater)
                if not pipeline_installer.check_requirements():
                    if status_updater:
                        status_updater.update_status(
                            "Error: Pipelines Environment Not Set Up.",
                            "Cannot start pipelines because the environment is not set up.",
                            0,
                        )
                    return

                status_updater.update_status(
                    "Step: Starting Pipelines...",
                    "Launching the Pipelines process. Please wait.",
                    50,
                )

                pipeline_process = pipeline_installer.start_pipelines()
                # pipeline_pid_file = os.path.join(pipeline_installer.config.base_path, "pipelines.pid")
                # with open(pipeline_pid_file, "w") as f:
                #     f.write(str(pipeline_process))

                status_updater.update_status(
                    "Step: Pipelines Started.",
                    "Pipelines are now running.",
                    75,
                )
            except Exception as e:
                if status_updater:
                    status_updater.update_status(
                        "Error: Failed to Start Pipelines.",
                        f"An error occurred: {e}",
                        0,
                    )
        def monitor_server_and_open_browser():
            """
            Monitor the Open WebUI server until it's up, then open the browser.
            """
            try:
                server_ready = False
                print("Checking server availability on localhost:8080...")
                for _ in range(120):  # Retry for up to 120 attempts (2 minutes)
                    try:
                        with socket.create_connection(("localhost", 8080), timeout=2):
                            server_ready = True
                            break
                    except (socket.timeout, ConnectionRefusedError):
                        time.sleep(2)  # Wait before retrying
                if server_ready:
                    print("Server is up. Opening browser to http://localhost:8080...")
                    webbrowser.open("http://localhost:8080")
                else:
                    print("Server did not come up after multiple attempts.")
            except Exception as e:
                print(f"Error while monitoring server: {e}")
                
        def start_both_processes():
            """
            Start both Open WebUI and Pipelines processes concurrently.
            """
            button_manager = ButtonStateManager()
            button_manager.disable_buttons("start_open_webui")

            # Start both processes in separate threads
            threading.Thread(target=start_open_webui, daemon=True).start()
            threading.Thread(target=start_pipelines, daemon=True).start()

            threading.Thread(target=monitor_server_and_open_browser, daemon=True).start()

            # After some time, re-enable the button
            time.sleep(2)
            button_manager.set_button_text("start_open_webui", "Stop Open WebUI")
            button_manager.enable_buttons("start_open_webui")

            start_button = button_manager.buttons.get("start_open_webui")
            if start_button:
                start_button.config(command=lambda: self.stop_server(status_updater))

        # Run the combined task in a separate thread
        threading.Thread(target=start_both_processes, daemon=True).start()


    def stop_server(self, status_updater=None):
        """
        Stops the Open WebUI server and related processes.
        """
        button_manager = ButtonStateManager()
        pid_files = ["open_webui.pid", "pipelines.pid"]  # List of PID files to check

        def stop_process_from_pid_file(pid_file):
            """
            Stops a process given a PID file.
            :param pid_file: The path to the PID file.
            """
            if os.path.exists(pid_file):
                try:
                    # Read the PID from the file
                    with open(pid_file, "r") as f:
                        pid = int(f.read().strip())

                    # Check if the process is running
                    if psutil.pid_exists(pid):
                        process = psutil.Process(pid)
                        print(f"Stopping process with PID {pid}...")
                        # Terminate the process and its children
                        for child in process.children(recursive=True):
                            child.terminate()
                        process.terminate()
                        psutil.wait_procs([process], timeout=5)
                        print(f"Process with PID {pid} stopped.")
                    else:
                        print(f"Process with PID {pid} is not running.")
                except Exception as e:
                    print(f"Error stopping process with PID file {pid_file}: {e}")
                finally:
                    # Remove the PID file
                    os.remove(pid_file)
                    print(f"Removed PID file: {pid_file}")
            else:
                print(f"PID file {pid_file} does not exist.")

        # Stop all processes specified by the PID files
        for pid_file in pid_files:
            stop_process_from_pid_file(os.path.join(self.config.base_path, pid_file))

        # Update server state and button
        self.server_running = False
        if status_updater:
            status_updater.update_status(
                "Server Status",
                "Open WebUI server and associated processes have stopped.",
                0,
            )

        # Reassign the button back to the start function
        start_button = button_manager.buttons.get("start_open_webui")
        if start_button:
            start_button.config(
                text="Start Open WebUI",
                command=lambda: self.start_server(status_updater)
            )

    def uninstall(self, status_updater=None):
        """
        Implements the uninstallation logic for Open WebUI.
        """
        if self.is_installed:
            print(f"Uninstalling {self.name}...")
            import time
            time.sleep(2)  # Simulate uninstallation time
            self.is_installed = False
            print(f"{self.name} uninstallation complete.")
        else:
            print(f"{self.name} is not installed.")

    def get_status(self, status_updater=None):
        """
        Returns the installation status of Open WebUI.
        """
        return f"{self.name} is {'installed' if self.is_installed else 'not installed'}."
    
    def handle_update_check_result(self, update_available):
        """
        Callback function to handle the result of the update check.
        :param update_available: True if an update is available, otherwise False.
        """
        button_manager = ButtonStateManager()
        if update_available:
            button_manager.enable_buttons("update_open_webui")
        else:
            button_manager.disable_buttons("update_open_webui")

        self.config.status_updater.update_status(
            "Initializing Complete",
            "An update is available." if update_available else "No update is available.",
            100,
        )


        
        print(f"Update Check Result: Update Available = {update_available}")            

    def update(self, status_updater=None):
        """
        Update Open WebUI to the latest version.
        Runs in the background and updates the status.
        """
        def update_task():
            try:
                buttonmanager = ButtonStateManager()
                buttonmanager.disable_buttons("update_open_webui")
                buttonmanager.disable_buttons("start_open_webui")

                self.stop_server(status_updater)


                if status_updater:
                    status_updater.update_status(
                        "Step: [1/2] Preparing Update...",
                        "Initializing update process for Open WebUI.",
                        0,
                    )
                import time
                time.sleep(1)  # Simulate preparation time

                if status_updater:
                    status_updater.update_status(
                        "Step: [2/2] Updating...",
                        "Updating Open WebUI. Please wait.",
                        50,
                    )
                
                # Call the `update` method in the installer
                webui_installer = OpenWebUIInstaller(status_updater)
                webui_installer.update()

                if status_updater:
                    status_updater.update_status(
                        "Update Complete",
                        "Open WebUI has been updated successfully.",
                        75,
                    )
                pipelines_installer = PipelinesInstaller(status_updater)
                pipelines_installer.update()

                # Final Step: Completion
                if status_updater:
                    status_updater.update_status(
                        "Update Complete",
                        "Pipelines have been updated successfully.",
                        100,
                    )
                print("Update complete: Open WebUI and Pipelines updated successfully.")

            except Exception as e:
                if status_updater:
                    status_updater.update_status(
                        "Error: Update Failed",
                        f"An error occurred during update: {e}",
                        0,
                    )
                print(f"Update failed: {e}")
            buttonmanager.enable_buttons("start_open_webui")
        # Run the update task in a background thread
        threading.Thread(target=update_task, daemon=True).start()


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

        card_icon = tk.Label(card_frame, image=card_photo)
        card_icon.image = card_photo  # Keep a reference
        card_icon.place(x=10, y=10)

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

        button_manager = ButtonStateManager()
        webui_installer = OpenWebUIInstaller(status_updater)
                


        install_button = tk.Button(card_frame, text="Install", command=lambda: self.install(status_updater))
        install_button.place(relx=1.0, rely=1.0, anchor="se", x=-180, y=-10)
        install_button.config(state="disabled")
        button_manager.register_button("install_open_webui", install_button)

        def toggle_server():
            if self.server_running:
                self.stop_server(status_updater)
                start_stop_button.config(text="Start Open WebUI")
            else:
                self.start_server(status_updater)
                start_stop_button.config(text="Stop Open WebUI")

        start_stop_button = tk.Button(card_frame, text="Start Open WebUI", command=toggle_server)
        start_stop_button.place(relx=1.0, rely=1.0, anchor="se", x=-67, y=-10)
        start_stop_button.config(state="disabled")
        button_manager.register_button("start_open_webui", start_stop_button)

        update_button = tk.Button(card_frame, text="Update", command=lambda: self.update(status_updater))
        update_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        update_button.config(state="disabled")
        button_manager.register_button("update_open_webui", update_button)

        if webui_installer.check_installed():
            button_manager.enable_buttons("start_open_webui")
            webui_installer.check_update(callback=self.handle_update_check_result)
        else:
            button_manager.enable_buttons("install_open_webui")
            self.config.status_updater.update_status(
                "Initializing Complete",
                "New install required",
                100,
            )            
        
        # button_manager.enable_buttons("update_open_webui")
        

        # button_manager.enable_buttons("install_open_webui")
