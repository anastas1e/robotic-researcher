import re
import time
from datetime import datetime

from RPA.Browser.Selenium import Selenium
from SeleniumLibrary.errors import ElementNotFound
from selenium.webdriver.common.by import By


class Robot:
    browser = None
    driver = None

    def __init__(self, name):
        self.name = name

    def open_browser(self, url):
        if not self.browser:
            self.browser = Selenium()
            self.browser.open_available_browser(url)
            self.driver = self.browser.driver

    def close_browser(self):
        if self.browser:
            self.browser.close_browser()

    def introduce(self, topic="scientists"):
        """
        Introduce robot and topic to share.
        """
        msg = f"Hello, my name is {self.name} \n"
        msg += (
            f"I'm a very special robot that can tell you lots of interesting facts!\n"
        )
        msg += f"Today I'd like to share with you some information about {topic}.\n"
        print(msg)

    def open_wiki_page(self, person_name):
        """
        Open Wiki page according to name of the person.
        """
        search_input = self.driver.find_element(By.ID, "searchform").find_element(
            By.TAG_NAME, "input"
        )
        search_input.send_keys(person_name)
        time.sleep(7)
        self.driver.find_element(By.CSS_SELECTOR, "#searchform > div > button").click()

    def extract_lifetime_dates(self):
        """
        Extract date of birth and death (if relevant).
        """

        def get_date_element_by_keyword(keyword):
            try:
                element = self.browser.find_element(
                    f"//th[@class='infobox-label' and text()='{keyword}']/following-sibling::td[@class='infobox-data']"
                ).text
            except ElementNotFound:
                return ""
            return element

        patterns = [r"\d{1,2}\s+\w+\s+\d{4}", r"\b\w+\s+\d{1,2},\s+\d{4}\b"]
        combined = "(" + ")|(".join(patterns) + ")"
        keywords = ["Born", "Died"]

        date_elements = list(map(get_date_element_by_keyword, keywords))
        lifetime_dates = [
            re.search(combined, date_element) for date_element in date_elements
        ]
        birth_date = lifetime_dates[0].group() if lifetime_dates[0] else None
        death_date = lifetime_dates[1].group() if lifetime_dates[1] else None

        return birth_date, death_date

    def extract_first_paragraph(self):
        """
        Extract the first paragraph from the wiki page.
        """
        first_paragraph = self.driver.find_element(
            By.XPATH, "//*[@id='mw-content-text']/div[1]/p[2]"
        )
        if not first_paragraph:
            first_paragraph = self.driver.find_element(
                By.XPATH, "//*[@id='mw-content-text']/div[1]/p[3]"
            )
        return first_paragraph.text

    def calculate_age(self, birth, death):
        """
        Calculate age based on birth date and death date. In case person is still alive, return current age based on
        current year and year of birth.
        """
        birth_object = self.convert_date_string_to_obj(birth).year
        death_object = (
            self.convert_date_string_to_obj(death).year
            if death
            else datetime.now().year
        )

        return death_object - birth_object

    def convert_date_string_to_obj(self, date_str):
        """
        Convert date string to date object by handling two possible options of the date string.
        """
        try:
            date_object = datetime.strptime(date_str, "%d %B %Y")
        except ValueError:
            date_object = datetime.strptime(date_str, "%B %d, %Y")
        return date_object

    def generate_info(self, person):
        """
        Generate the main part of the report about a person.
        """
        self.open_wiki_page(person)
        time.sleep(5)
        birth, death = self.extract_lifetime_dates()
        person_age = self.calculate_age(birth, death)
        brief_info = self.extract_first_paragraph()
        return birth, death, person_age, brief_info
