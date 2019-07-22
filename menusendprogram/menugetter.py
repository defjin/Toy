import requests
import bs4
from selenium import webdriver
import urllib
from decouple import config
import slack


def getMenuImage(address) :
    chromedriver_dir = r'C:\Users\student\Downloads\chromedriver_win32\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_dir)

    inputusername = config("USERID") #사용자이름
    inputuserpwd  = config("USERPASSWORD") #사용자 비밀번호

    loginurl = "https://edu.ssafy.com/comm/login/SecurityLoginForm.do"
    driver.get(loginurl)
    username = driver.find_element_by_id("userId")
    username.clear()
    username.send_keys(inputusername)
    password = driver.find_element_by_id("userPwd")
    password.clear()
    password.send_keys(inputuserpwd)

    #driver.find_element_by_name("로그인").click()
    driver.find_element_by_css_selector("#wrap > div > div > div.section > form > div > div.field-set.log-in > div.form-btn > a").click()


    #로그인 과정 완료 후 공지사항으로 이동.
    noticeurl = "https://edu.ssafy.com/edu/board/notice/list.do"
    driver.get(noticeurl)
    # 공지사항에서 <중식시간>이라는 글을 찾아서 가장 번호가 높은 것을 받아내자.
    
    html = driver.page_source
    # 왜 res.text = "" ? 비어있어서 뒤로 진행이 안됨. js 때문인가? 
    # driver 를 통해서 직접 가져오자.
    doc = bs4.BeautifulSoup(html, 'html.parser')
    # 공지사항 아래의 것들을 가져온다
    # 어떻게 찾은 위치로 들어가게 할 수 있지 ?.
    # # > tbody > tr" : 여기까지 쓰면 셀레니움이 꺼져버림...??? 단순 크래시의 문제는 버전 문제일수도???
    position = "#wrap > form > div > div.content > div.section > div.board-wrap > table.default-tbl.type2 > tbody" 
    noticebox = doc.select_one(position)
    #print(noticebox)
    notices = noticebox.find_all("tr")
    #print(notices)

    launches = []
    for notice in notices :
         if "중식" in notice.text :
              launches.append(notice)
    
    # launches[0] 가 최신
    # 찾아냈다면 해당되는 페이지를 클릭해 내부 진입 후 그림을 찾아 다운로드한다.
    target = launches[0].a['onclick'] # onclick attribute에 해당되는 값을 받는다.
    # target : fnDetail('2588'); 함수
    driver.execute_script(target)

    html = driver.page_source
    doc = bs4.BeautifulSoup(html,'html.parser')
    #tr:nth-child of 와 같은 식으로 사용할 수 없다. nth-of-type처럼 사용해야 beautiful soup에서 인식가능
    imagebox =  doc.select_one("#wrap > form > div > div.content > div > div:nth-of-type(1) > div.datail-content.mb20 > p > img")
    imageurl = imagebox['src']
    
    #res = urllib.request.urlretrieve("https:" + imageurl, address +"\menu.png")
    fullimageurl = 'https:' + imageurl
    slack_token = config("TESTMENUSLACKTOKEN") # test
    client = slack.WebClient(token = slack_token)
    # 두 가지 방식으로 전달 가능
    # block, and download
  #https://api.slack.com/tools/block-kit-builder?blocks=%5B%7B%22type%22%3A%22section%22%2C%22text%22%3A%7B%22type%22%3A%22mrkdwn%22%2C%22text%22%3A%22Hello%2C%20Assistant%20to%20the%20Regional%20Manager%20Dwight!%20*Michael%20Scott*%20wants%20to%20know%20where%20you%27d%20like%20to%20take%20the%20Paper%20Company%20investors%20to%20dinner%20tonight.%5Cn%5Cn%20*Please%20select%20a%20restaurant%3A*%22%7D%7D%2C%7B%22type%22%3A%22divider%22%7D%2C%7B%22type%22%3A%22section%22%2C%22text%22%3A%7B%22type%22%3A%22mrkdwn%22%2C%22text%22%3A%22*Farmhouse%20Thai%20Cuisine*%5Cn%3Astar%3A%3Astar%3A%3Astar%3A%3Astar%3A%201528%20reviews%5Cn%20They%20do%20have%20some%20vegan%20options%2C%20like%20the%20roti%20and%20curry%2C%20plus%20they%20have%20a%20ton%20of%20salad%20stuff%20and%20noodles%20can%20be%20ordered%20without%20meat!!%20They%20have%20something%20for%20everyone%20here%22%7D%2C%22accessory%22%3A%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fs3-media3.fl.yelpcdn.com%2Fbphoto%2Fc7ed05m9lC2EmA3Aruue7A%2Fo.jpg%22%2C%22alt_text%22%3A%22alt%20text%20for%20image%22%7D%7D%2C%7B%22type%22%3A%22section%22%2C%22text%22%3A%7B%22type%22%3A%22mrkdwn%22%2C%22text%22%3A%22*Kin%20Khao*%5Cn%3Astar%3A%3Astar%3A%3Astar%3A%3Astar%3A%201638%20reviews%5Cn%20The%20sticky%20rice%20also%20goes%20wonderfully%20with%20the%20caramelized%20pork%20belly%2C%20which%20is%20absolutely%20melt-in-your-mouth%20and%20so%20soft.%22%7D%2C%22accessory%22%3A%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fs3-media2.fl.yelpcdn.com%2Fbphoto%2Fkorel-1YjNtFtJlMTaC26A%2Fo.jpg%22%2C%22alt_text%22%3A%22alt%20text%20for%20image%22%7D%7D%2C%7B%22type%22%3A%22section%22%2C%22text%22%3A%7B%22type%22%3A%22mrkdwn%22%2C%22text%22%3A%22*Ler%20Ros*%5Cn%3Astar%3A%3Astar%3A%3Astar%3A%3Astar%3A%202082%20reviews%5Cn%20I%20would%20really%20recommend%20the%20%20Yum%20Koh%20Moo%20Yang%20-%20Spicy%20lime%20dressing%20and%20roasted%20quick%20marinated%20pork%20shoulder%2C%20basil%20leaves%2C%20chili%20%26%20rice%20powder.%22%7D%2C%22accessory%22%3A%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fs3-media2.fl.yelpcdn.com%2Fbphoto%2FDawwNigKJ2ckPeDeDM7jAg%2Fo.jpg%22%2C%22alt_text%22%3A%22alt%20text%20for%20image%22%7D%7D%2C%7B%22type%22%3A%22divider%22%7D%2C%7B%22type%22%3A%22actions%22%2C%22elements%22%3A%5B%7B%22type%22%3A%22button%22%2C%22text%22%3A%7B%22type%22%3A%22plain_text%22%2C%22text%22%3A%22Farmhouse%22%2C%22emoji%22%3Atrue%7D%2C%22value%22%3A%22click_me_123%22%7D%2C%7B%22type%22%3A%22button%22%2C%22text%22%3A%7B%22type%22%3A%22plain_text%22%2C%22text%22%3A%22Kin%20Khao%22%2C%22emoji%22%3Atrue%7D%2C%22value%22%3A%22click_me_123%22%7D%2C%7B%22type%22%3A%22button%22%2C%22text%22%3A%7B%22type%22%3A%22plain_text%22%2C%22text%22%3A%22Ler%20Ros%22%2C%22emoji%22%3Atrue%7D%2C%22value%22%3A%22click_me_123%22%7D%5D%7D%2C%7B%22type%22%3A%22section%22%2C%22text%22%3A%7B%22type%22%3A%22mrkdwn%22%2C%22text%22%3A%22Take%20a%20look%20at%20this%20image.%22%7D%2C%22accessory%22%3A%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fapi.slack.com%2Fimg%2Fblocks%2Fbkb_template_images%2Fpalmtree.png%22%2C%22alt_text%22%3A%22palm%20tree%22%7D%7D%2C%7B%22type%22%3A%22section%22%2C%22text%22%3A%7B%22type%22%3A%22mrkdwn%22%2C%22text%22%3A%22Take%20a%20look%20at%20this%20image.%22%7D%2C%22accessory%22%3A%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fapi.slack.com%2Fimg%2Fblocks%2Fbkb_template_images%2Fpalmtree.png%22%2C%22alt_text%22%3A%22palm%20tree%22%7D%7D%2C%7B%22type%22%3A%22actions%22%2C%22elements%22%3A%5B%7B%22type%22%3A%22conversations_select%22%2C%22placeholder%22%3A%7B%22type%22%3A%22plain_text%22%2C%22text%22%3A%22Select%20a%20conversation%22%2C%22emoji%22%3Atrue%7D%7D%2C%7B%22type%22%3A%22channels_select%22%2C%22placeholder%22%3A%7B%22type%22%3A%22plain_text%22%2C%22text%22%3A%22Select%20a%20channel%22%2C%22emoji%22%3Atrue%7D%7D%2C%7B%22type%22%3A%22users_select%22%2C%22placeholder%22%3A%7B%22type%22%3A%22plain_text%22%2C%22text%22%3A%22Select%20a%20user%22%2C%22emoji%22%3Atrue%7D%7D%2C%7B%22type%22%3A%22static_select%22%2C%22placeholder%22%3A%7B%22type%22%3A%22plain_text%22%2C%22text%22%3A%22Select%20an%20item%22%2C%22emoji%22%3Atrue%7D%2C%22options%22%3A%5B%7B%22text%22%3A%7B%22type%22%3A%22plain_text%22%2C%22text%22%3A%22Excellent%20item%201%22%2C%22emoji%22%3Atrue%7D%2C%22value%22%3A%22value-0%22%7D%2C%7B%22text%22%3A%7B%22type%22%3A%22plain_text%22%2C%22text%22%3A%22Fantastic%20item%202%22%2C%22emoji%22%3Atrue%7D%2C%22value%22%3A%22value-1%22%7D%2C%7B%22text%22%3A%7B%22type%22%3A%22plain_text%22%2C%22text%22%3A%22Nifty%20item%203%22%2C%22emoji%22%3Atrue%7D%2C%22value%22%3A%22value-2%22%7D%2C%7B%22text%22%3A%7B%22type%22%3A%22plain_text%22%2C%22text%22%3A%22Pretty%20good%20item%204%22%2C%22emoji%22%3Atrue%7D%2C%22value%22%3A%22value-3%22%7D%5D%7D%5D%7D%2C%7B%22type%22%3A%22section%22%2C%22text%22%3A%7B%22type%22%3A%22mrkdwn%22%2C%22text%22%3A%22You%20can%20add%20an%20image%20next%20to%20text%20in%20this%20block.%22%7D%2C%22accessory%22%3A%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fapi.slack.com%2Fimg%2Fblocks%2Fbkb_template_images%2Fplants.png%22%2C%22alt_text%22%3A%22plants%22%7D%7D%2C%7B%22type%22%3A%22section%22%2C%22text%22%3A%7B%22type%22%3A%22mrkdwn%22%2C%22text%22%3A%22You%20can%20add%20an%20image%20next%20to%20text%20in%20this%20block.%22%7D%2C%22accessory%22%3A%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fapi.slack.com%2Fimg%2Fblocks%2Fbkb_template_images%2Fplants.png%22%2C%22alt_text%22%3A%22plants%22%7D%7D%2C%7B%22type%22%3A%22image%22%2C%22title%22%3A%7B%22type%22%3A%22plain_text%22%2C%22text%22%3A%22Example%20Image%22%2C%22emoji%22%3Atrue%7D%2C%22image_url%22%3A%22https%3A%2F%2Fapi.slack.com%2Fimg%2Fblocks%2Fbkb_template_images%2Fgoldengate.png%22%2C%22alt_text%22%3A%22Example%20Image%22%7D%5D
    client.chat_postMessage(
  channel="general",
  blocks=[
    {
		"type": "image",
		"title": {
			"type": "plain_text",
			"text": "Example Image",
			"emoji": True
		},
		"image_url": fullimageurl,
		"alt_text": "Example Image"
	}
  ]
)
#     client.files_upload(
#     #channels="menu",
#     channels = 'general',
#     file= fullimageurl,
#     title="Test upload"
     

if __name__ == "__main__" :
     address = r"C:\Users\student\Downloads"
     getMenuImage(address)
