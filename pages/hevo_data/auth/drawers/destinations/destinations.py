from pages import Page
from selenium.webdriver.common.by import By

from pages.hevo_data.auth.drawers.destinations.overview import PageDestinationOverview


class PageDestinations(Page):
    """Destination Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements

    # Page methods


class PageDestinationsDrawer(Page):
    """Destination Drawer Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    btn_right_arrow = (By.XPATH, "//span[contains(@class, 'hevo-right-arrow')]")

    # Page methods
    def click_button_right_arrow(self):
        """Click Button Right Arrow"""

        self.click(*self.btn_right_arrow)

        return PageDestinationOverview(driver=self.driver, logger=self.logger)


