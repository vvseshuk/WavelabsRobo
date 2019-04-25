*** Settings ***
Documentation       This suite is for demonstrating the Robot Framework with Selenium Webdriver and Python langauge

Library             ../../../common/pages/WavelabsPage.py
Resource            ../../../common/keywords/wavelabsPageKeywords/WavelabsKeywords.robot
Variables           ../../../common/variables/CommonVariables.py
Variables           ../../variables/InvescoVariables.py
Variables           ../../pages/LoginPageLocators.py


*** Test Cases ***

Google Search
    [Tags]    DEBUG
    Test Initialize
    Open Browser To Start Page      ${APP URL}
    Input Text   ${LOCATOR NAME}     ${SEARCH TEXTBOX NAME}       Automation Testing   ${SEARCH TEXTBOX NAME}
    Press Escape    ${LOCATOR NAME}      ${SEARCH TEXTBOX NAME}
    Click Element   ${LOCATOR NAME}      ${SEARCH BUTTON NAME}      ${SEARCH BUTTON NAME}
    Title Should Be    Automation Testing - Google Search
    Test Teardown

