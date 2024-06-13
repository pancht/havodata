from pages import Page
from selenium.webdriver.common.by import By


class PagePublic(Page):
    """Public HevoData.com Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    lnk_login = (By.CSS_SELECTOR, "a[href='/login/']")

    # Page methods
    def go_to_login_page(self, url):
        """Go To Login Page by clicking over Login link"""

        self.maximize_window()

        self.logger.info(f"Open url: {url}")
        self.get(url)
        self.wait_for_page_to_be_loaded()

        if url == 'https://hevodata.com/':
            self.logger.info("Click on Login link")
            self.click(*self.lnk_login)

        from pages.hevo_data.public.login import PageLoginStepEmail
        return PageLoginStepEmail(driver=self.driver, logger=self.logger)
