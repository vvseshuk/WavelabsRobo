*** Settings ***
Documentation    Test case to demonestrate the authentication key request
Library         REST    https://community-manga-eden.p.rapidapi.com     ssl_verify=false    content_type=application/json
Resource            ../../../common/keywords/wavelabsAPIKeywords/WavelabsAPIKeywords.robot

*** Test Cases ***
Test first sample
    Set Headers     {"X-RapidAPI-Host": "community-manga-eden.p.rapidapi.com"}
    Set Headers     {"X-RapidAPI-Key": "f3035f69a2msh7bc2ca1e67c133ep115d25jsn8079ee82eced"}
    Get from the URI          /list/0
    Integer     response status           200
    [Teardown]  Output  response body     ${OUTPUTDIR}/auth_demo.json

