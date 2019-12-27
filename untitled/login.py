from selenium import webdriver
from decouple import config

def do():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.implicitly_wait(3)
    driver.get('https://edu.ssafy.com')

    driver.find_element_by_id('userId').send_keys(config('USERID'))
    driver.find_element_by_id('userPwd').send_keys((config('USERPWD')))
    driver.find_element_by_xpath('//*[@id="wrap"]/div/div/div[2]/form/div/div[2]/div[3]/a').click()
    return driver
