from selenium import webdriver
import os
import login
import json

#required library
# decouple , selenium  + selenium exe


def collectTitleAndAddressByPage():
    global index
    lectures = driver.find_elements_by_class_name('lecture-tit')
    count = len(lectures)
    for i in range(count):
        driver.execute_script("document.getElementsByClassName('lecture-tit')[{}].getElementsByTagName('a')[0].click()".format(i))
        driver.implicitly_wait(2)
        title = driver.find_element_by_class_name('detail-title').find_element_by_class_name('left').text
        lectureFiles = driver.find_element_by_class_name('file-list').find_elements_by_tag_name('a')
        subTitles = []
        subAddresses = []
        for lectureFile in lectureFiles:
            if lectureFile:
                subtitle = lectureFile.text
                subTitles.append(subtitle)
                address = lectureFile.get_attribute('onclick').split("'")[1]
                subAddresses.append('http://edu.ssafy.com/data/upload_files/crossUpload/openLrn/ebook/unzip/{}/index.html'.format(address))
        backButton = driver.find_element_by_xpath('//*[@id="wrap"]/div/div[2]/div/div/div[3]/div/div/button')
        backButton.click()

        detail = dict()
        detail['title'] = title
        detail['subTitles'] = subTitles
        detail['subAddresses'] = subAddresses
        theDict[index] = detail
        index += 1

# (1) chrome driver 다운로드
# chrome://version 을  통해서 chrome 버전을 확인하고 크롬 버전 및 운영체제에 맞는 버전을 확인해서 다운로드한다
# https://sites.google.com/a/chromium.org/chromedriver/downloads

driver = login.do()
# 자율학습 자료
driver.implicitly_wait(2)
driver.get('http://edu.ssafy.com/edu/lectureroom/openlearning/openLearningList.do')
driver.implicitly_wait(2)

search_count = driver.find_element_by_class_name('search-count').find_element_by_tag_name('em').text
search_count = int(search_count)

# 1번, 글 제목 / 타이틀리스트 /주소리스트
theDict = dict()
index = 0

while index < search_count:
    driver.implicitly_wait(2)
    collectTitleAndAddressByPage()
    nextbutton = driver.find_element_by_css_selector('#paging > li.next')
    nextbutton.click()

totalAddressCount = 0 
for k,v in theDict.items():
    totalAddressCount += len(v['subAddresses'])

print('글 개수 :{} , 전체 주소 개수: {}'.format(search_count, totalAddressCount))
with open('data.json', 'w') as outfile:
    json.dump(theDict, outfile)

