from pages import Page
from selenium.webdriver.common.by import By


class PageSelectDestinationType(Page):
    """Select Destination Type Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    btn_mysql = (By.XPATH, "//button//h5[text()='MySQL']")

    # Page methods
    def click_button_mysql(self):
        """Click Button MySql"""

        self.click(*self.btn_mysql)
        self.wait_for_page_to_be_loaded()


