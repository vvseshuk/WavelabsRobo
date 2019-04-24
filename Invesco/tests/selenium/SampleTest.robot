*** Settings ***
Documentation    First sample to use own keywords

Resource          ../../../common/keywords/wavelabsPageKeywords/WavelabsKeywords.robot

*** Test Cases ***
Test title
    [Tags]    DEBUG
    Test Initialize
    Open Browser To Start Page      https://google.com
    Test Teardown

