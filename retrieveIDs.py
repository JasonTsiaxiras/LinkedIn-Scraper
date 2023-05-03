from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from functions import navigate_login, enter_keyword, scroll_load_job_cards, get_li_tags, page_numbers, page_ember, get_ids_on_page
from functions import save_id_data, click_on_24_hours

# set options and initialise webdriver
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

driver = navigate_login(url='https://www.linkedin.com/jobs/',driver=driver)

search_keyword = 'Data Analyst'
driver = enter_keyword(keyword = search_keyword,driver= driver)
driver = click_on_24_hours(driver=driver)

driver = scroll_load_job_cards(driver=driver) 
# possible way to improve this is by using: driver.find_element_by_class_name("scaffold-layout__list-container").get_attribute('innerHTML')

li_tags = get_li_tags(driver=driver)
current_page_num, next_page_num, last_page_num = page_numbers(li_tags=li_tags)

for p in range(1,int(last_page_num)+1):

    driver = scroll_load_job_cards(driver=driver) 
    li_tags = get_li_tags(driver=driver)
    current_page_num, next_page_num, last_page_num = page_numbers(li_tags=li_tags)

    # Retrieve and parse job_cards html
    job_ids = get_ids_on_page(driver=driver)
    print(job_ids)

    if int(current_page_num) < int(last_page_num):
        next_ember = page_ember(li_tags,next_page_num)
        print(next_ember)
        driver.find_element_by_id(next_ember).click()

    save_id_data(search_keyword = search_keyword, scrape_date = str(pd.Timestamp.today().date()), job_ids = job_ids)
