import re
import logging
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FireFoxWebDriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__,)
logger.setLevel(logging.INFO)

WEBDRIVERS = WebDriver | FireFoxWebDriver


def create_firefox_driver(headless=False):
    """Creates A Driver For Firefox"""
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.firefox.service import Service

    installed = GeckoDriverManager().install()
    service = Service(executable_path=installed)

    option = webdriver.FirefoxOptions()

    if headless:
        option.add_argument("--headless")

    driver = webdriver.Firefox(service=service)

    return driver


def create_chrome_driver(headless=False):
    """Creates A Driver For Chrome"""
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service

    option = webdriver.ChromeOptions()
    if headless:
        option.add_argument("--headless")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=option)
    return driver


def element_attribute_matches(
    element: WebElement, attr: str = "href", reg_exp: str = r"*"
):
    try:
        return bool(re.match(reg_exp, element.get_attribute(attr)))
    except StaleElementReferenceException as e:
        logger.warning("Got a StaleReferenceException %r" % e, exc_info=True)
        return False


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
    """This function assumes you gotten to cloudfare iframe or the main document"""
    import time

    wait = WebDriverWait(driver, 100)
    shadow = driver.find_element(By.CSS_SELECTOR, "body").shadow_root

    print(shadow, "shadow_root")

    try:
        wait._driver = shadow
        checkbox = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox']"))
        )
        print("Found Check Box")

        checkbox.click()

        time.sleep(25)
        print("Captcha Clicked")
        return checkbox
    except NoSuchElementException:
        return None
    except AttributeError:
        return None
    except TypeError:
        return None
    finally:
        wait._driver = driver


def verify_cloudfare_captcha(driver: WEBDRIVERS):
    wait = WebDriverWait(driver, 100)
    main_element = wait.until(EC.presence_of_element_located((By.ID, "vVgbN6")))
    wait._driver = main_element
    div = wait.until(EC.presence_of_element_located((By.TAG_NAME, "div")))
    div = div.find_element(By.TAG_NAME, "div") if div else div
    shaow_root1 = div.shadow_root
    wait._driver = shaow_root1
    frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
    print(frame)
    print(frame.screenshot("frame-screenshot.png"))
    driver.switch_to.frame(frame)
    checkbox = cloudfare_captcha(driver)
    print(checkbox)
    driver.switch_to.default_content()
    return driver


def verify_cloudfare_captcha2(driver: WEBDRIVERS):
    try:
        frame = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//iframe[contains(@title, 'challenge') or contains(@src, 'cf-challenge')]",
                )
            )
        )
        print("[INFO] Captcha iframe found.")

        driver.switch_to.frame(frame)

        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='checkbox' or @id='cf-challenge-checkbox']")
            )
        )
        print("[INFO] Captcha checkbox located:", checkbox)

        driver.switch_to.default_content()
        return checkbox  # optionally return checkbox or status
    except Exception as e:
        print("[ERROR] Failed to verify Cloudflare CAPTCHA:", e)
        driver.switch_to.default_content()
        return None
