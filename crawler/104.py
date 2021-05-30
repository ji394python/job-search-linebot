from bs4 import BeautifulSoup
from requests_html import HTMLSession
import urllib3
import csv 
import time


csvRows = list()

def main():
    job = "工程師"
    pages = 10

    #headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "\
    #        "Chrome/52.0.2743.116 Safari/537.36', 
    #        "Referer": "https://www.104.com.tw/job/6vrlf"}

    http = urllib3.PoolManager()

    for page in range(1, pages + 1):
        url = "https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={job}&expansionType=area%2Cspec%2" \
                "Ccom%2Cjob%2Cwf%2Cwktm&order=15&asc=0&page={page}&mode=s&jobsource=2018indexpoc".format(job = job, page = page)
        r = http.request("GET", url)
        soup = BeautifulSoup(r.data, "lxml")
        soup = soup.find("div", {"id" : "main-content"})
        articles = soup.find_all("article", {'class':'b-block--top-bord job-list-item b-clearfix js-job-item'})

        for article in articles:
            jobTitleTag = article.find("h2", { "class" : "b-tit" })
            companyTag = article.find("ul", { "class" : "b-list-inline b-clearfix" })
            requestSkillTag = article.find("ul", { "class" : "b-list-inline b-clearfix job-list-intro b-content" })
            jobDescript = article.find("p", { "class" : "job-list-item__info b-clearfix b-content" })
            inforTag = article.find("div", {"class" : "job-list-tag b-content"})

            job_and_date = findJobAndDate(jobTitleTag)
            company_and_relativeIndustry = findHTMLStructure(companyTag, "li")
            workAddr_reqYear_education = findHTMLStructure(requestSkillTag, "li")
            salary_otherInformation = findHTMLStructure(inforTag, "span")
            wrapCSVRow(job_and_date[0], company_and_relativeIndustry[0], 
                    job_and_date[1], workAddr_reqYear_education[1], 
                    salary_otherInformation[0], workAddr_reqYear_education[0], 
                    company_and_relativeIndustry[1], jobDescript.getText())

    writeCSV(job)

def findJobAndDate(tag):
    title = tag.find("a").getText()
    date = tag.find("span").getText()
    date = "".join([x for x in date if x != " " and x != "\n"])
    return (title, date)

def findHTMLStructure(tag, html_tag):
    h_list = tag.find_all(html_tag)
    retValue = tuple()
    for ele in h_list:
        eleStr = ele.getText()
        ele = "".join([x for x in eleStr if x != " " and x != "\n"])
        if ele != "":
            retValue = retValue + (ele,) 
    return retValue 

def wrapCSVRow(jobName, jobCompany, date, requestSkill, salary, addr, job_type, content):
    global csvRows
    csvRows.append([jobName, jobCompany, date, requestSkill, salary, addr, job_type, content])

def writeCSV(job):
    global csvRows
    with open("data/"+job + "_work.csv", "w+", newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["職缺", "職缺公司", "職缺日期", "職缺技術", "薪水", "工作地點", "職務類別", "內容"])
        writer.writerows(csvRows)

if __name__ == "__main__":
    while True:
        main() 
        time.sleep(60*30)