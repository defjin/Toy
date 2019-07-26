from selenium import webdriver
import chromedriver_binary
from pprint import pprint
import time
import csv

def run():
    driver = webdriver.Chrome()
    loginurl = 'https://swexpertacademy.com/main/identity/anonymous/loginPage.do'
    driver.get(loginurl)
    username = driver.find_element_by_id("id")
    username.clear()
    username.send_keys('')
    password = driver.find_element_by_id("pwd")
    password.clear()
    password.send_keys('')

    #driver.find_element_by_name("로그인").click()
    #driver.find_element_by_xpath('//*[@id="LoginForm"]/div/div/div[2]/div/div/fieldset/div/div[4]/button').click()
    driver.find_element_by_css_selector('#LoginForm > div > div > div.member_wrap > div > div > fieldset > div > div.btn_wrap > button').click()
    #driver.find_element_by_xpath('//*[@id="LoginForm"]/div/div/div[2]/div/div/fieldset/div/div[4]/button').get_attribute('onclick')
    #print()

    problemInfoList = []

    for pageIndex in range(1,18):
        pageurl = f'https://swexpertacademy.com/main/code/problem/problemList.do?problemTitle=&orderBy=FIRST_REG_DATETIME&select-1=&pageSize=30&pageIndex={pageIndex}'
        driver.get(pageurl)
        time.sleep(0.5)

        for num in range(1,31):
            if pageIndex==17 and num > 24 : 
                continue 
            pro_path = f'//*[@id="searchForm"]/div[2]/div/div/div[2]/div/div[2]/div[{num}]/div[1]/div[1]/span[2]/a'
            driver.find_element_by_xpath(pro_path).click()
            # 최종page
            time.sleep(1)
            #
            title = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[1]/p').text
            title_infos = title.split()
            title_info_dict = dict()
            title_info_dict['번호'] = title_infos[0][:-1]
            if title_infos[-1] == 'Attack':
                title_info_dict['제목'] = ''.join(title_infos[1:-2])
                title_info_dict['난이도'] = title_infos[-2]
            else :
                title_info_dict['제목'] = ''.join(title_infos[1:-1])
                title_info_dict['난이도'] = title_infos[-1]
            title_info_dict['C'] = 'X'
            title_info_dict['C++'] = 'X'
            title_info_dict['Java'] = 'X'
            title_info_dict['Python'] = 'X'
            
            #언어
            lantexts = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[7]/div/div[1]/ul/li[1]/span[2]').text.split('/')
            for lantext in lantexts:
                if 'C' in lantext and 'C++' not in lantext:
                    title_info_dict['C'] = 'O'
                elif 'C++' in lantext:
                    title_info_dict['C++'] = 'O'
                elif 'Java' in lantext:
                    title_info_dict['Java'] = 'O'
                elif 'Python' in lantext:
                    title_info_dict['Python'] = 'O'
                else:
                    pass

            problemInfoList.append(title_info_dict)
            driver.back()
            time.sleep(1)
            

    print(problemInfoList)

    with open('swProblem.csv','w', encoding='utf-8',newline='') as f:
        fieldnames = ['번호','제목','난이도','C','C++','Java','Python']
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()
        for problemInfo  in problemInfoList:
            writer.writerow(problemInfo)
        
        
if __name__ == '__main__':
    run()    

 

