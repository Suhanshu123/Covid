from bs4 import BeautifulSoup
import requests
#url="https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=covid+19&btnG="


for i in range(0,5):
    url="https://scholar.google.com/scholar?start="+str(i*10)+"&q=covid+19&hl=en&as_sdt=0,5"
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'html.parser')
    
    for containers in soup.findAll("h3", {"class": "gs_rt"}):
        #print(containers)
        for i in containers.findAll("a",href=True):
            print(i.text,"->",i["href"])
