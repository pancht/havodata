from pages import Page
from selenium.webdriver.common.by import By

from pages.hevo_data.public.login import PageLoginStepEmail


class PagePublic(Page):
    """Public Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    lnk_login = (By.CSS_SELECTOR, "a[href='/login/']")

    # Page methods
    def go_to_login_page(self):
        """Go To Login Page by clicking over Login link"""

        self.click(*self.lnk_login)

        return PageLoginStepEmail(driver=self.driver, logger=self.logger)