import os
import shutil
import sys
import threading
from AppConfig import AppConfig

class HelperImage:
    """
    Helper class to manage image files for both script and PyInstaller executable environments,
    and to integrate with AppConfig for base path checking.
    """

    @staticmethod
    def get_image_path(image_name, callback=None):
        """
        Get the path of the image file. If it doesn't exist, extract it from the PyInstaller directory (_MEIPASS)
        or check the AppConfig base path.
        
        :param image_name: Name of the image file to check and extract if necessary.
        :param callback: Optional callback function to call after the image is extracted.
        :return: Full path to the image file.
        """
        app_config = AppConfig()  # Initialize AppConfig to get the base path

        # Check the current working directory first
        target_path = os.path.join(os.getcwd(), image_name)
        if os.path.exists(target_path):
            if callback:
                callback(target_path)
            return target_path

        # Check the AppConfig base path
        app_config_path = os.path.join(app_config.base_path, image_name)
        if os.path.exists(app_config_path):
            if callback:
                callback(app_config_path)
            return app_config_path

        # Check the PyInstaller directory (_MEIPASS) or script directory
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        source_path = os.path.join(base_dir, image_name)

        # Extract the file from the source path if it exists
        if os.path.exists(source_path):
            try:
                # Extract to the AppConfig base path
                if not os.path.exists(app_config.base_path):
                    os.makedirs(app_config.base_path, exist_ok=True)
                shutil.copy2(source_path, app_config_path)
                print(f"Extracted '{image_name}' to '{app_config_path}'.")
                if callback:
                    callback(app_config_path)
                return app_config_path
            except Exception as e:
                raise RuntimeError(f"Failed to extract '{image_name}': {e}")
        else:
            raise FileNotFoundError(
                f"Image '{image_name}' not found in '{source_path}', '{target_path}', or '{app_config_path}'."
            )

    @staticmethod
    def extract_images_in_background(image_list, callback=None):
        """
        Extract multiple images in a background thread.
        
        :param image_list: List of image filenames to extract.
        :param callback: Optional callback function to call after all images are processed.
        """
        def extract_task():
            app_config = AppConfig()  # Initialize AppConfig to get the base path
            extracted_images = []

            for image_name in image_list:
                try:
                    # Check or extract each image
                    target_path = HelperImage.get_image_path(image_name)
                    extracted_images.append(target_path)
                except Exception as e:
                    print(f"Error processing '{image_name}': {e}")

            # Invoke the callback with the list of extracted images
            if callback:
                callback(extracted_images)

        # Run the extraction task in a background thread
        threading.Thread(target=extract_task, daemon=True).start()