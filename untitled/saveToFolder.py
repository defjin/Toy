import login
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import os
import json
import pyautogui
import requests
import time

#https://crosp.net/blog/software-development/web/download-images-using-webdriverio-selenium-webdriver/
# javascript download origin image file
#https://stackoverflow.com/questions/17527713/force-browser-to-download-image-files-on-click
# download multiple allow
# https://stackoverflow.com/questions/46937319/how-to-use-chrome-webdriver-in-selenium-to-download-files-in-python
# 동시에 파일을 많이 받으면 소켓 개수 제한이 걸린다.
# https://smallpdf.com/jpg-to-pdf 개좋은 변환툴

def getEbookImages(address):
    driver.get(address)
    driver.implicitly_wait(3)
    imgNextButton = driver.find_element_by_xpath('/html/body/div[3]/aside/div[2]/div[1]/button[4]')
    toggleButton = driver.find_element_by_xpath('/html/body/div[3]/aside/div[2]/div[2]/button[2]')
    if toggleButton.get_attribute('class') == 'btn active':
        toggleButton.click()

    pageLabel = driver.find_element_by_class_name('label-page')
    totalPageNum = pageLabel.text.split('/')[-1]
    print(totalPageNum) # 1부터 pageNum까지

    srcList = []
    for i in range(1, int(totalPageNum)+1):
        #이건 원래코드
        pageWrappers = driver.find_elements_by_class_name('page-wrapper') 
        for wrapper in pageWrappers:
           if i == int(wrapper.get_attribute('page')):
                images = wrapper.find_elements_by_tag_name('img')
                for image in images:
                    src = image.get_attribute('src')
                    srcList.append(src)
        # 간혹 풀 레코드 다 올라와있는 경우가 생김. 그런 경우만 사용
        # pageWrappers = driver.find_elements_by_tag_name('section')
        # wrapper = pageWrappers[i-1]
        # images = wrapper.find_elements_by_tag_name('img')
        # for image in images:
        #     src = image.get_attribute('src')
        #     srcList.append(src)
        if imgNextButton.is_enabled():
            imgNextButton.click()
    return srcList


def saveToFolder(ebookAddress, foldername):
    imgList = getEbookImages(ebookAddress)
    imageAddress = os.path.join(DOWN_DIR, "SSAFYTEXT", foldername)
    print(imageAddress)
    if not os.path.isdir(imageAddress):
        os.makedirs(imageAddress)
    print(len(imgList))
    print(foldername)
    for i in range(len(imgList)):
        imgUrl = '"' + imgList[i] + '"'
        name = imgList[i].split('/')[-1]
        filename = f'"{i}_{name}"'
        filename = filename.replace('\\','\\\\')
        script = f'var link = document.createElement("a");link.href = { imgUrl }; link.download = {filename};document.body.appendChild(link);link.click();document.body.removeChild(link);'
        driver.execute_script(script)
        time.sleep(0.2)

    time.sleep(1)
    for i in range(len(imgList)):
        # 나중엔 덮어쓰기도 고려해봐야.
        name = f"{i}_{imgList[i].split('/')[-1]}"
        os.rename(os.path.join(DOWN_DIR, name), os.path.join(imageAddress, name))
    


driver = login.do()
#BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "untitled")
DOWN_DIR = 'C:\\Users\\Jin\\Downloads'

with open('data.json') as json_file:
    data = json.load(json_file)
    for num, detail in data.items():
        if int(num) < 32: 
            continue
        if int(num) > 32: 
            continue
        if len(detail['subTitles']) > 1:
            for i in range(len(detail['subTitles'])):
                address = detail['subAddresses'][i]
                title = detail['title'] + '_' + detail['subTitles'][i]
        else:
            address = detail['subAddresses'][0]
            title = detail['title']
        try:
            saveToFolder(address, title)
            print('현재 id {} 진행 완료'.format(num))
        except:
            print('error')
            print('현재 id {} 진행 중 종료됨'.format(num))
    print('전체 종료')
