from pages import Page
from selenium.webdriver.common.by import By

from pages.hevo_data.auth.create_pipeline.select_destination import PageSelectDestinationStepOne
from pages.hevo_data.auth.create_pipeline.select_source_type import PageSelectSourceType


class PageSelectObjectsStepOne(Page):
    """Select Objects Step One Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    btn_continue = (By.XPATH, "//button[text()='Continue']")

    # Page methods
    def click_button_continue(self):
        """Click Continue button"""

        self.click(*self.btn_continue)

        self.wait_for_page_to_be_loaded()

        return PageSelectObjectsStepTwo(driver=self.driver, logger=self.logger)


class PageSelectObjectsStepTwo(Page):
    """Select Objects Step Two Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    btn_continue = (By.XPATH, "//button[text()='Continue']")

    # Page methods
    def click_button_continue(self):
        """Click Continue button"""

        self.click(*self.btn_continue)

        self.wait_for_page_to_be_loaded()

        return PageSelectDestinationStepOne(driver=self.driver, logger=self.logger)

