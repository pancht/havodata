from pages import Page
from selenium.webdriver.common.by import By


class PageLoginStepEmail(Page):
    """HevoData.com Public Login Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    txt_registered_email = (By.CSS_SELECTOR, "input[name='email']")

    btn_continue = (By.XPATH, "//button[contains(text(),'Continue')]")

    # Page methods
    def type_registered_email(self, email):
        """Type registered email"""

        self.send_keys(*self.txt_registered_email, email)

    def click_button_continue(self):
        """Click button 'Continue' """

        self.click(*self.btn_continue)
        self.wait_for_page_to_be_loaded()

        from pages.hevo_data.public.login_pass import PageLoginStepPassword
        return PageLoginStepPassword(driver=self.driver, logger=self.logger)




