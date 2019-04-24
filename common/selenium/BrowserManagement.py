
from common.selenium.WavelabsDriver import WavelabsDriver

class BrowserManagement:

    def driver(self):
        return WavelabsDriver.WavelabsDriver.instance.val



