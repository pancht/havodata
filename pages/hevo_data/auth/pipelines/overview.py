from pages import Page
from selenium.webdriver.common.by import By


class PagePipelineOverview(Page):
    """Select Destination Step Two Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    btn_pipeline_header_view_more = (By.CSS_SELECTOR, "header button .hevo-more-vertical")

    # Page methods
    def click_button_run_now_pipeline_header(self):
        """Click View More button from Pipeline Header view"""
        self.click(*self.btn_pipeline_header_view_more)
        self.wait_for_page_to_be_loaded()

        ico_run_now = (By.CSS_SELECTOR, "[iconname='run-now']")
        self.click(*ico_run_now)
        self.wait_for_page_to_be_loaded()

        status_check = (By.XPATH,
                        "//div[text()='Started Loading Events']/../..//span[contains(@class, 'hevo-checked-tick')]")
        self.wait_for_element_to_be_present(*status_check, 60)

        self.wait_for_page_to_be_loaded()

