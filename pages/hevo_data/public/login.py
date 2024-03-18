from pages import Page
from selenium.webdriver.common.by import By

from pages.hevo_data.public.login_pass import PageLoginStepPassword


class PageLoginStepEmail(Page):
    """Public Login Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    txt_registered_email = (By.XPATH, "//h1[text()='Log in to your Account']/..//input[@name='email']")

    btn_continue = (By.XPATH, "//span[contains(text(),'Continue')]/..")

    # Page methods
    def type_registered_email(self, email):
        """Type registered email"""

        self.send_keys(*self.txt_registered_email, email)

    def click_button_continue(self):
        """Click button 'Continue' """

        self.click(*self.btn_continue)

        return PageLoginStepPassword(driver=self.driver, logger=self.logger)



