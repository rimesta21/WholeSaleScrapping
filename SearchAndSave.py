# -*- coding: utf-8 -*-
"""
Created on Sat May 15 20:30:04 2021

@author: rimes
"""


from InputOutput import InputOutput
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import requests, bs4
import re
from Person import Person
import time

def save(browser, searchData, results):
            
    for address, name in searchData.items():
        checkSearch = search(browser, address, name)
        if checkSearch == None:
            continue
        results.append(checkSearch)
        homePage = browser.find_element_by_xpath("//a[@title = 'Home Page']")
        homePage.click()
    
    return results
        
    
def search(browser, address, name):
    fixString = InputOutput()
    
    addressSearch = browser.find_element_by_id("search-nav-link-address")
    addressSearch.click()
    
    street = fixString.getAdress(address)
    streetEntry = browser.find_element_by_xpath("//input[@name = 'address1']")
    streetEntry.send_keys(street)
    
    cityState = fixString.getCityState(address)
    cityStateEntry = browser.find_element_by_xpath("//input[@name = 'address2']")
    cityStateEntry.send_keys(cityState, Keys.RETURN)
        
    name = fixString.commaCheck(name)
    name = fixString.parenthesisCheck(name)
    name = fixString.middleInitialCheck(name)
    #timeout expeption, if there is a next page click it and repeat, if return none
    while(True):
        try:
            personSearch = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.LINK_TEXT,name)))
            personSearch.click()
            break
        except TimeoutException:
            try:
                nxtBttn = browser.find_element_by_xpath("//a[@title = 'Next page of search results']")
                nxtBttn.click()
            except NoSuchElementException:
                return None
                
    numbers, addresses = scrapInfo(browser.current_url, address)
    return makePerson(name, numbers, addresses)
    
    
def scrapInfo(url, address):
    hdr = {'User-Agent' : 'Mozilla/5.0'}
    res = requests.get(url, headers = hdr)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    numbers = getNumbers(soup)
    mailingAddress = mailAddress(soup, address)
    return numbers, mailingAddress
    
def getNumbers(soup):
    numbersBox = soup.find('div', {'class' : 'detail-box-phone'})
    numbers = []
    if numbersBox == None:
        return numbers
    
    text = numbersBox.get_text()
    phoneNumRegex = re.compile(r'\(\d\d\d\) \d\d\d-\d\d\d\d')
    numbers = phoneNumRegex.findall(text)
    return numbers

def mailAddress(soup, address):
    addressRegex = re.compile(r'\d+ \w+ \w{2}(, \w+ \d+)?\n(\w+)? \w+ \w{2} \d+')
    currAddressBox = soup.find('div', {'id' : 'current_address_section'})
    
    temp = currAddressBox.get_text()
    currAddress = addressRegex.search(temp).group()
    currAddress = currAddress.replace("\n", ", ")
    
    if currAddress.lower() != address.lower():
        return [currAddress, address]
    
    addresses = soup.find('div', {'class' : 'detail-box-address'})
    if addresses == None:
        return [currAddress]
    temp = addresses.get_text()
    prevAddress = addressRegex.search(temp).group()
    return [prevAddress.replace("\n", ", "), address]

def makePerson(name, numbers, addresses):
    tempPerson = Person()
    tempPerson.setName(name)
    
    if len(addresses) == 1:
        tempPerson.setProperty(addresses[0])
        tempPerson.setMailAddress(addresses[0])
    else:
        tempPerson.setProperty(addresses[1])
        tempPerson.setMailAddress(addresses[0])
    tempPerson.printInfo()
    return tempPerson
    
      
    
    
if __name__ == '__main__':
    io = InputOutput()
    io.getInput('2 26 19 Skip Tracing.xlsx')
    searchData = io.properties
    
    option = Options()
    path_to_ad_block = r'C:\Users\rimes\OneDrive\Desktop\1.35.2_0'

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("load-extension=" + path_to_ad_block)

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1 
    })

    browser = webdriver.Chrome(chrome_options=option)
    
    #browser = webdriver.Chrome()
    browser.get('https://fastpeoplesearch.com/')
    
    results = []
    results = save(browser, searchData, results)
    
    
    
    