import os

# Function to delete empty folders
def delete_empty_folders(directory):

    folders_to_delete: list[str] = []

    # Walk through the directory structure from bottom to top
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        # Check if the directory is empty
        if not dirnames and not filenames:
            print(f"Deleting empty folder: {dirpath}")
            folders_to_delete.append(dirpath)

    if input("Confirm deleting all empty folders by pressing enter.") == "":
        for folder in folders_to_delete:
            os.rmdir(folder)

    print("All empty folders deleted.")

# Get the directory where the script is located
root_dir = os.path.dirname(os.path.abspath(__file__))
delete_empty_folders(root_dir)

