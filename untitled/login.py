from selenium import webdriver
from decouple import config
from selenium.webdriver.chrome.options import Options

# 여러개 파일 다운을 위해서는 alert를 disalbe 처리해줘야한다.

def do():
    chrome_options = Options()
    prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome('chromedriver.exe',chrome_options=chrome_options)
    #driver = webdriver.Chrome('chromedriver.exe')
    driver.implicitly_wait(3)
    driver.get('https://edu.ssafy.com')

    driver.find_element_by_id('userId').send_keys(config('USERID'))
    driver.find_element_by_id('userPwd').send_keys((config('USERPWD')))
    driver.find_element_by_xpath('//*[@id="wrap"]/div/div/div[2]/form/div/div[2]/div[3]/a').click()
    return driver
