from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class Browser:
    def __init__(self) -> None:
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def getCookies(self) -> list[dict]:
        return self.browser.get_cookies()