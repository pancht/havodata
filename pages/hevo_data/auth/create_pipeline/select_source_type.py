from pages import Page
from selenium.webdriver.common.by import By

from pages.hevo_data.auth.create_pipeline.configure_mysql_source import PageConfigureMySqlSource


class PageSelectSourceType(Page):
    """Select Source Type Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    btn_mysql = (By.XPATH, "//button//h5[text()='MySQL']")

    # Page methods
    def select_source_type_mysql(self):
        """Click MySql button"""

        self.click(*self.btn_mysql)
        self.wait_for_page_to_be_loaded()

        return PageConfigureMySqlSource(driver=self.driver, logger=self.logger)