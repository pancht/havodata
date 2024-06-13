from pages import Page
from selenium.webdriver.common.by import By

from pages.hevo_data.auth.drawers.pipelines.drawer_pipelines import PageDrawerPipelines


class PageDashboard(Page):
    """Dashboard Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    css_loc_drawer_pipeline_exists = "[href='/model?drawer=pipelines']"
    lnk_drawer_pipeline_exists = (By.CSS_SELECTOR, css_loc_drawer_pipeline_exists)
    lnk_drawer_pipelines = (By.CSS_SELECTOR, f"{css_loc_drawer_pipeline_exists}, [href='/pipeline?drawer=pipelines']")

    btn_create_pipeline = (By.XPATH, "//button[contains(text(),'Create Pipeline')]")
    btn_create_on_drawer_pipeline = (By.CSS_SELECTOR, "button[data-id='pipeline-drawer-create-button']")
    # Page methods

    def pipeline_exists(self):
        self.wait_for_page_to_be_loaded()

        if self.is_displayed(*self.btn_create_on_drawer_pipeline):
            return True
        else:
            return False

        # if self.is_displayed(*self.btn_create_pipeline):
        #     if not self.is_displayed(*self.lnk_drawer_pipeline_exists):
        #         return True
        #     else:
        #         return False
        #
        # return True

    def click_link_drawer_pipelines(self) -> PageDrawerPipelines | None:
        self.logger.info("Click Pipelines drawer link")
        self.click(*self.lnk_drawer_pipelines)

        self.wait_for_page_to_be_loaded()
        self.close_product_tour_popup()
        self.wait_for_page_to_be_loaded()

        if self.pipeline_exists():
            return PageDrawerPipelines(self.driver, self.logger)
        else:
            self.wait_for_page_to_be_loaded()
            return None

    def click_button_create_pipeline(self):
        """Click Create Pipeline button"""

        self.close_product_tour_popup()

        # self.click(*self.lnk_drawer_pipelines)
        page = self.click_link_drawer_pipelines()
        # self.wait_for_page_to_be_loaded()

        # Start Test code
        if page is None:
            self.logger.info("Pipeline not found")
            # self.close_product_tour_popup()
            self.is_displayed(*self.btn_create_pipeline)
            self.logger.info("Click Create Pipeline button")
            self.click(*self.btn_create_pipeline)
            self.wait_for_page_to_be_loaded()

            from pages.hevo_data.auth.create_pipeline.select_source_type import PageSelectSourceType
            return PageSelectSourceType(driver=self.driver, logger=self.logger)
        else:
            # pipelines exist
            self.logger.info("Pipeline found")
            pipeline_count = page.get_pipelines_count()
            print(pipeline_count)

            page.click_button_create()

            from pages.hevo_data.auth.create_pipeline.select_source_type import PageSelectSourceType
            return PageSelectSourceType(driver=self.driver, logger=self.logger)