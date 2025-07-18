import re
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FireFoxWebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

WEBDRIVERS = WebDriver | FireFoxWebDriver


def element_attribute_matches(
    element: WebElement, attr: str = "href", reg_exp: str = r"*"
):
    return bool(re.match(reg_exp, element.get_attribute(attr)))


def attribute_matches(
    attr: str = "href", reg_exp: str = r"*", elements: list[WebElement] = []
):
    """
    Returns The Elements That matches The Specified Attributes And Pattern
    """

    return [
        element
        for element in elements
        if element_attribute_matches(element, attr, reg_exp)
    ]


def cloudfare_captcha(driver: WEBDRIVERS):
    import time

    wait = WebDriverWait(driver, 20)
    try:
        checkbox = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[starts-with(@id, 'verifying')]//input[@type='checkbox']",
                )
            )
        )
        time.sleep(25)
        return checkbox
        return driver.find_element(
            By.XPATH, "//*[starts-with(@id, 'verifying')]"
        ).find_element(By.XPATH, "//input[@type='checkbox']")
    except NoSuchElementException:
        return None
    except AttributeError:
        return None
    except TypeError:
        return None


def verify_cloudfare_captcha(driver: WEBDRIVERS):
    import time
    time.sleep(20)
    frame = driver.find_element(By.XPATH, "//*[@id=\"cf-chl-widget-x13kc\"]")
    print(frame)
    driver.switch_to.frame(frame)
    checkbox = cloudfare_captcha(driver)
    print(checkbox)
    driver.switch_to.default_content()
    return driver



def verify_cloudfare_captcha2(driver: WEBDRIVERS):
    try:
        frame = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//iframe[contains(@title, 'challenge') or contains(@src, 'cf-challenge')]"
            ))
        )
        print("[INFO] Captcha iframe found.")
        
        driver.switch_to.frame(frame)

        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//input[@type='checkbox' or @id='cf-challenge-checkbox']"
            ))
        )
        print("[INFO] Captcha checkbox located:", checkbox)

        driver.switch_to.default_content()
        return checkbox  # optionally return checkbox or status
    except Exception as e:
        print("[ERROR] Failed to verify Cloudflare CAPTCHA:", e)
        driver.switch_to.default_content()
        return None

