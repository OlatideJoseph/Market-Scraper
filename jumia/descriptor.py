import csv
import io
from typing import Any
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FireFoxWebDriver

PAGE_DESCRIPTION = r"(https?://)?(www\.jumia\.com\.ng)?/[a-zA-z0-9\-]+(\.html)$"


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
