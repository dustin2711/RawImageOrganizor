import os
from os.path import join
from file_movement import FileMovement

"""
This method will iterate through all files under the folder of the specified root folder path.
Every files with the specified file extension will then be moved to subfolder of the given folder name.
"""
def move_rawfiles_to_subfolder(rootfolderpath: str, folderdepths: list[int] = [1], fileending: str = ".arw", subfoldername = "raw"):
    print(f"This program will moves all files ending with {fileending} in all subfolders of {rootfolderpath} with depths {folderdepths} to another subfolder named '{subfoldername}'.\n")

    file_movements: list[FileMovement] = []

    # Walk through the directory structure
    for folderpath, _, filenames in os.walk(rootfolderpath):
        # Skip if folder has wrong depth
        folderdepth = folderpath.count(os.sep) - rootfolderpath.count(os.sep)
        if folderdepth not in folderdepths:
            continue
        print(folderpath, "| folderdepth = ", folderdepth)

        # Skip if already in folder of the given name
        if folderpath.endswith(subfoldername):
            continue
        
        # Filter for .arw files
        for filename in filenames:
            if filename.lower().endswith(fileending):
                movement: FileMovement = FileMovement(
                    source_filepath = join(folderpath, filename), 
                    destination_filepath = join(folderpath, subfoldername, filename))
                print(f"{movement.source_filepath} -> {movement.destination_filepath}");
                file_movements.append(movement)

    # Before moving files, ask for confirmation
    if input("Confirm moving all next files by pressing enter.") == "":
        for movement in file_movements:
            movement.execute()

    print("Moved all files successfully.")

# Get the directory where the script is located
root_folderpath = os.path.dirname(os.path.abspath(__file__))
move_rawfiles_to_subfolder(root_folderpath)