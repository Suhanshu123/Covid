import pymysql
from tabulate import tabulate
import requests
from bs4 import BeautifulSoup

url="https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/"

r=requests.get(url)
soup=BeautifulSoup(r.content,'html.parser')

db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='Covid',
)
c = db.cursor()

# c.execute("CREATE DATABASE CovidDB")
# c.execute("CREATE DATABASE Adviosry")
# c.execute("DROP TABLE Hello")

# c.execute("SHOW TABLES")
# databases = c.fetchall()
# print(databases)
# for database in databases:
#     print(database)

# c.execute("SHOW DATABASES")
# databases = c.fetchall()
# print(databases)
# for database in databases:
#     print(database)


def create_table(table_name):
    try:
        c.execute("CREATE TABLE "+str(table_name)+" (Name VARCHAR(255) PRIMARY KEY, Cases INT(11), Increased_cases INT(11), Cured INT(11), Cured_and_Sent INT(11), Active INT(11), Deaths INT(11), Deaths_Today INT(11))")
    except:
        pass
header=["Name","Cases","Increased_cases","Cured","Cured_and_Sent","Active","Deaths","Deaths_Today"]
def insert_data(table_name,arr,c,conn1):
    for i in arr:
        Name=i[0]
        Cases=i[1]
        Increased_cases=i[2]
        Cured=i[3]
        Cured_and_Sent=i[4]
        Active=i[5]
        Deaths=i[6]
        Deaths_Today=i[7]

        try:
            #will execute this part when first time insert needs to be done
            arguments=(Name,Cases,Increased_cases,Cured,Cured_and_Sent,Active,Deaths,Deaths_Today)
            query="INSERT INTO "+str(table_name)+" (Name, Cases, Increased_cases, Cured, Cured_and_Sent, Active, Deaths, Deaths_Today) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            c.execute(query,arguments)
        except:
            #This will execute when table is their and we have to update the entries
            arguments=(Cases,Increased_cases,Cured,Cured_and_Sent,Active,Deaths,Deaths_Today,Name)
            query="UPDATE "+str(table_name)+" SET Cases = %s , Increased_cases = %s , Cured= %s , Cured_and_Sent = %s , Active = %s , Deaths = %s , Deaths_Today = %s WHERE Name = %s"
            c.execute(query,arguments)
        #print("after execution")
        conn1.commit()
def print_data(table_name,c,conn1):
        query=" SELECT * FROM "+str(table_name)+" "
        c.execute(query)
        
        rows = c.fetchall()
        print(tabulate(rows, header, tablefmt="fancy_grid"))

states=[]
state_name=""
for i in soup.find_all("div","skgm-states"):
    state=[]
    
    for j in i.find_all("span","show-district"):
        #print("state name= ",j.text)   #got the state name
        state.append(j.text)
        state_name=j.text
        state_name=state_name.replace(' ','_')
        create_table(state_name)
    for k in i.find_all("div","skgm-td"):   
        for k1 in k.findAll("div","td-sc"):
            #print(k1.text,end=" ")  #   cases
            state.append(k1.text)
        for k2 in k.findAll("div","td-sdc"):
            #print(k2.text)  # increase in cases
            if(k2.text==''):
                state.append('0')
            else:
                state.append(k2.text)
        for k1 in k.findAll("div","td-sr"):
            #print(k1.text,end=" ")  #   cured cases
            state.append(k1.text)
        for k2 in k.findAll("div","td-sdr"):
            #print(k2.text)  #   increase in cured cases
            if(k2.text==''):
                state.append('0')
            else:
                state.append(k2.text)
        for k1 in k.findAll("div","td-sa"):
            #print(k1.text)  #active cases
            state.append(k1.text)
        for k2 in k.findAll("div","td-sd"):
            #print(k2.text,end=" ")  #total fatalities
            state.append(k2.text)
        for k2 in k.findAll("div","td-sdd"):
            #print(k2.text)  #todays fatality
            #state.append(k2.text)
            if(k2.text==''):
                state.append('0')
            else:
                state.append(k2.text)
    states.append(state)
    
    districts=[]
    #print("==========districts shown here=============")
    for res in i.find_all('div'):
        count=0
        
        for k in res.find_all("div","skgm-tr"):
            count=0
            district=[]
            for l in k.find_all("div","skgm-td"):
                if(count==0):
                    #print("city name= ",l.text)
                    district.append(l.text)
                elif(count==1):
                    for l in k.find_all("div","td-dc"):
                        #print("cases= ",l.text,end=" ")
                        district.append(l.text)
                    for l in k.find_all("div","td-ddc"):
                        #print("increase= ",l.text)   # increases in cases
                        if(l.text==''):
                            district.append('0')
                        else:
                            district.append(l.text)
                elif(count==2):
                    for l in k.find_all("div","td-dr"):
                        #print("cured= ",l.text,end=" ")
                        district.append(l.text)
                    for l in k.find_all("div","td-ddr"):
                        #print("increase= ",l.text)
                        if(l.text==''):
                            district.append('0')
                        else:
                            district.append(l.text)
                elif(count==3):
                    for l in k.find_all("div","td-da"):
                        #print("active= ",l.text)
                        district.append(l.text)
                elif(count==4):
                    for l in k.find_all("div","td-dd"):
                        #print("fatalities= ",l.text,end=" ")
                        district.append(l.text)
                    for l in k.find_all("div","td-ddd"):
                        #print("today's mortality= ",l.text)#todays fatality count
                        if(l.text==''):
                            district.append('0')
                        else:
                            district.append(l.text)
                count+=1
            #print(district)
            districts.append(district)
    insert_data(state_name,districts, c, db)
    print_data(state_name, c, db)
create_table("States")
table_name="States"
insert_data(table_name,states,c,db)
print_data(table_name,c,db)
# browser.close()
# browser.quit()

