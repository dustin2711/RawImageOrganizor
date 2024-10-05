import os
from datetime import datetime
import re
from config import Config
from file_movement import FileMovement

def sort_files_to_folders_by_date(
        rootfolderpath : str, 
        folderdepths: list[int] = [1],
        raw_fileending: str = ".arw", 
        compressed_fileending: str = ".jpg",
        date_pattern_string: str = r"^\d{4}-\d{2}-\d{2}"):
    # Regex pattern to match folders starting with the yyyy-mm-dd format
    date_pattern = re.compile(date_pattern_string)

    file_movements: list[FileMovement] = []

    # Walk through the directory structure
    for folderpath, _, filenames in os.walk(rootfolderpath):
        # Skip if folder has wrong depth
        folderdepth = folderpath.count(os.sep) - rootfolderpath.count(os.sep)
        if folderdepth not in folderdepths:
            continue

        # Skip directories that already start with YYYY-MM-DD
        if date_pattern.match(os.path.basename(folderpath)):
            continue

        # Process the files in the non-YYYY-MM-DD folders
        for file in filenames:
            # Only process files of specified raw and jpg format
            if not file.lower().endswith((raw_fileending, compressed_fileending)):
                continue

            # Get the full file path
            file_path = os.path.join(folderpath, file)
            
            # Get the file's creation time (or last modification time if creation time is unavailable)
            file_time = os.path.getmtime(file_path)
            file_time_string = datetime.fromtimestamp(file_time).strftime('%Y-%m-%d')
            
            # Create the folder for the recording day if it doesn't exist
            date_folder = os.path.join(rootfolderpath, file_time_string)

            # Move the file to the folder named by recording day
            destination_path = os.path.join(date_folder, file)
            file_movements.append(FileMovement(file_path, destination_path))
            print(f"{file_path} -> {destination_path}")

    if input("Confirm moving all next files by pressing enter.") == "":
        for movement in file_movements:
            movement.execute()

    print("Images moved based on their recording day, excluding YYYY-MM-DD folders.")

# Get the directory where this script is located
rootfolderpath = os.path.dirname(os.path.abspath(__file__))
config = Config()
sort_files_to_folders_by_date(rootfolderpath, [1], config.raw_fileending, config.jpg_fileending, config.date_pattern)