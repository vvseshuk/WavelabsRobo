import os
from os.path import dirname
from pathlib import Path

from selenium import webdriver
from enum import Enum
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

ROBOT_LIBRARY_SCOPE = 'GLOBAL'


class DriverType(Enum):


    """
    Enum containing supported Selenium driver types.  To use a driver,
    set the UI.driver property to one of the values in this Enum
    """

    CHROME = "chrome"
    CHROME_HEADLESS = "headless_chrome"
    INTERNET_EXPLORER = "internet_explorer"
    EDGE = "edge"
    FIREFOX = "firefox"
    SAFARI = "safari"


class WavelabsDriver:

    """
    Wrapper class around a Selenium WebDriver, contains methods for initializing
    the correct driver type, etc.  Implements the Singleton pattern to ensure
    only one driver gets used in a single test run.

    See here: http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    # Constant defining the folder containing the Selenium driver executables
    DRIVER_EXECUTABLE_FOLDER = "C:\\SeleniumDrivers"
    DOWNLOAD_FOLDER = "C:\\SeleniumTestDownloads"

    DRIVER_EXECUTABLE_CHROME = "chromedriver"
    DRIVER_EXECUTABLE_INTERNET_EXPLORER = "IEDriverServer.exe"
    DRIVER_EXECUTABLE_EDGE = "MicrosoftWebDriver.exe"
    DRIVER_EXECUTABLE_FIREFOX = "geckodriver.exe"
    DRIVER_EXECUTABLE_SAFARI = "TBD"

    DEFAULT_WAIT_TIME = 60

    def __init__(self):
        print("init Wavelabs driver")
        if not WavelabsDriver.instance:
            WavelabsDriver.instance = WavelabsDriver.__Driver()


    class __Driver:

        """
        Internal class that actually creates the WebDriver
        """

        ROBOT_LIBRARY_SCOPE = 'GLOBAL'
        val = None;

        def driver(self, driver_type=DriverType.CHROME.value):

            """
            Get the current instance of the WebDriver - initializes one if not already done.

            :return: the current singleton WebDriver
            """
            print("driver")
            if self.val is None:  # create if it doesn't exist
                self.val = self._init_driver(driver_type)

            return self.val

        def _init_driver(self, driver_type):

            """
            Parses the framework.ini config file and initializes the appropriate web driver type
            based on the value of the UI.driver property
            """
            print("_init_driver")
            if driver_type == DriverType.CHROME.value:
                self.val = self._init_chrome_driver(False)

            elif driver_type == DriverType.CHROME_HEADLESS:
                self.val = self._init_chrome_driver(True)

            elif driver_type == DriverType.FIREFOX:
                self.val = webdriver.Firefox()

            elif driver_type == DriverType.INTERNET_EXPLORER:
                self.val = webdriver.Ie()

            elif driver_type == DriverType.EDGE:
                self.val = webdriver.Edge

            else:
                raise Exception("Specified WebDriver type \"{}\" is not yet supported.".format(driver_type))

            return self.val

        @staticmethod
        def _init_chrome_driver(headless):

            """
            Initializes a Chrome Driver, with the options necessary to ensure test stability (maximize browser, etc.)

            :param headless: if true, run as a headless browser

            :return: the initialized driver
            """

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("prefs", {
                "profile.default_content_settings.popups": 0,
                "download.default_directory": WavelabsDriver.DOWNLOAD_FOLDER
            })

            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--no-sandbox")

            if headless:
                chrome_options.add_argument('headless')

            # driver_path = WavelabsDriver.DRIVER_EXECUTABLE_CHROME

            #PROJECT_ROOT = os.path.abspath (os.path.dirname (__file__))
            #PROJECT_ROOTS = os.path.abspath(Path(__file__).parent.parent)
            #driver_path = os.path.join (PROJECT_ROOT, "\\Drivers\\chromedriver")
            #driver_path = os.path.join(PROJECT_ROOT, "//Drivers//chromedriver")
            #print("Dir:",os.path.dirname(__file__))
            #print("project root:", PROJECT_ROOT)
            #print("driver path:",driver_path)
            MAIN_DIRECTORY = dirname(dirname(__file__))+("\drivers\chromedriver")
            print("main direcotry:", MAIN_DIRECTORY)
            #MAIN_DIRECTORYSS = join(MAIN_DIRECTORY, "\Drivers\chromedriver")
            #print("main direcotry:", MAIN_DIRECTORY)
            #return webdriver.Chrome(executable_path="C:\\Users\\seshuk\\PycharmProjects\\WavelabsRobo\\WebDriver\\Drivers\\chromedriver", chrome_options=chrome_options)
            return webdriver.Chrome(
                executable_path=MAIN_DIRECTORY,
                chrome_options=chrome_options)

        def inner_start_browser(self, driver_type):
            print("inner Start Browser")
            if self.val is None:  # create if it doesn't exist

                self.val = self._init_driver(driver_type)

        @staticmethod
        def get_project_root() -> Path:
            """Returns project root folder."""
            return Path(__file__).parent.parent

        def inner_close_browser(self):

            """Close the WebDriver and associated Browser; should be called at the end of every test run"""
            print("inner close Browser")
            if self.val is not None:
                self.val.close()
                self.val = None

        def wait_for_page_load(self):
            self.wait_for_javascript()
            self.wait_for_jquery()
            self.wait_for_angular_1()

        def wait_for_javascript(self):

            try:
                js_ready = self.has_javascript_loaded(self.val)

                if not js_ready:
                    WebDriverWait(self.val, WavelabsDriver.DEFAULT_WAIT_TIME).until(self.has_javascript_loaded)

            except TimeoutException:
                pass

        def wait_for_jquery(self):

            try:
                if self.is_jquery_present():

                    jquery_ready = self.has_jquery_loaded(self.val)

                    if not jquery_ready:
                        WebDriverWait(self.val, WavelabsDriver.DEFAULT_WAIT_TIME).until(self.has_jquery_loaded)

            except TimeoutException:
                pass

        def wait_for_angular_1(self):

            try:
                if self.is_angular_1_present():

                    jquery_ready = self.has_angular_1_loaded(self.val)

                    if not jquery_ready:
                        WebDriverWait(self.val, WavelabsDriver.DEFAULT_WAIT_TIME).until(self.has_angular_1_loaded)

            except TimeoutException:
                pass

        def has_javascript_loaded(self, driver):
            current_state = driver.execute_script("return document.readyState;")
            return current_state == 'complete'

        def has_jquery_loaded(self, driver):
            current_state = driver.execute_script("return jQuery.active==0")
            return current_state

        def has_angular_1_loaded(self, driver):
            current_state = driver.execute_script("return angular.element(document).injector().get('$http').pendingRequests.length === 0")
            return current_state

        def is_jquery_present(self):
            is_defined = self.val.execute_script("return typeof jQuery != 'undefined'")
            return is_defined

        def is_angular_1_present(self):
            is_angular_undefined = self.val.execute_script("return window.angular === undefined")

            if not is_angular_undefined:
                is_angular_injector_undefined = self.val.execute_script("return angular.element(document).injector() === undefined")
            else:
                is_angular_injector_undefined = False

            is_defined = (not is_angular_undefined) & (not is_angular_injector_undefined)
            return is_defined

    instance = None


    def __getattr__(self, name):
        return getattr(self.instance, name)

