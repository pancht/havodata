"""
=====================CAUTION=======================
DO NOT DELETE THIS FILE SINCE IT IS PART OF NROBO
FRAMEWORK AND IT MAY CHANGE IN THE FUTURE UPGRADES
OF NROBO FRAMEWORK. THUS, TO BE ABLE TO SAFELY UPGRADE
TO LATEST NROBO VERSION, PLEASE DO NOT DELETE THIS
FILE OR ALTER ITS LOCATION OR ALTER ITS CONTENT!!!
===================================================

@author: Panchdev Singh Chauhan
@email: erpanchdev@gmail.com
"""
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Union
from nrobo.selenese import NRobo, WAITS

AnyBrowser = Union[None, WebDriver]
from selenium.webdriver.common.actions.wheel_input import WheelInput
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.key_input import KeyInput
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from typing import Optional, Union
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys

AnyDevice = Union[PointerInput, KeyInput, WheelInput]
AnyBy = Union[By, AppiumBy]


class Page(NRobo):
    """
    Page class is the base class for every _page objects
    that one is going to be created for his/her project.

    Page class inherits wrapper classes wraps the most
    frequently used api's of the Webdriver, WebElement,
    and other selenium classes which brings the power of
    readability of your scripts. Along with readable code,
    comes the power of highly maintainable and understandable
    code-base.

    And many more...
    I would request to checkout video tutorials uploaded at the
    following YouTube channel: https://shorturl.at/lpqKS

    Example usage: Assume that you want to create a Page Object
    in your automation project for home _page, then you should
    declare your Page Class as following:

    Package: pages
    File: home.py
    ============FileContent of home.py===========================

    from pages import Page

    class PageHome(Page):

        def __init__(self, driver, logger):
            super().__init__(driver, logger)

            # Definition of home _page locators should go below

        def page_method_1(self):
            ...

        def page_mathod_2(self):
            ...

        # and so on per project need.
    """

    def __init__(self, driver=AnyBrowser, logger=None | logging.Logger, duration: int = 250,
                 devices: list[AnyDevice] | None = None):
        """constructor"""
        # call parent constructor
        super().__init__(driver, logger, duration=duration, devices=devices)

        self.close_product_tour_popup()

    ##################################################
    # Implement application specific _page methods here
    ##################################################

    def wait_for_element_to_be_present(self, by: AnyBy, value: Optional[str] = None, wait: int = 0):
        """Wait for element to be visible"""

        if wait:
            try:
                WebDriverWait(self.driver, wait).until(
                    expected_conditions.presence_of_element_located([by, value]))
                return True
            except Exception as e:
                return False

        try:
            WebDriverWait(self.driver, self.nconfig[WAITS.WAIT]).until(
                expected_conditions.presence_of_element_located([by, value]))
            return True
        except Exception as e:
            return False

    def close_product_tour_popup(self):

        btn_product_tour_close_icon = (By.CSS_SELECTOR, "button[data-id='product-tour-close-icon-button']")
        self.wait_for_element_to_be_present(*btn_product_tour_close_icon, 10)

        if self.is_displayed(*btn_product_tour_close_icon):
            """Close the intercom frame"""
            self.click(*btn_product_tour_close_icon)
            self.wait_for_page_to_be_loaded()

    def wait_for_element_to_be_disappeared(self, by: AnyBy, value: Optional[str] = None, wait: int = 0):
        """wait till <element> disappears from the UI"""

        # wait a little
        self.wait_for_a_while(self.nconfig[WAITS.WAIT])

        # wait until the locator becomes invisible
        if wait:
            try:
                WebDriverWait(self.driver, wait).until(
                    expected_conditions.invisibility_of_element_located([by, value]))
            except Exception as e:
                return False

            self.wait_for_a_while(self.nconfig[WAITS.WAIT])
            return True

        try:
            WebDriverWait(self.driver, self.nconfig[WAITS.WAIT]).until(
                expected_conditions.invisibility_of_element_located([by, value]))
        except Exception as e:
            return False

        self.wait_for_a_while(self.nconfig[WAITS.WAIT])
        return True

    def open_drawer_destination(self):
        """Open Destination Drawer"""

        lnk_destination_drawer = (By.XPATH, "//a[contains(@href,'drawer=destinations')]")
        self.click(*lnk_destination_drawer)
        self.wait_for_page_to_be_loaded()

        from pages.hevo_data.auth.drawers.destinations.destinations import PageDestinationsDrawer
        return PageDestinationsDrawer(driver=self.driver, logger=self.logger)

    def clear_spl(self, by: AnyBy, value: Optional[str] = None):

        element = self.find_element(by, value)
        self.action_chain().click(element).send_keys(Keys.ARROW_LEFT)\
            .double_click(self.find_element(by, value)).send_keys(Keys.DELETE)\
            .perform()
        self.wait_for_a_while(2)
