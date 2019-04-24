from collections import namedtuple

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from common.selenium.WavelabsDriver import WavelabsDriver


class ElementManagement :


    def press_keys(self, locator=None, *keys):
        """Simulates user pressing key(s) to an element or on the active browser.
        If ``locator`` evaluates as false, then the ``keys`` are sent to the currently active browser.
        Otherwise element is searched and ``keys`` are send to the element
        identified by the ``locator``. If Key is combined
        with strings, key and strings must be separated by the
        `+` character, like in `CONTROL+c`. Keys
        are space and case sensitive and Selenium Keys are not parsed
        inside of the string.

        If Selenium Keys are detected in the ``keys`` argument, keyword
        will press the Selenium Key down, send the strings and
         then release the Selenium Key. If keyword needs to send a Selenium
        Key as a string, then each character must be separated with
        `+` character, example `E+N+D`.

        Examples:
        | `Press Keys` | text_field | AAAAA          |            | # Sends string "AAAAA" to element.                                                |
        | `Press Keys` | None       | BBBBB          |            | # Sends string "BBBBB" to currently active browser.                               |
        | `Press Keys` | text_field | E+N+D          |            | # Sends string "END" to element.                                                  |
        | `Press Keys` | text_field | XXX            | YY         | # Sends strings "XXX" and "YY" to element.                                        |
        | `Press Keys` | text_field | XXX+YY         |            | # Same as above.                                                                  |
        | `Press Keys` | text_field | ALT+ARROW_DOWN |            | # Pressing "ALT" key down, then pressing ARROW_DOWN and then releasing both keys. |
        | `Press Keys` | text_field | ALT            | ARROW_DOWN | # Pressing "ALT" key and then pressing ARROW_DOWN.                                |
        | `Press Keys` | text_field | CTRL+c         |            | # Pressing CTRL key down, sends string "c" and then releases CTRL key.            |
        | `Press Keys` | button     | RETURN         |            | # Pressing "ENTER" key to element.                                                |
        """
        driver = WavelabsDriver.instance.val
        driver.find_element().send_keys(Keys.ESCAPE)

        parsed_keys = self._parse_keys(*keys)
        self._press_keys(locator, parsed_keys)

    def _press_keys(self, locator, parsed_keys):
        driver = WavelabsDriver.instance.val
        element = driver.find_element(locator)
        for parsed_key in parsed_keys:
            actions = ActionChains(driver)
            special_keys = []
            for key in parsed_key:
                if self._selenium_keys_has_attr(key.original):
                    special_keys = self._press_keys_special_keys(actions, element, parsed_key,
                                                                 key, special_keys)
                else:
                    self._press_keys_normal_keys(actions, element, key)
            for special_key in special_keys:
                actions.key_up(special_key.converted)
            actions.perform()

    def _press_keys_normal_keys(self, actions, element, key):
        if element:
            actions.send_keys_to_element(element, key.converted)
        else:
            actions.send_keys(key.converted)

    def _press_keys_special_keys(self, actions, element, parsed_key, key, special_keys):
        if len(parsed_key) == 1 and element:
            actions.send_keys_to_element(element, key.converted)
        elif len(parsed_key) == 1 and not element:
            actions.send_keys(key.converted)
        else:
            actions.key_down(key.converted)
            special_keys.append(key)
        return special_keys

    def _parse_keys(self, *keys):
        if not keys:
            raise AssertionError('"keys" argument can not be empty.')
        list_keys = []
        for key in keys:
            separate_keys = self._separate_key(key)
            separate_keys = self._convert_special_keys(separate_keys)
            list_keys.append(separate_keys)
        return list_keys

    def _parse_aliases(self, key):
        if key == 'CTRL':
            return 'CONTROL'
        if key == 'ESC':
            return 'ESCAPE'
        return key

    def _separate_key(self, key):
        one_key = ''
        list_keys = []
        for char in key:
            if char == '+' and one_key != '':
                list_keys.append(one_key)
                one_key = ''
            else:
                one_key += char
        if one_key:
            list_keys.append(one_key)
        return list_keys

    def _convert_special_keys(self, keys):
        KeysRecord = namedtuple('KeysRecord', 'converted, original')
        converted_keys = []
        for key in keys:
            key = self._parse_aliases(key)
            if self._selenium_keys_has_attr(key):
                converted_keys.append(KeysRecord(getattr(Keys, key), key))
            else:
                converted_keys.append(KeysRecord(key, key))
        return converted_keys

    def _selenium_keys_has_attr(self, key):
        try:
            return hasattr(Keys, key)
        except UnicodeError:  # To support Python 2 and non ascii characters.
            return False
