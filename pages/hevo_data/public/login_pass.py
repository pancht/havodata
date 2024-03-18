from pages import Page
from selenium.webdriver.common.by import By

from pages.hevo_data.auth.dashboard import PageDashboard


class PageLoginStepPassword(Page):
    """Public Login Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    text_password = (By.XPATH, "//input[@name='password']")

    btn_login = (By.XPATH, "//button[text()='Log In']")

    # Page methods
    def type_password(self, password):
        """Type password"""

        self.send_keys(*self.text_password, password)

    def click_button_login(self):
        """Click button 'Login' """

        self.click(*self.btn_login)

        return PageDashboard(driver=self.driver, logger=self.logger)