from typing import Optional
from requests import Response, Session
from urllib.parse import quote
import json 
from BasicInstagramUserInformation import BasicInstagramUserInformation
import constants
from Instagram import Instagram
from logger import log

class WhoDontFollowBackMeAtInstagram:
    def __init__(self, username: str, instagram: Instagram) -> None:
        self.instagramUser: BasicInstagramUserInformation = (
            self._setupInstagramUserInformation(username=username)
        )
        self.instagram: Instagram = instagram
        self.session: Session = self._setupCorrectUserAgent()
        self.usersDontFollowMeBack: list[BasicInstagramUserInformation] = []
        self.usertsIDontFollowBack: list[BasicInstagramUserInformation] = []

    def _setupCorrectUserAgent(self) -> Session:
        session = Session()
        instagram_user_agent = self.instagram.browser.execute_script(
            constants.COMMAND_USER_AGENT_SELENIUM
        )
        session.headers.update({constants.USER_AGENT: instagram_user_agent})
        for cookie in self.instagram.browser.get_cookies():
            session.cookies.set(
                name=cookie[constants.NAME], 
                value=cookie[constants.VALUE], 
                domain=cookie[constants.DOMAIN])
        return session

    def _setupInstagramUserInformation(self, username: str) -> BasicInstagramUserInformation:
        return BasicInstagramUserInformation(username = username)

    def analyzeInstagramUser(self) -> None:
        self._logAnalysisMessage()
        self._setUserIdToInstagramUser()
        self._setFollowersFromUser()
        self._setFollowingsFromUser()
        self._usersDontFollowmeBack()

    def _logAnalysisMessage(self) -> None:
        message: str = constants.STARTING_MESSAGE + self.instagramUser.username
        log(message = message)

    def _setUserIdToInstagramUser(self) -> None:
        userQueryResponse: Response = self._getQueryResponseUserSearch()
        userQueryJson: dict = self._transformUserQueryResponseToJson(
            userQueryResponse = userQueryResponse
        )
        self.instagramUser.id = self._getUserIdFromQueryJson(userQueryResponseJson=userQueryJson)

    def _getQueryResponseUserSearch(self) -> Response: 
        return self.session.get(
            constants.URL_SEARCH_INSTAGRAM + self.instagramUser.username
        )

    def _transformUserQueryResponseToJson(self, userQueryResponse: dict) -> dict:
        return userQueryResponse.json()

    def _getUserIdFromQueryJson(self, userQueryResponseJson: dict) -> list:
        return self._getUserIdFromUserList(
            userListFromSearch = userQueryResponseJson[constants.USERS]
        ) 

    def _getUserIdFromUserList(self, userListFromSearch: list) -> dict:
        return self._getUserIdFromMainUser(
            mainUserFromSearch = userListFromSearch[constants.FIRST_POSITION]
        ) 

    def _getUserIdFromMainUser(self, mainUserFromSearch: dict) -> dict:
        return self._getUserIdFromMainUserInformation(
            mainUserInformation = mainUserFromSearch[constants.USER]
        ) 

    def _getUserIdFromMainUserInformation(self, mainUserInformation: dict) -> str:
        return mainUserInformation[constants.PK]

    def _setFollowersFromUser(self) -> None:
        after: Optional[str] = None
        hasNextPage: bool = True

        while hasNextPage:
            followerQuery: dict = self._getFollowersJsonQuery(after = after)
            hasNextPage: bool = self._hasFollowerNextPage(followerQuery = followerQuery)
            after: Optional[str] = self._followerAfter(followerQuery = followerQuery)
            for node in self._getFollowerNodes(followerQuery = followerQuery):
                user = node[constants.NODE]
                userInformation: BasicInstagramUserInformation = BasicInstagramUserInformation(
                    username=user[constants.USERNAME]
                )
                userInformation.fullName = user[constants.FULL_NAME]
                userInformation.isPrivate = user[constants.IS_PRIVATE]
                self.instagramUser.followers.append(userInformation)

    def _setFollowingsFromUser(self) -> None:
        after: Optional[str] = None
        hasNextPage: bool = True

        while hasNextPage:
            followingQuery: dict = self._getFollowingsJsonQuery(after = after)
            hasNextPage: bool = self._hasFollowingNextPage(followingQuery = followingQuery)
            after: Optional[str] = self._followingAfter(followingQuery = followingQuery)
            for node in self._getFollowingNodes(followingQuery=followingQuery):
                user = node[constants.NODE]
                userInformation: BasicInstagramUserInformation = BasicInstagramUserInformation(
                    username=user[constants.USERNAME]
                )
                userInformation.fullName = user[constants.FULL_NAME]
                userInformation.isPrivate = user[constants.IS_PRIVATE]
                self.instagramUser.following.append(userInformation)

    def _getFollowersJsonQuery(self, after: Optional[str]) -> dict:
        url: str = self._getFollowerUrl(after = after)
        responseQuery: Response = self.session.get(url)
        return responseQuery.json()

    def _getFollowingsJsonQuery(self, after: Optional[str]) -> dict:
        url: str = self._getFollowingUrl(after = after)
        responseQuery: Response = self.session.get(url)
        return responseQuery.json()

    def _getFollowerUrl(self, after: Optional[str]) -> str:
        return constants.URL_QUERY_FOLLOWERS + self._getEncodedUrlPart(after=after)

    def _getFollowingUrl(self, after: Optional[str]) -> str:
        return constants.URL_QUERY_FOLLOWINGS + self._getEncodedUrlPart(after=after)

    def _getEncodedUrlPart(self, after) -> str:
        urlComponents: dict = self._getURLInstagramComponents(after=after)
        return self._encodeURLComponents(obj = urlComponents)

    def _encodeURLComponents(self, obj: dict) -> str:
        return quote(
            string = json.dumps(obj=obj), 
            safe = constants.SAFE_CHARS_ENCODER
        )

    def _getURLInstagramComponents(self, after) -> dict:
        return {
            constants.ID: self.instagramUser.id,
            constants.INCLUDE_REEL : True,
            constants.FETCH_MUTUAL : True,
            constants.FIRST : 50,
            constants.AFTER : after
        }

    def _hasFollowerNextPage(self, followerQuery: dict) -> bool:
        return (
            followerQuery
                [constants.DATA]
                [constants.USER]
                [constants.EDGE_FOLLOWED_BY]
                [constants.PAGE_INFO]
                [constants.HAS_NEXT_PAGE]
        )

    def _hasFollowingNextPage(self, followingQuery: dict) -> bool:
        return (
            followingQuery
                [constants.DATA]
                [constants.USER]
                [constants.EDGE_FOLLOW]
                [constants.PAGE_INFO]
                [constants.HAS_NEXT_PAGE]
        )

    def _followerAfter(self, followerQuery: dict) -> bool:
        return (
            followerQuery
                [constants.DATA]
                [constants.USER]
                [constants.EDGE_FOLLOWED_BY]
                [constants.PAGE_INFO]
                [constants.END_CURSOR]
        )

    def _followingAfter(self, followingQuery: dict) -> bool:
        return (
            followingQuery
                [constants.DATA]
                [constants.USER]
                [constants.EDGE_FOLLOW]
                [constants.PAGE_INFO]
                [constants.END_CURSOR]
        )

    def _getFollowingNodes(self, followingQuery: dict) -> list[dict]:
        return (
            followingQuery
                [constants.DATA]
                [constants.USER]
                [constants.EDGE_FOLLOW]
                [constants.EDGES]
        )

    def _getFollowerNodes(self, followerQuery: dict) -> list[dict]:
        return (
            followerQuery
                [constants.DATA]
                [constants.USER]
                [constants.EDGE_FOLLOWED_BY]
                [constants.EDGES]
        )

    #TODO Optimize this important function
    def _usersDontFollowmeBack(self) -> None:
        followingDict = self.instagramUser.getCleanFollowing()
        followerDict = self.instagramUser.getCleanFollower()
        countusersDontFollowmeBack = 0
        for username in followingDict:
            if username not in followerDict:
                log(message = followingDict[username])
                countusersDontFollowmeBack += 1
        message: str = constants.TOTAL_MESSAGE + str(countusersDontFollowmeBack)
        log(message = message)