import os
import shutil

class FileMovement:
    def __init__(self,
            source_filepath: str,
            destination_filepath: str):
        self.source_filepath = source_filepath
        self.destination_filepath = destination_filepath

    """
    Gets the folder path of the destination. 
    """
    @property
    def destination_folderpath(self) -> str:
        return os.path.dirname(self.destination_filepath)
    
    """
    Moves the file to its destination path.
    """
    def execute(self):
        # Create the subfolder if it doesn't exist
        os.makedirs(self.destination_folderpath, exist_ok=True)

        # Move the file
        shutil.move(self.source_filepath, self.destination_filepath)
        print("Moved " + self.source_filepath + " to " + self.destination_filepath)
