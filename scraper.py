import time
import re
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from jumia.descriptor import PAGE_DESCRIPTION, JumiaContent
from jumia.utils import find_and_close_popup


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


def get_page_links(driver, link_description=PAGE_DESCRIPTION):
    return attribute_matches(
        reg_exp=link_description, elements=driver.find_elements(By.TAG_NAME, "a")
    )


driver = create_chrome_driver(headless=True)

driver.get("https://www.jumia.com.ng/")

time.sleep(5)

find_and_close_popup(driver)

footer = driver.find_element(By.TAG_NAME, "footer")

action_chain = webdriver.ActionChains(driver)

action_chain.scroll_to_element(footer)

anchors_with_matched_links = get_page_links(driver=driver)

# for e in driver.find_elements(By.TAG_NAME, "a"):
#     print(e, e.get_attribute("href"))

jumia_contents = []


def get_pages_contents(
    limits: int | None = None,
    elements=anchors_with_matched_links,
    storage=jumia_contents,
) -> list[JumiaContent]:
    filtered = [e.get_attribute("href") for e in elements]
    for href in filtered[: limits or len(filtered)]:
        try:
            driver.get(href)
            time.sleep(5)
            storage.append(JumiaContent.from_page(driver))
        except Exception as e:
            print(f"failed {e}")
    return storage


storage = get_pages_contents(6)

with open("filename.csv", "w+") as f:
    fieldnames = ["title", "price", "details", "specifications"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for i in storage:
        print(writer.writerow(i.as_dict()))

# search = driver.find_element(By.NAME, "q")
# search.clear()
# search.send_keys("fish")
# search.send_keys(Keys.ENTER)

time.sleep(20)


# print(driver.page_source)

if __name__ == "__main__":
    driver.quit()
