import sys
from os.path import dirname
import traceback
from robot.libraries.BuiltIn import BuiltIn
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# from mainpackage.selenium.WavelabsDriver import WavelabsDriver
# sys.path.append('../../mainpackage/')
# sys.path.insert(0, '../../mainpackage')
# sys.path.insert(0, 'C:\\Users\\seshuk\\PycharmProjects\\WavelabsRobo')
sys.path.insert(0, dirname(dirname(dirname(__file__))))
from common.selenium.WavelabsDriver import WavelabsDriver


def no_such_element_exception_msg(locator_type, locator):
    tb = traceback.format_exc()
    BuiltIn().fail("Element located by: " + str(locator_type + ": " + locator) + " is not found, " + str(tb))


def timeout_exception_msg(locator_type="", locator="", wait_time=0):
    tb = traceback.format_exc()
    BuiltIn().fail("Element by: " + str(locator_type + ": " + locator) +
                   " is not found in the given max wait time (i.e. " + str(wait_time) + ")" + str(tb))


def generic_exception_msg(method_name):
    tb = traceback.format_exc()
    BuiltIn().fail("Exception in " + method_name + " keyword/method " + str(tb))


class WavelabsPage:

    def navigate_to_page(self, url):
        """navigates to the launch page, performs logout if within VE"""
        driver = self.driver
        driver.get(url)

    def get_webelement(self, locator_type, locator):
        """
        This method is used to get the WebElement object by passing the required arguments
        :return: WebElement object
        :param locator_type: type of locator identifier
        :param locator: element locator
        """
        try:
            driver = self.driver
            element = driver.find_element(locator_type, locator)
            return element
        except NoSuchElementException as ex:
            no_such_element_exception_msg(locator_type, locator)

        except Exception:
            generic_exception_msg(self.get_webelement.__name__)

    def get_webelements(self, locator_type, locator):
        """
        This method is used to get the list of matching elements to the provided element locator
        :param locator_type:
        :param locator:
        :return:
        """
        try:
            driver = self.driver
            elements_list = driver.find_elements(locator_type, locator)
            return elements_list
        except NoSuchElementException:
            no_such_element_exception_msg(locator_type, locator)
        except Exception:
            generic_exception_msg(self.get_webelements.__name__)

    def get_element_attribute(self, locator_type, locator, attribute_name):
        self.scroll_to_element(locator_type, locator)
        return self.get_webelement(locator_type, locator).get_attribute(attribute_name)

    def clear(self, locator_type, locator):
        """clicks the element identified by given element locator tuple"""
        try:
            self.get_webelement(locator_type, locator).clear()
        except NoSuchElementException:
            no_such_element_exception_msg(locator_type, locator)
        except Exception:
            generic_exception_msg(self.clear.__name__)

    def input_text(self, locator_type, locator, text, element_name):
        """
        Keyword/definition is useful to type the given text in the given element
        :param locator_type: type of the element locator
        :param locator: element locator
        :param text: the text to type in the mentioned element
        :param element_name: name of the input element
        :return:
        """
        builtIn = BuiltIn()
        try:
            self.clear(locator_type, locator)
            self.get_webelement(locator_type, locator).send_keys(text)
            if text.find(Keys.TAB) > -1:
                text = text.replace(Keys.TAB, "")
            builtIn.log("Entered  input for " + element_name + " as: " + text, html=True)
        except NoSuchElementException:
            no_such_element_exception_msg(locator_type, locator)
        except Exception:
            generic_exception_msg(self.input_text.__name__)

    def input_password(self, locator_type, locator, password):
        """
        Keyword/definition is useful to type the given text in the given element
        :param locator_type: type of the element locator
        :param locator: element locator
        :param password: the text to type in the mentioned element

        :return:
        """
        builtIn = BuiltIn()
        try:
            self.clear(locator_type, locator)
            self.get_webelement(locator_type, locator).send_keys(password)
            builtIn.log("Entered  Password as: * * * * * * * *", html=True)
        except NoSuchElementException:
            no_such_element_exception_msg(locator_type, locator)
        except Exception:
            generic_exception_msg(self.input_password.__name__)

    def click_element(self, locator_type, locator, element_name):
        """clicks the element identified by given element locator tuple"""
        builtIn = BuiltIn()
        try:
            self.wait_for_element_visible(locator_type, locator)
            self.click_element_without_report(locator_type, locator)
            builtIn.log(element_name + " clicked successfully", html=True)
            self.wait_for_page_load()
        except NoSuchElementException:
            no_such_element_exception_msg(locator_type, locator)
        except Exception:
            generic_exception_msg(self.click_element.__name__)

    def click_element_without_report(self, locator_type, locator):
        """clicks the element identified by given element locator tuple"""
        try:
            self.get_webelement(locator_type, locator).click()
            self.wait_for_page_load()
        except Exception:
            generic_exception_msg(self.click_element_without_report.__name__)

    def javascript_click_without_report(self, locator_type, locator):

        builtIn = BuiltIn()
        try:
            driver = self.driver
            element = self.get_webelement(locator_type, locator)
            driver.execute_script("arguments[0].click();", element)
            self.wait_for_page_load()
        except Exception:
            generic_exception_msg(self.javascript_click_without_report.__name__)

    def javascript_click(self, locator_type, locator, element_name):
        """
        :param locator_type: By which type element is identified
        :param locator: element locator
        :param element_name: Name of the element for reporting purpose
        This method is used to click the element which is identified by given locator_type & locator
        (Note: This definition/keyword useful if regular Click Element/Button keyword not working properly)
        """
        builtIn = BuiltIn()
        try:
            self.javascript_click_without_report(locator_type, locator)
            builtIn.log("Element " + element_name + " clicked successfully", html=True)
        except Exception:
            generic_exception_msg(self.javascript_click.__name__)

    def is_element_displayed(self, locator_type, locator, element_name="", report_log=False):
        builtIn = BuiltIn()
        is_displayed = False
        element_list = self.get_webelements(locator_type, locator)
        if len(element_list) > 0:
            is_displayed = True

        if report_log:
            if is_displayed:
                if len(element_name) > 0:
                    builtIn.log("Element: " + element_name + " is displayed", html=True)
                else:
                    builtIn.log("Element located by " + locator_type + ": " + locator + " is displayed", html=True)
            else:
                builtIn.log("Element: " + element_name + " is displayed", html=True, level='WARN')

        return is_displayed

    def scroll_to_element(self, locator_type, locator):
        """
        This method is used to scroll down/up to the required element
        :param locator_type:
        :param locator:
        :return:
        """
        try:
            element = self.get_webelement(locator_type, locator)
            self.driver.execute_script("return arguments[0].scrollIntoView();", element)
            return
        except Exception:
            generic_exception_msg(self.scroll_to_element.__name__)

    def start_browser(self, driver_type):
        print("Start Browser")
        self.driver = WavelabsDriver().driver(driver_type)

    def close_browser(self):
        """Close the WebDriver and associated Browser; should be called at the end of every test run"""
        print("Close Browser")
        WavelabsDriver().inner_close_browser()

    def driver(self):
        temp = WavelabsDriver.WavelabsDriver.instance.val
        return temp

    def wait_for_page_load(self):
        try:
            WavelabsDriver.instance.wait_for_page_load()
        except TimeoutException:
            BuiltIn().fail(
                "Page loading time exceeded the max wait time (i.e. " + str(WavelabsDriver.DEFAULT_WAIT_TIME) + ")")

        except Exception:
            generic_exception_msg(self.wait_for_page_load.__name__)

    def wait_for_element_present(self, locator_type, locator, wait_time=WavelabsDriver.DEFAULT_WAIT_TIME):
        try:
            WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located((locator_type, locator)))
        except TimeoutException:
            timeout_exception_msg(locator_type, locator, wait_time)

        except Exception:
            generic_exception_msg(self.wait_for_element_present.__name__)

    def wait_for_element_visible(self, locator_type, locator, wait_time=WavelabsDriver.DEFAULT_WAIT_TIME):
        try:
            WebDriverWait(self.driver, WavelabsDriver.DEFAULT_WAIT_TIME).until(
                EC.visibility_of_element_located((locator_type, locator)))
        except TimeoutException:
            timeout_exception_msg(locator_type, locator, wait_time)

        except Exception:
            generic_exception_msg(self.wait_for_element_visible.__name__)

    def wait_for_element_not_present(self, locator_type, locator, wait_time=WavelabsDriver.DEFAULT_WAIT_TIME):
        try:
            wait = WebDriverWait(self.driver, WavelabsDriver.DEFAULT_WAIT_TIME)
            wait.until(EC.invisibility_of_element_located((locator_type, locator)))
        except TimeoutException:
            timeout_exception_msg(locator_type, locator, wait_time)

        except Exception:
            generic_exception_msg(self.wait_for_element_not_present.__name__)

    def wait_for_element_present(self, locator_type, locator, wait_time=WavelabsDriver.DEFAULT_WAIT_TIME):
        try:
            wait = WebDriverWait(self.driver, WavelabsDriver.DEFAULT_WAIT_TIME)
            wait.until(EC.visibility_of_element_located((locator_type, locator)))
        except TimeoutException:
            timeout_exception_msg(locator_type, locator, wait_time)

        except Exception:
            generic_exception_msg(self.wait_for_element_not_present.__name__)

    def press_escape(self, locator_type, locator):
        self.get_webelement(locator_type, locator).send_keys(Keys.ESCAPE)

    def title_should_be(self, expectedTitle, message=None):
        actualTitle = self.driver.title
        if actualTitle != expectedTitle:
            if (message):
                message = "Title should have been '%s' but was '%s'." % (expectedTitle, actualTitle)
            raise AssertionError(message)
