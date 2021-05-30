import requests 
from bs4 import BeautifulSoup
import urllib3
import json

http = urllib3.PoolManager()
r = http.request("GET", "https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=工程師&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=11&asc=0&page=1&mode=s&jobsource=2018indexpoc")
soup = BeautifulSoup(r.data,'lxml')
soup = soup.find("div", {"id" : "js-job-content"})
soup = soup.find_all("h2",{"class":'b-tit'})
next = soup[10].find('a').get('href') #前面十個職缺都是廣告，故從第十一個開始爬

jobNo = "https:"+next
jobNo = jobNo[jobNo.find('/job')+5:jobNo.find('?jobsource')]

url = 'https://www.104.com.tw/job/ajax/content/{jobNo}'.format(jobNo = jobNo)
headers = {
    "Referer": "https://www.104.com.tw/job/{jobNo}".format(jobNo = jobNo),
}

sub_job = http.request("GET", url,headers=headers)
json.loads(sub_job.data)
json.dump(json.loads(sub_job.data),open('data.json','w+',encoding='utf-8'),indent=4)