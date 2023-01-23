from typing import Optional
import constants
from logger import log

class BasicInstagramUserInformation:
    def __init__(self, username: str) -> None:
        self.username: str = username
        self.id: Optional[str] = None
        self.fullName: Optional[str] = None
        self.isPrivate: Optional[bool] = None
        self.followers: list[BasicInstagramUserInformation] = []
        self.following: list[BasicInstagramUserInformation] = []

    def getCleanFollowing(self) -> dict:
        following = {}
        for index in range(len(self.following)):
            following[self.following[index].username] = {
                constants.USERNAME: self.following[index].username,
                constants.FULL_NAME: self.following[index].fullName,
                constants.IS_PRIVATE: self.following[index].isPrivate
            }
        return following

    def getCleanFollower(self) -> dict:
        follower = {}
        for index in range(len(self.followers)):
            follower[self.followers[index].username] = {
                constants.USERNAME: self.followers[index].username,
                constants.FULL_NAME: self.followers[index].fullName,
                constants.IS_PRIVATE: self.followers[index].isPrivate
            }
        return follower