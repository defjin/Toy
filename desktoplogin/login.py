#https://www.simplifiedpython.net/python-gui-login/
#https://www.datacamp.com/community/tutorials/gui-tkinter-python
#https://pypi.org/project/chromedriver-binary/75.0.3770.140.0/

#%%file = homepath + r'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'

from tkinter import *
from selenium import webdriver
import os
from datetime import datetime
import edussafylogin


def login():
    if check_empty() : return
    username_info = username.get()
    password_info = password.get()
    loginfile = open(homepath+'\\username.txt','w')
    loginfile.write(username_info)
    loginfile.close()
    edussafylogin.login(username_info, password_info, True)
    
def logout():
    username_info = username.get()
    password_info = password.get()
    edussafylogin.login(username_info, password_info, False)
    
def reset_screen():
    yesBtn.forget()
    noBtn.forget()
    loginBtn.pack()
    logoutBtn.pack()
    sixLabel.forget()

def check_empty():
    if username.get() == '' or password.get() == '':
        notyLabel.pack()
        return True
    return False

def logoutcheck():
    if check_empty() : return
    if datetime.now().hour <= 18:
        notyLabel.forget()
        global sixLabel
        sixLabel = Label(main_screen, text = '6시 전입니다.\n 진짜 퇴실하시겠습니까?')
        sixLabel.pack()
        loginBtn.forget()
        logoutBtn.forget()
        global yesBtn
        global noBtn
        yesBtn = Button(text="Yes", height="1", width="15", command = logout)
        noBtn = Button(text="No", height="1", width="15", command=reset_screen)
        yesBtn.pack()
        noBtn.pack()
    else:
        logout()      

# Designing Main(first) window
def main_account_screen():
    global main_screen
    main_screen = Tk()
    filepath = homepath+'\\username.txt'
    if os.path.isfile(filepath):
        loginfile = open(filepath,'r')
        
    else:
        loginfile = open(filepath,'w')
    
    global username
    global password
    username = StringVar()
    password = StringVar()
    username.set(loginfile.read())

    main_screen.geometry("300x250")
    main_screen.title("간단입퇴실")
    Label(text="Username * ").pack()
    username_login_entry = Entry(main_screen, textvariable=username)
    username_login_entry.pack()
    Label(text="Password * ").pack()
    password_login_entry = Entry(main_screen, textvariable=password, show= '*')
    password_login_entry.pack()
    Label(text="").pack()
    global loginBtn
    global logoutBtn
    loginBtn = Button(text="입실", height="1", width="15", command = login)
    logoutBtn = Button(text="퇴실", height="1", width="15", command= logoutcheck)
    loginBtn.pack()
    logoutBtn.pack()
    global notyLabel
    notyLabel = Label(main_screen, text = '계정 또는 사용자비밀번호가 비었습니다.')
    notyLabel.forget()

    main_screen.mainloop()


#start of program
homepath = os.path.expanduser('~')
main_account_screen()