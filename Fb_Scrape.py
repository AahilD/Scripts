#auto facebook login.
from tkinter import *  #GUI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

def extractName(link):
    friendName = ""
    try:
        extractLink = link.replace("https://www.facebook.com/", "")
        for char in extractLink:
            if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
                friendName += char
            if char == ".":
                friendName += " "
            if char == "?" or char == "/":
                break
        return friendName
    except AttributeError:
        print()


def extractInfo(browser, link):
    browser.get(link)

    content = browser.page_source
    soup = BeautifulSoup(content, features="html.parser")

    for a in soup.find_all("a", {"data-tab-key": "about"}):
        link_href = a.get("href")
        browser.get(link_href)


    content = browser.page_source
    soup = BeautifulSoup(content, features="html.parser")
    for span in soup.find_all("span", {"class": "_c24 _2ieq"}):
        span = str(span)
        extractSpan = span.replace(""" <span class="_c24 _2ieq"><div><span class="accessible_elem"> """, '')

        for char in extractSpan:
            if char == "P":
                phoneNumber = ""
                extractSpan2 = span.replace('<span class="_c24 _2ieq"><div><span class="accessible_elem">Phones</span></div><div><span dir="ltr">', '')
                for char in extractSpan2:
                    if (char != "<"):
                        phoneNumber += char
                    else:
                        print(phoneNumber)
                        break

            if char == "E":
                email = ""
                extractSpan2 = span.replace('<span class="_c24 _2ieq"><div><span class="accessible_elem">Email</span></div><div><a href="mailto:dosani%40hotmail.ca">', '')
                for char in extractSpan2:
                    if (char != "<"):
                        email += char
                    else:
                        print(email)
                        break

            if char == "B":
                birthday = ""
                extractSpan2 = span.replace('<span class="_c24 _2ieq"><div><span class="accessible_elem">Birthday</span></div><div>', '')
                for char in extractSpan2:
                    if (char != "<"):
                        birthday += char
                    else:
                        print(birthday)
                        break


def login():
    browser = webdriver.Chrome()
    browser.get("") #enter address to friends list in ""
    login = browser.find_element_by_id("email")
    passw = browser.find_element_by_id("pass")
    login.send_keys("") #enter email in ""
    passw.send_keys("")   #enter password in ""
    browser.find_element_by_id("u_0_2").click()

    #browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    SCROLL_PAUSE_TIME = 0
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    list_link = []
    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    content = browser.page_source
    soup = BeautifulSoup(content, features="html.parser")
    for link in soup.find_all('a'):
        link_href = link.get('href')
        extractedName = extractName(link_href)
        if extractedName in list_link:
            print()
        else:
            list_link.append(extractedName)

    for divs in soup.find_all("div", {"class": "fsl fwb fcb"}):
        for a in divs:
            link_href = a.get("href")
            print(link_href)
            extractInfo(browser, link_href)


    df = pd.DataFrame({'Friend Name':list_link})
    df.to_csv('friends1.csv', index=False, encoding='utf-8')
    print("done!")

root = Tk()
root.title("Facebook Login")
root.geometry("200x100")
app=Frame(root)
app.grid()
but=Button(text="login",command=login)
but.grid()
root.mainloop()
