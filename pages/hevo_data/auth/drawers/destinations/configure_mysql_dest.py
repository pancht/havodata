from pages import Page
from selenium.webdriver.common.by import By


class PageConfigureMySqlDest(Page):
    """Configure MySql Destination Page Class"""

    def __init__(self, driver, logger):
        """constructor"""

        super().__init__(driver=driver, logger=logger)

    # Page elements
    txt_db_host = (By.CSS_SELECTOR, "input[name='host']")
    txt_db_port = (By.CSS_SELECTOR, "input[name='port']")
    txt_db_user = (By.CSS_SELECTOR, "input[name='user']")
    txt_db_pass = (By.CSS_SELECTOR, "input[name='password']")
    txt_db_name = (By.CSS_SELECTOR, "input[name='databaseName']")

    rdo_connect_through_ssh = (By.CSS_SELECTOR, "input[name='useSSH']")
    txt_sship = (By.CSS_SELECTOR, "input[name='sshIp']")
    txt_sshport = (By.CSS_SELECTOR, "input[name='sshPort']")
    txt_sshuser = (By.CSS_SELECTOR, "input[name='sshUser']")

    btn_test_connection = (By.XPATH, "//button[text()='Test Connection']")
    btn_save_and_continue = (By.XPATH, "//button[text()='Save & Continue']")

    # Page methods
    def config_dest_type_save_test_continue(self, config: {}, ssh: {}):
        """Config Source Type, Save, Test and Continue"""

        self.close_product_tour_popup()

        self.clear_spl(*self.txt_db_host)
        self.send_keys(*self.txt_db_host, config['host'])
        self.clear_spl(*self.txt_db_port)
        self.send_keys(*self.txt_db_port, str(config['port']))
        self.clear_spl(*self.txt_db_user)
        self.send_keys(*self.txt_db_user, config['user'])

        try:
            self.click(By.XPATH, "//*[text()='Change']")
            self.wait_for_a_while(1)
        except Exception as e:
            pass
        self.clear_spl(*self.txt_db_pass)
        self.send_keys(*self.txt_db_pass, config['password'])

        self.clear_spl(*self.txt_db_name)
        self.send_keys(*self.txt_db_name, config['database'])

        # self.location_once_scrolled_into_view(*self.rdo_connect_through_ssh)
        # for count in range(10):
        #     self.action_chain().pause(1).double_click(self.find_element(*self.rdo_connect_through_ssh)).perform()
        #     self.wait_for_page_to_be_loaded()
        #
        #     if self.is_displayed(*self.txt_sship):
        #         break
        #
        # self.send_keys(*self.txt_sship, ssh['ip'])
        # self.send_keys(*self.txt_sshport, str(ssh['port']))
        #
        # self.location_once_scrolled_into_view(*self.txt_sshuser)
        # self.send_keys(*self.txt_sshuser, ssh['username'])

        self.click(*self.btn_save_and_continue)
        self.wait_for_page_to_be_loaded()

        for count in range(5):
            if not self.wait_for_element_to_be_disappeared(*self.btn_save_and_continue, 15):
                self.click(*self.btn_save_and_continue)
            else:
                break

        from pages.hevo_data.auth.create_pipeline.select_destination import PageSelectDestinationStepTwo
        return PageSelectDestinationStepTwo(driver=self.driver, logger=self.logger)
