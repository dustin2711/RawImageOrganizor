import configparser

class Config:
    def __init__(self, path: str = "config.ini") -> None:
        parser = configparser.ConfigParser()
        parser.read(path)

        # Access the values
        # self.root_folderpath = parser['Settings']['root_folderpath']
        self.jpg_fileending = parser['Settings']['jpg_fileending']
        self.raw_fileending = parser['Settings']['raw_fileending']
        self.raw_subfoldername = parser['Settings']['subfoldername']
        self.date_pattern = parser['Settings']['date_pattern']
