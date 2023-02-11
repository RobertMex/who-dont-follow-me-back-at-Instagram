from typing import Optional
import constants

class BasicInstagramUserInformation:
    def __init__(self, username: str) -> None:
        self.username: str = username
        self.id: Optional[str] = None
        self.fullName: Optional[str] = None
        self.isPrivate: Optional[bool] = None
        self.followers: list[BasicInstagramUserInformation] = []
        self.following: list[BasicInstagramUserInformation] = []

    def getCleanFollowing(self) -> dict:
        return self.getCleanInstagramUsers(self.following)

    def getCleanFollower(self) -> dict:
        return self.getCleanInstagramUsers(self.followers)

    def getCleanInstagramUsers(self, listUser: list) -> dict:
        dictInstagramUsers: dict = {}
        for index in range(len(listUser)):
            dictInstagramUsers[listUser[index].username] = {
                constants.USERNAME: listUser[index].username,
                constants.FULL_NAME: listUser[index].fullName,
                constants.IS_PRIVATE: listUser[index].isPrivate
            }
        return dictInstagramUsers