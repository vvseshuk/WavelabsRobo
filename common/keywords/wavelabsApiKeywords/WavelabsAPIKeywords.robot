*** Settings ***
Documentation    API related reusable Keywords

Library         REST


*** Keywords ***
Get from the URI
    [Arguments]    ${uri}
    Log    Initializing Get Request ...
    GET         ${uri}                 # this creates a new instance
