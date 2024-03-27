from pages import Page
from selenium.webdriver.common.by import By


class PageSelectObjectsStepOne(Page):
    """Select Objects Step One Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    btn_mysql_destination_one = (By.XPATH, "//button//h5[text()='MySQL Destination 1']")
    btn_add_destination = (By.XPATH, "//button[@data-id='destination-list-add-new-button']")
    btn_continue = (By.XPATH, "//button[text()='Continue']")

    def is_destination_already_present(self):
        """Check if destination already exists"""

        if self.wait_for_element_to_be_present(*self.btn_mysql_destination_one, wait=5):
            return True

        return False

    # Page methods
    def click_button_continue(self):
        """Click Continue button"""

        self.wait_for_element_to_be_present(*self.btn_continue)
        self.click(*self.btn_continue)
        self.wait_for_page_to_be_loaded()

        self.click(*self.btn_continue)
        self.wait_for_page_to_be_loaded()

        from pages.hevo_data.auth.create_pipeline.select_destination import PageSelectDestinationStepOne
        return PageSelectDestinationStepOne(driver=self.driver, logger=self.logger)

    def click_button_add_destination(self):
        """Click Button Add Destination"""

        self.wait_for_element_to_be_present(*self.btn_add_destination)
        self.click(*self.btn_add_destination)

        from pages.hevo_data.auth.create_pipeline.select_destination_type import PageSelectDestinationType
        return PageSelectDestinationType(driver=self.driver, logger=self.logger)


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

        from pages.hevo_data.auth.create_pipeline.select_destination import PageSelectDestinationStepOne
        return PageSelectDestinationStepOne(driver=self.driver, logger=self.logger)
