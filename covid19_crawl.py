'''author:TwistingTornadoes

'''
# for running this you need to install selenium


from bs4 import BeautifulSoup
import time
from selenium import webdriver
import requests
import urllib.request
url = "https://maps.covidindia.org/?state=UP"
browser = webdriver.Firefox()

browser.get(url)
time.sleep(3)
html = browser.page_source
soup = BeautifulSoup(html, "lxml")

print("here is the data guys")
for item in soup.findAll("table","table table-bordered maptable"):
    for ele in item.findAll('tr'):
        column_count=ele.findAll('td')
        count=0
        for i in column_count:
            if(count==0):
                print("col---->",i.text)
            elif(count==1):
                par=i.find("span","val1")
                print(par.text,end=" ")
                par=i.find("span","cl3")
                print(par.text)
            elif(count==2):
                par=i.find("span","val1")
                print(par.text,end=" ")
                par=i.find("span","cl2")
                print(par.text)
            elif(count==3):
                par=i.find("span","val1")
                print(par.text,end=" ")
                par=i.find("span","cl1")
                print(par.text)
            count+=1

browser.close()
browser.quit()
