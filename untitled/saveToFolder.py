import login
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import json

def getEbookImages(address):
    driver.get(address)
    driver.implicitly_wait(3)
    imgNextButton = driver.find_element_by_xpath('/html/body/div[3]/aside/div[2]/div[1]/button[4]')
    srcList = set()
    while True:
        images = driver.find_elements_by_class_name('background')
        for image in images:
            src = image.get_attribute('src')
            srcList.add(src)
        if not imgNextButton.is_enabled():
            break
        imgNextButton.click()
    return sorted(list(srcList))


def saveToFolder(ebookAddress, foldername):
    imgList = getEbookImages(ebookAddress)
    imageAddress = os.path.join(BASE_DIR, foldername)
    os.makedirs(imageAddress)
    driver.maximize_window()
    for i in range(len(imgList)):
        filename = imgList[i].split('/')[-1]
        driver.get(imgList[i])
        driver.implicitly_wait(1)
        action = ActionChains(driver)
        action.context_click(driver.find_element_by_tag_name('img')).key_down('v').perform()
        driver.find_element_by_tag_name('img').screenshot(imageAddress + "\\" + filename.split(".")[0] + ".png")



driver = login.do()
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "untitled")

# driver 페이지 전환으로 잊어버림. 고쳐야 됨.
with open('data.json') as json_file:
    data = json.load(json_file)
    for address, title in data.items():
        print(address)
        print(title)
        saveToFolder(address, title)
