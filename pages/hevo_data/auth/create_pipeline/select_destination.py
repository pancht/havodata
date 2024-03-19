from pages import Page
from selenium.webdriver.common.by import By

from pages.hevo_data.auth.pipelines.overview import PagePipelineOverview


class PageSelectDestinationStepOne(Page):
    """Select Destination Step One Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    btn_mysql = (By.XPATH, "//button//h5[text()='MySQL']")

    # Page methods
    def click_button_mysql(self):
        """Click button MySql"""

        self.click(*self.btn_mysql)

        self.wait_for_page_to_be_loaded()

        return PageSelectDestinationStepTwo(driver=self.driver, logger=self.logger)


class PageSelectDestinationStepTwo(Page):
    """Select Destination Step Two Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    txt_destination_tbl_prefix = (By.CSS_SELECTOR, "input[id='destinationPrefix']")
    btn_scheduled_12_hours = (By.XPATH, "//button[text()='12 Hrs']")

    btn_continue = (By.CSS_SELECTOR, "button[type='submit']")

    # Page methods
    def type_destination_tbl_prefix(self, prefix):
        """Type destination table prefix"""

        self.send_keys(*self.txt_destination_tbl_prefix, prefix)

    def select_scheduled_12_hours(self):
        """Select Scheduled 12 Hours"""
        self.click(*self.btn_scheduled_12_hours)

    def click_continue(self):
        """Click Continue button"""
        self.click(*self.btn_continue)
        self.wait_for_page_to_be_loaded()

        return PagePipelineOverview(driver=self.driver, logger=self.logger)


