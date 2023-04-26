from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def navigate_login(url,driver):
    driver.get(url)
    folder = driver.find_element_by_xpath("//*[@id='artdeco-global-alert-container']/div/section/div/div[2]/button[1]")
    folder.click()
    folder2 = driver.find_element_by_xpath("/html/body/nav/div/a[2]")
    folder2.click()

    element_user = driver.find_element_by_id('username')
    element_user.send_keys('JMV.dummy@gmail.com')
    element_password = driver.find_element_by_id('password')
    element_password.send_keys('$dummy2023')
    element_aanmelden = driver.find_element_by_xpath("//*[@id='organic-div']/form/div[3]/button")
    element_aanmelden.click()

    return driver

def enter_keyword(keyword, driver):
    job_search = driver.find_element_by_xpath("//*[starts-with(@id, 'jobs-search-box-keyword-id-')]")
    job_search.send_keys(keyword+"\n")
    return driver

def scroll_load_job_cards(driver):

    scrollable_element = driver.find_element_by_class_name("jobs-search-results-list")
    scroll_length = scrollable_element.size['height']/2

    for i in range(0,15):
        driver.execute_script("arguments[0].scroll(0,"+str(i*scroll_length)+");", scrollable_element)
        time.sleep(0.5)
    return driver

def get_li_tags(driver):
    html__ = driver.find_element_by_class_name("jobs-search-results-list").get_attribute('innerHTML')
    doc__ = BeautifulSoup(html__, 'html.parser')
    li_tags = doc__.find_all('li',attrs={'class': lambda e: e.startswith('artdeco-pagination__indicator') if e else False})
    return li_tags

def page_numbers(li_tags):
    current_page = [x for x in li_tags if "active selected ember-view" in str(x)][0]
    current_page_number = str(current_page).split('data-test-pagination-page-btn="')[1].split('" id=')[0]
    next_page_number = str(int(current_page_number)+1)
    last_page_number = str(li_tags[-1]).split('data-test-pagination-page-btn="')[1].split('" id=')[0]

    return current_page_number, next_page_number, last_page_number

# def page_ember(li_tags, page_num):
#     string_tag = str([x for x in li_tags if f'data-test-pagination-page-btn="{page_num}"' in str(x)][0])
#     ember = string_tag.split('id="')[1].split('">')[0]
#     return ember

def page_ember(li_tags, page_num):
    string_tag = str([x for x in li_tags if f'aria-label="Pagina {page_num}"' in str(x)][0])
    ember = string_tag.split('id="')[1].split('">')[0]
    return ember

def get_ids_on_page(driver):
    html_ = driver.page_source
    doc = BeautifulSoup(html_,"html.parser")
    html_class = 'disabled ember-view job-card-container__link job-card-list__title'
    tags = doc.find_all("a", {"class" : html_class})
    job_ids = [x['href'].split('/')[3] for x in tags]
    return job_ids