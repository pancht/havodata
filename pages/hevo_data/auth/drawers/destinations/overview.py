from pages import Page
from selenium.webdriver.common.by import By

from pages.hevo_data.auth.drawers.destinations.destinations import PageDestinations


class PageDestinationOverview(Page):
    """Destination Overview Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    btn_header_three_dots = (By.XPATH, "//header//button//span[contains(@class,'hevo-more-vertical')]")
    lst_delete_option = (By.XPATH, "//li[text()='Delete']")
    btn_yes_delete_this_dest = (By.XPATH, "//button[text()='Yes, delete this Destination']")

    # Page methods
    def click_delete_destination(self):
        """Click Delete Destination Option"""

        self.wait_for_element_to_be_present(*self.btn_header_three_dots, wait=20)
        self.click(*self.btn_header_three_dots)

        self.wait_for_element_to_be_present(*self.lst_delete_option, wait=3)
        self.click(*self.lst_delete_option)

        self.wait_for_element_to_be_present(*self.btn_yes_delete_this_dest, wait=4)
        self.click(*self.btn_yes_delete_this_dest)

        return PageDestinations(driver=self.driver, logger=self.logger)





