from Browser import Browser
import constants
from logger import logError
from selenium.webdriver.common.by import By
import time

class Instagram:
    def __init__(self, username: str, password: str, browser: Browser) -> None:
        self.username: str = username
        self.password: str = password
        self.browser: Browser = browser

    def loginInstagram(self) -> None:
        try:
            self._openInstagram()
            self._writeUsernameLoginInstagram()
            self._writePasswordLoginInstagram()
            self._clickLoginInstagram()
            self._resetUsernameAndPasswordInstagram()
        except Exception as exception:
            logError(message = exception)
            self._resetUsernameAndPasswordInstagram()
            self.logoutInstagram()
            time.sleep(5)

    def _openInstagram(self) -> None:
        self.browser.get(constants.URL_INSTAGRAM)
        time.sleep(10)

    def _writeUsernameLoginInstagram(self) -> None:
        self.browser.find_element(By.NAME, constants.USERNAME).click()
        time.sleep(2)
        self.browser.find_element(By.NAME, constants.USERNAME).send_keys(self.username)
        time.sleep(2)

    def _writePasswordLoginInstagram(self) -> None:
        self.browser.find_element(By.NAME, constants.PASSWORD).click()
        time.sleep(2)
        self.browser.find_element(By.NAME, constants.PASSWORD).send_keys(self.password)
        time.sleep(2)

    def _clickLoginInstagram(self) -> None:
        self.browser.find_element(By.CSS_SELECTOR, constants.CSS_SUBMIT).click()
        time.sleep(10)
        
    def logoutInstagram(self) -> None:
        self.browser.get(constants.URL_INSTAGRAM_LOGOUT)
        time.sleep(5)
        self.browser.quit()

    def _resetUsernameAndPasswordInstagram(self) -> None:
        self.username = constants.USERNAME
        self.password = constants.PASSWORD