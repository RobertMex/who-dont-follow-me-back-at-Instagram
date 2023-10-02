from Browser import Browser
import constants
from Instagram import Instagram
from logger import log, logError
from WhoDontFollowBackMeAtInstagram import WhoDontFollowBackMeAtInstagram
import key

def main():
    try:
        log(message=constants.MAIN_MESSAGE)
        browser: Browser = Browser().browser
        ig: Instagram = Instagram(
            username=key.usernameToAuthenticate,
            password=key.passwordToAuthenticate,
            browser=browser
        )
        ig.loginInstagram()
        sourceCode: WhoDontFollowBackMeAtInstagram = WhoDontFollowBackMeAtInstagram(
            username=key.usernameToAnalyze,
            instagram=ig
        )
        sourceCode.analyzeInstagramUser()
        ig.logoutInstagram()
    except Exception as exception:
        logError(message = exception)

if __name__ == '__main__':
    main()