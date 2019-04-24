*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.

Library       ../../pages/WavelabsPage.py




*** Variables ***
${UI.BROWSER}     chrome

*** Keywords ***
Test Initialize
    Log    Initializing Test Suite...

    WavelabsPage.Start Browser    ${UI.BROWSER}
    Log    Test Suite Initialization Complete

Test Teardown
    Log    Tearing Down Test Suite...
    WavelabsPage.Close Browser
    Log    Test Suite Teardown Complete

Open Browser To Start Page
    [Arguments]    ${url}
    WavelabsPage.Navigate To Page     ${url}
