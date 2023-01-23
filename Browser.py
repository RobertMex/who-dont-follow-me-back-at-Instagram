from selenium import webdriver

class Browser:
    def __init__(self) -> None:
        self.browser = webdriver.Chrome()

    def getCookies(self) -> list[dict]:
        return self.browser.get_cookies()