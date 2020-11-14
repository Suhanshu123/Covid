#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:24:03 2020

@author: suhanshu
"""

import pymysql
from tabulate import tabulate
import requests
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client

page_url = "https://www.mohfw.gov.in/"

uClient = uReq(page_url)

page_soup = soup(uClient.read(), "html.parser")
uClient.close()

header=["Date","Heading","Link"]

tableName = ["Travel", "Behavioural",
            "Citizens" ,"Hospitals" ,"Training", "States", "Employees", "Awareness",
            "Inspirational"]
# <--------------------------------------------Sql Part---------------------------------------------->

db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='Advisory',
)
c = db.cursor()

def create_table(table_name):
    try:
        c.execute("CREATE TABLE "+str(table_name)+" (Date VARCHAR(255), Heading VARCHAR(255),Link VARCHAR(255))")
    except:
        print(table_name + "Failed")
        pass



def insert_data(table_name, date, head, link, c, conn1):
    print("insert_data started : ")
    length = len(date)
    for i in range(0, length):
        Date= date[i]
        Heading= head[i]
        Link=  link[i]
        # print(type(str(Date)))
        # print("date is : "+ Date)
        # print(type(Heading))
        # print("head is : "+ Heading)
        # print(type(Link))
        # print("link is : "+ Link)
        try:
            #will execute this part when first time insert needs to be done
            arguments=(Date, Heading, Link)

            query="INSERT INTO "+str(table_name)+" (Date, Heading, Link) VALUES (%s,%s,%s)"
            c.execute(query,arguments)
        except:
            #This will execute when table is their and we have to update the entries
            arguments=(Date, Heading, Link)
            query="UPDATE "+str(table_name)+" SET Date = %s , Heading = %s , Link= %s"
            c.execute(query,arguments)
        #print("after execution")
        conn1.commit()

def print_data(table_name,c,conn1):
        query=" SELECT * FROM "+str(table_name)+" "
        c.execute(query)
        rows = c.fetchall()
        print(tabulate(rows, header, tablefmt="fancy_grid"))



# <--------------------------------------------Sql Part---------------------------------------------->

# <---------------------Creating Table---------------------------------------->

for name in tableName:
    
    create_table(name)

# <---------------------fetching part---------------------------------------->
containers = page_soup.findAll("div", {"class": "tab"})

for container in containers:
  subcontainer = page_soup.findAll("div", {"class": "panes"})
  i = 0
  for contain in subcontainer:
    a = contain.findAll("li")
    date = []
    head = []
    link = []
    for list in a:
        if((list.find("a") and list.find("span"))):
            
            date.append(list.find("span").text)
            b = list.find("a")
            head.append(b.text.strip())
            link.append(b["href"])
    #         print(list.find("span").text)
    #         print(list.find("a").text.strip())
    #         print(list.find("a")["href"])
    # print("i is : "+ str(i))
    # print("Table name is :" + tableName[i])
    # print("len of date is : "+ str(len(date)))
    # print("len of heading is : "+ str(len(head)))
    # print("len of link is : "+ str(len(link)))
    insert_data(tableName[i], date, head, link, c, db)
    i = i+1
# <---------------------fetching part---------------------------------------->
for name in tableName:
    print_data(name,c,db)