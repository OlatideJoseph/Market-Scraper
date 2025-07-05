import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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


driver = create_chrome_driver()

driver.get("https://www.jumia.com.ng/")

time.sleep(20)

search = driver.find_element(By.NAME, "q")
search.clear()
search.send_keys("fish")
search.send_keys(Keys.ENTER)

time.sleep(20)


print(driver.page_source)

if __name__ == "__main__":
    driver.quit()
