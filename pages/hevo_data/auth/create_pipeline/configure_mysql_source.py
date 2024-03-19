from pages import Page
from selenium.webdriver.common.by import By

from pages.hevo_data.auth.create_pipeline.select_objects import PageSelectObjectsStepOne


class PageConfigureMySqlSource(Page):
    """Configure MySql Source Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    txt_db_host = (By.CSS_SELECTOR, "input[name='host']")
    txt_db_port = (By.CSS_SELECTOR, "input[name='port']")
    txt_db_user = (By.CSS_SELECTOR, "input[name='user']")
    txt_db_pass = (By.CSS_SELECTOR, "input[name='password']")
    btn_see_more = (By.CSS_SELECTOR, "seeMoreBtn_RIGA_ btn-thumbnail-right")
    rdo_ingestion_mode_table = (By.CSS_SELECTOR, "input[value='table']")
    txt_db_name = (By.CSS_SELECTOR, "input[name='databaseName']")

    rdo_connect_through_ssh = (By.CSS_SELECTOR, "input[name='useSSH']")
    txt_sship = (By.CSS_SELECTOR, "input[name='sshIp']")
    txt_sshport = (By.CSS_SELECTOR, "input[name='sshPort']")
    txt_sshuser = (By.CSS_SELECTOR, "input[name='sshUser']")

    btn_test_connection = (By.XPATH, "//button[text()='Test Connection']")
    btn_test_connection_and_continue = (By.XPATH, "//button[text()='Test Connection']")

    # Page methods
    def config_source_type_save_test_continue(self, config: {}, ssh: {}):
        """Config Source Type, Save, Test and Continue"""

        self.send_keys(*self.txt_db_host, config['host'])
        self.send_keys(*self.txt_db_port, config['port'])
        self.send_keys(*self.txt_db_user, config['user'])
        self.send_keys(*self.txt_db_pass, config['password'])

        self.click(*self.btn_see_more)
        self.click(*self.rdo_ingestion_mode_table)
        self.wait_for_page_to_be_loaded()

        self.send_keys(*self.txt_db_name)

        self.click(*self.rdo_connect_through_ssh)
        self.wait_for_page_to_be_loaded()
        self.send_keys(*self.txt_sship, ssh['ip'])
        self.send_keys(*self.txt_sshport, ssh['port'])
        self.send_keys(*self.txt_sshuser, ssh['username'])

        self.click(*self.btn_test_connection_and_continue)
        self.wait_for_page_to_be_loaded()

        return PageSelectObjectsStepOne(driver=self.driver, logger=self.logger)

