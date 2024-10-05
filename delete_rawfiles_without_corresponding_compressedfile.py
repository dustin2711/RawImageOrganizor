import os
from os.path import join
from pathlib import Path
from config import Config

""" Returns filesize of all files in byte. """
def get_sizes_of_files(paths: list[str]):
    return sum(os.path.getsize(path) for path in paths if os.path.isfile(path))

def delete_rawfiles_without_corresponding_jpg(rootfolderpath: str, raw_fileending: str = ".arw", compressed_fileending: str = ".jpg", subfoldername = "raw"):
    print(f"Searching for raw files with ending {raw_fileending} in sub-subfolders of {rootfolderpath}: ")
    raw_filepaths_to_delete = []

    # Walk through the directory structure
    for folderpath, _, filenames in os.walk(rootfolderpath):
        # Skip if folder is not in a sub-subfolder
        if folderpath.count(os.sep) - rootfolderpath.count(os.sep) != 2:
            continue

        if not folderpath.endswith(subfoldername):
            continue

        parent_foldername = os.path.dirname(folderpath)
        parent_folder_filenames = os.listdir(parent_foldername)


        # List of .jpg files in the parent folder
        jpg_filenames = sorted([Path(filename).stem.lower() for filename in parent_folder_filenames if filename.lower().endswith(compressed_fileending)])
        raw_filenames = sorted([Path(filename).stem.lower() for filename in filenames if filename.lower().endswith(raw_fileending)])

        # Check for orphan .arw files in the current folder
        for raw_filename in raw_filenames:
            if not any((jpg_filename in raw_filename) for jpg_filename in jpg_filenames):
                # Orphan .arw file detected, delete it
                path = join(folderpath, raw_filename + raw_fileending)
                raw_filepaths_to_delete.append(path)
                print(path)

    if not raw_filepaths_to_delete:
        print(f"No {raw_fileending} files without {compressed_fileending} file in parent folders were found.")
        return
    
    if input(f"Press any key to delete all listed files ({0.000001 * get_sizes_of_files(raw_filepaths_to_delete)} MB).") == "":
        for filepath in raw_filepaths_to_delete:
            os.remove(filepath)

        print("Deleted all orphan raw files successfully.")

# Get the directory where the script is located
root_folderpath = os.path.dirname(os.path.abspath(__file__))
config = Config()
delete_rawfiles_without_corresponding_jpg(root_folderpath, config.raw_fileending, config.jpg_fileending, config.raw_subfoldername)