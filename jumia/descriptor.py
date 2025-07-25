import re
from typing import Any, List
from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FireFoxWebDriver
from selenium.webdriver.support import expected_conditions as EC

from utils import WEBDRIVERS

PAGE_DESCRIPTION = r"(https?://)?(www\.jumia\.com\.ng)?/[a-zA-z0-9\-]+(\.html)$"
compiled_page_description = re.compile(PAGE_DESCRIPTION)


def match_page(page: WEBDRIVERS):
    return bool(compiled_page_description.match(page.current_url))


class JumiaPageDescription:
    title_tag_by: str = By.XPATH
    title_tag_value: str = "//h1[starts-with(@class, '-fs20 ')]"
    price_tag_by: str = By.CLASS_NAME
    price_tag_value: str = "-fs24"
    details_tag_by: str = By.CLASS_NAME
    details_tag_value: str = "-sc"
    specifications_tag_by: str = By.XPATH
    specifications_tag_value: str = "//div[@class='markup -pam']"


class JumiaContent:
    """Describes The Fields Needed To Be Stored"""

    title: str
    price: str
    details: str
    specifications: str | None
    page: WEBDRIVERS | None

    def __init__(self, title, price, details, specifications=None):
        self.title = title
        self.price = price
        self.details = details
        self.specifications = specifications

    @classmethod
    def from_page(
        cls,
        page: WebDriver | FireFoxWebDriver,
        page_description: JumiaPageDescription | Any = JumiaPageDescription,
    ):
        assert match_page(page)
        description = page_description
        return cls(
            title=page.find_element(
                description.title_tag_by, description.title_tag_value
            ).text,
            price=page.find_element(
                description.price_tag_by, description.price_tag_value
            ).text,
            details=page.find_element(
                description.details_tag_by, description.details_tag_value
            ).text,
            specifications=page.find_element(
                description.specifications_tag_by, description.specifications_tag_value
            ).text,
        )

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.title} - {self.price}>\n{("" or self.details)[:15]}"

    def __repr__(self):
        return f"{str(self)!r}"

    def as_list(self):
        """title, price, details, specifications"""
        return [self.title, self.price, self.details, self.specifications]

    def as_dict(self):
        """title, price, details, specifications"""
        return {
            "title": self.title,
            "price": self.price,
            "details": self.details,
            "specifications": self.specifications,
        }

    def write_to_as_csv(self, buffer):
        """Write To A Buffer"""


class JumiaCommentDescription:
    header_tag_by = By.CSS_SELECTOR
    header_tag_value = "h3.-m.-fs16.-pvs"
    comment_tag_by = By.CSS_SELECTOR
    comment_tag_value = "p.-pvs"
    rating_tag_by = By.XPATH
    rating_tag_value = "//div[starts-with(@class, 'stars')]"
    date_tag_by = By.XPATH
    date_tag_value = "//div/div/span[@class='-prs']"
    author_tag_by = "//div/div/span[2]"


@dataclass
class JumiaCommentContent:
    """Gets Jumia Comment Contents"""

    header: str
    comment: str
    rating: str
    date: str
    author: str

    @classmethod
    def from_page(cls, page: WEBDRIVERS, comment_description: JumiaCommentDescription):
        assert match_page(page)
        return cls(header="")

    @staticmethod
    def find_comment_section(page: WEBDRIVERS):
        return WebDriverWait(page, 20).until(
            EC.presence_of_element_located((By.XPATH, "//section[2]"))
        )

    @staticmethod
    def find_comment_section_on_catalog_page(page: WEBDRIVERS):
        return WebDriverWait(page, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//main/div/div/section[@class='card']")
            )
        )

    @staticmethod
    def get_all_comments_elements(element: WebElement) -> List[WebElement]:
        return WebDriverWait(element, 10).until(
            EC.presence_of_all_elements_located(
                By.CSS_SELECTOR, "article.-pvs.-hr._bet"
            )
        )

    @staticmethod
    def get_catalog_next(page: WEBDRIVERS):
        return WebDriverWait(page, 10).until(
            EC.element_to_be_clickable(
                By.XPATH, "//a[@class='pg'][@aria-label='Next Page']"
            )
        )
