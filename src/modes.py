from enum import Enum

class GlobalMode(Enum):
    NAVIGATION_MODE = 1
    COMMAND_MODE = 2

class NavMode(Enum):
    FOCUSED_MODE = 3
    DIRECTORY_MODE = 4
