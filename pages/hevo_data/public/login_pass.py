from pages import Page
from selenium.webdriver.common.by import By


class PageLoginStepPassword(Page):
    """Public Login Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    txt_password = (By.ID, "password")

    btn_login = (By.XPATH, "//button[text()='Log In']")

    # Page methods
    def type_password(self, password):
        """Type password"""

        self.logger.info(f"Enter password: {'*' * len(password)}")
        self.send_keys(*self.txt_password, password)

    def click_button_login(self):
        """Click button 'Login' """

        self.logger.info("Click Login button")
        self.click(*self.btn_login)
        self.wait_for_page_to_be_loaded()

        from pages.hevo_data.auth.dashboard import PageDashboard
        return PageDashboard(driver=self.driver, logger=self.logger)
