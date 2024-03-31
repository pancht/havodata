from pages import Page
from selenium.webdriver.common.by import By


class PageDashboard(Page):
    """Dashboard Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    lnk_pipelines = (By.CSS_SELECTOR, "[href='/pipeline?drawer=pipelines']")

    btn_create_pipeline = (By.XPATH, "//button[contains(text(),'Create Pipeline')]")

    # Page methods
    def click_button_create_pipeline(self):
        """Click Create Pipeline button"""

        self.close_product_tour_popup()

        self.click(*self.lnk_pipelines)
        self.wait_for_page_to_be_loaded()

        self.close_product_tour_popup()
        print(self.is_displayed(*self.btn_create_pipeline))
        self.click(*self.btn_create_pipeline)
        self.wait_for_page_to_be_loaded()

        from pages.hevo_data.auth.create_pipeline.select_source_type import PageSelectSourceType
        return PageSelectSourceType(driver=self.driver, logger=self.logger)

