import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

from functions import navigate_login, load_ids, navigate_job, get_job_description_html_text
from functions import get_primary_card, clean_primary, get_secondary_card, get_skills

"""
First piece of code below runs once to initialise the driver
""" 
# set options and initialise webdriver
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

#login
driver = navigate_login(url='https://www.linkedin.com/jobs/',driver=driver)

#load ids in pandas dataframe
df = load_ids(date='2023-05-03')

"""
Second piece of code will be looped to retrieve data for all found job_ids
"""
#line below replace to iterate over all job ids
job_ids = df['job_id']
for j in job_ids:
    #navigate to job page
    driver = navigate_job(j,driver=driver)

    #retrieve all data
    print(j)
    primary_raw = get_primary_card(driver=driver)
    primary_list = clean_primary(primary_raw)
    print(primary_list)
    secondary_list = get_secondary_card(driver)
    skills_list = get_skills(driver)
    print(secondary_list)
    print(skills_list)
    html,text = get_job_description_html_text(driver=driver)
    print(text)


