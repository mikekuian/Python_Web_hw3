import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def move_file(path_to_file, destination_folder):
    destination_path = os.path.join(destination_folder, os.path.basename(path_to_file))
    if not os.path.exists(destination_path):
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        shutil.move(path_to_file, destination_folder)
        logging.info(f"Moved file {path_to_file} to {destination_folder}")
    else:
        logging.warning(f"File {destination_path} already exists. Skipping.")

def process_folder(folder_path, base_folder=None):
    if base_folder is None:
        base_folder = folder_path

    with ThreadPoolExecutor() as executor:
        futures = []
        for item in os.listdir(folder_path):
            full_path = os.path.join(folder_path, item)

            if os.path.isdir(full_path):
                future = executor.submit(process_folder, full_path, base_folder)
                futures.append(future)
            else:
                _, file_extension = os.path.splitext(item)
                if file_extension:
                    destination_folder = os.path.join(base_folder, file_extension.strip('.').upper())
                    future = executor.submit(move_file, full_path, destination_folder)
                    futures.append(future)

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    base_folder = r"D:\ham_project"  # Use the correct path to your folder

    if not os.path.exists(base_folder):
        logging.error(f"Error: the path '{base_folder}' does not exist.")
    else:
        try:
            process_folder(base_folder)
        except Exception as e:
            logging.error(f"An error happened during the folder execution: {e}")
