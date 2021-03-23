#!/usr/bin/python3
#Created By Andres Campo---GitHub: AndresSern
import scrapy
from scrapy import Spider
from scrapy.http import FormRequest
from getpass import getpass
import re

class QuotesSpider(Spider):
    """ Class to do scprapping to a page """
    name = 'quotes'
    start_urls = ["https://intranet.hbtn.io/auth/sign_in/"]
    password = getpass()

    def replaceWords(self, argument):
        pass

    def parse(self, response):
        """ Method to login a page """
        token = response.xpath('//*[@name="authenticity_token"]/@value').extract_first()
        return FormRequest.from_response(response,
                                         formdata={'authenticity_token': token,
                                                   'uf8': '✓',
                                                 'user[login]':
                                                   '2207@holbertonschool.com',
                                                   'user[password]':
                                                   self.password,
                                                   'commit':'Log in'},
                                         callback=self.scrape_210_page)
    def scrape_210_page(self, response):
        """ Method to initialize the page """
        print("Logged in")
        url = input("What Do You Want Scrapping: ")
        #url = "https://intranet.hbtn.io/projects/260"
        return scrapy.Request(url=url, callback=self.scrape_pages)

    def scrape_pages(self, response):
        """ Scraping the page with the general, read and watch and the
        exericise"""

        with open("scraping2.txt", "w") as scrapTxt:

            FileWrite = scrapTxt.write
            wordReplace = self.wordReplace
            title = response.xpath(f"//h1[@class='gap']/text()").get()
            general = wordReplace("general", response, 2)
            resources = wordReplace("resources", response, 1)
            descriptionFiles = []
            count = 0

            FileWrite(f"# {title}\n\n")
            FileWrite("## GENERAL " + ":open_book:" * 3 + f":\n\n {general}\n\n")
            FileWrite(f"## RESOURCES:\n\n {resources}\n\n")

            FileWrite("## INTRODUCTION TO FILES " + ":closed_book:" * 3 + ":\n\n")

            for j in range(0, 100):

                numberOfTask =  response.xpath(f"//div[@id='task-num-{j}']/@data-role").extract_first()

                if (numberOfTask):

                    idTask =  int((re.findall(r'\d+', numberOfTask))[0])
                    checkIfIDid = response.xpath(f"//button[@data-task-id={idTask}]/@class").extract_first()

                else:
                    break

                if checkIfIDid.find("yes") != -1:

                    dictFiles = {}

                    nameFile =  response.xpath(f"//div[@id='task-num-{j}']/div/div/div/ul/li[3]/code/text()").get()
                    titleDesc = wordReplace("titleDesc", response, j)
                    codeExample = response.xpath(f"//div[@id='task-num-{j}']/div/div/pre").get()

                    dictFiles["nameFile"] = nameFile
                    dictFiles["titleDesc"] = titleDesc
                    dictFiles["codeExample"] = codeExample
                    descriptionFiles.append(dictFiles)

                    removingPoint = nameFile.replace(".", "")
                    titleDesc = titleDesc.replace("<p>","").replace("</p>","")

                    FileWrite(f'{count}.\t[**{nameFile}**:](#{removingPoint}) {titleDesc}\n')
                    count = count + 1

            FileWrite("\n## FILES " + ":bookmark_tabs:" * 3 + ":\n\n")

            for item in descriptionFiles:
                """ Loop to write description about files with, the name of file
                    example of code, and what do the code"""
                FileWrite(f"### {item['nameFile']}\n\n")
                FileWrite(f"**{item['titleDesc']}**\n\n")
                FileWrite(f"{item['codeExample']}\n\n")

    def wordReplace(self, name, response, i):
        if name == "general" or name == "resources":
            target = response.xpath(f"//div[@id='project-description']/ul[{i}]").get()
            target = target.replace("<li>","\t<li>").replace("ul>", "ol>")
            return target
        if name == "titleDesc":

            titleDesc = response.xpath(f"//div[@id='task-num-{i}']/div/div/p").getall()
            titleDesc = "".join(titleDesc).replace("Write a function", "Function")
            titleDesc = titleDesc.replace("Write a ","").replace("Write an","An")
            titleDesc = titleDesc.replace("<strong>No test cases needed</strong>", "")
            titleDesc = titleDesc[0:3] + titleDesc[3].upper() + titleDesc[4:]
            titleDesc = titleDesc.replace(":","")
            return titleDesc
