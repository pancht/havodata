from pages import Page
from selenium.webdriver.common.by import By


class PageDrawerPipelines(Page):
    """
    Drawer Pipelines Page Class
    """

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page Elements
    btn_create = (By.CSS_SELECTOR, "button[data-id='pipeline-drawer-create-button']")

    drawer_filters = (By.CSS_SELECTOR, "div[class='drawer-filters-container']")

    txt_pipelines_count = (By.CSS_SELECTOR, f"{drawer_filters[1]} div.text-secondary")

    # Page Methods
    def get_pipelines_count(self):
        """Get Pipelines Count"""

        if self.is_displayed(*self.txt_pipelines_count):
            pipelines_count = self.find_element(*self.txt_pipelines_count).text
            self.logger.info(f"Pipelines Count = {pipelines_count}")
            return self.find_element(*self.txt_pipelines_count).text

    def pipeline_exists(self) -> bool:
        """
        Test if any pipeline exists or not.

        :return: True if at-least a pipeline exists.
        """

        if self.is_displayed(*self.btn_create_pipeline):
            return True

        return False

    def click_button_create(self):

        self.logger.info("Click button Create")
        self.click(*self.btn_create)
