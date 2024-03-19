from pages import Page
from selenium.webdriver.common.by import By


class PagePipelineOverview(Page):
    """Select Destination Step Two Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    btn_pipeline_header_view_more = (By.XPATH, "//header//*[contains(@class, 'hevo-more-vertical')]/..")

    btn_pipeline_delete = (By.CSS_SELECTOR, "[iconname='delete']")

    # Page methods
    def click_button_run_now_pipeline_header(self):
        """Click View More button from Pipeline Header view"""
        status_check = (By.XPATH,
                        "//div[text()='Started Loading Events']/../..//span[contains(@class, 'hevo-checked-tick')]")

        btn_maybe_later = (By.XPATH, "//button[text()='Maybe Later']")

        if not self.wait_for_element_to_be_disappeared(*btn_maybe_later, wait=15):
            self.click(*btn_maybe_later)

        self.wait_for_element_to_be_present(*status_check, 10 * 60)

        self.click(*self.btn_pipeline_header_view_more)
        self.wait_for_page_to_be_loaded()

        ico_run_now = (By.CSS_SELECTOR, "[iconname='run-now']")
        self.click(*ico_run_now)
        self.wait_for_page_to_be_loaded()

        for count in range(15):
            if self.wait_for_element_to_be_present(*status_check, 10 * 60):
                break
            self.refresh()
            continue

        self.wait_for_page_to_be_loaded()

    def click_button_delete_pipeline(self):
        """Click Button Delete Pipeline"""

        self.click(*self.btn_pipeline_header_view_more)
        self.wait_for_page_to_be_loaded()

        self.click(*self.btn_pipeline_delete)
        self.wait_for_page_to_be_loaded()


