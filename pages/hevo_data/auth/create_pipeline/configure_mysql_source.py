from pages import Page
from selenium.webdriver.common.by import By


class PageConfigureMySqlSource(Page):
    """Configure MySql Source Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    txt_host = (By.CSS_SELECTOR, "input[name='host']")

    # Page methods
    def select_source_type_mysql(self):
        """Click MySql button"""

        self.click(*self.btn_mysql)

