import time
import constants

def log(message: str) -> None:
    print(time.ctime(), message)

def logError(message: str) -> None:
    print(time.ctime(), constants.ERROR, message)