from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FireFoxWebDriver
from selenium.common.exceptions import NoSuchElementException

WEBDRIVERS = WebDriver | FireFoxWebDriver


def find_popup(driver: WEBDRIVERS, by=By.CLASS_NAME, value="popup"):
    """Finds Popups"""

    try:
        return driver.find_element(by, value)
    except NoSuchElementException:
        return None


def find_and_close_popup(driver: WEBDRIVERS, **kwargs):
    """This Functions Finds And Closes The Popup On the Page"""
    web_element = find_popup(driver, **kwargs)
    if web_element:
        try:
            close_button = web_element.find_element(By.CLASS_NAME, "cls")
            if close_button:
                close_button.click()
        except NoSuchElementException:
            return None
