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
    #password = getpass()

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
                                                   "NocheTriste11021",
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

        with open("scraping.txt", "w") as scrapTxt:

            FileWrite = scrapTxt.write
            title = response.xpath(f"//h1[@class='gap']/text()").get()
            general = response.xpath(f"//div[@id='project-description']/ul[3]").get()
            general = general.replace("<li>","\t<li>").replace("ul>", "ol>")
            resources = response.xpath(f"//div[@id='project-description']/ul[1]").get()
            resources = resources.replace("<li>", "\t<li>").replace("ul>", "ol>")
            FileWrite(f"# {title}\n\n")
            FileWrite(f"## GENERAL:\n\n {general}\n\n")
            FileWrite(f"## RESOURCES:\n\n {resources}\n\n")
            FileWrite("## INTRODUCTION TO FILES:\n\n")
            count = 0

            for j in range(0, 100):

                numberOfTask =  response.xpath(f"//div[@id='task-num-{j}']/@data-role").extract_first()

                if(not numberOfTask):
                    break

                if (numberOfTask):

                    idTask =  int((re.findall(r'\d+', numberOfTask))[0])
                    checkIfIDid = response.xpath(f"//button[@data-task-id={idTask}]/@class").extract_first()

                else:
                    break

                if checkIfIDid.find("yes") != -1:

                    nameFile =  response.xpath(f"//div[@id='task-num-{j}']/div/div/div/ul/li[3]/code/text()").get()
                    titleDesc = response.xpath(f"//div[@id='task-num-{j}']/div/div/p").getall()
                    titleDesc = "".join(titleDesc).replace("Write a","").replace("<p>","")
                    titleDesc = titleDesc.replace("Write a function","A function")
                    titleDesc = titleDesc.replace("</p>","").replace("Write an","An")

                    removingPoint = nameFile.replace(".", "")
                    FileWrite(f'{count}.\t[**{nameFile}**:](#{removingPoint}) {titleDesc}\n')
                    count = count + 1

            FileWrite("## FILES:\n\n")

            for i in range(0, 100):

                numberOfTask =  response.xpath(f"//div[@id='task-num-{i}']/@data-role").extract_first()

                if(not numberOfTask):
                    break

                if (numberOfTask):
                    idTask =  int((re.findall(r'\d+', numberOfTask))[0])
                    checkIfIDid = response.xpath(f"//button[@data-task-id={idTask}]/@class").extract_first()

                if checkIfIDid.find("yes") != -1:

                    nameFile = response.xpath(f"//div[@id='task-num-{i}']/div/div/div/ul/li[3]/code/text()").get()
                    titleDesc = response.xpath(f"//div[@id='task-num-{i}']/div/div/p").getall()
                    titleDesc = "".join(titleDesc).replace("Write a function", "Function")
                    titleDesc = titleDesc.replace("Write a ","").replace("Write an","An")
                    desc  =  response.xpath(f"//div[@id='task-num-{i}']/div/div/ul").getall()
                    example =   response.xpath(f"//div[@id='task-num-{i}']/div/div/pre").get()
                    FileWrite(f"### {nameFile}\n\n")
                    FileWrite(f"*{titleDesc}*\n\n")
                    if desc:
                        desc = "\n".join(desc).replace("<li>", "\t<li>")
                        desc = desc.replace("\n\t<li>You are not allowed to import any module</li>", "")
                        desc = desc.replace("You must use","Must")
                        desc = desc.replace("You are","It is").replace("Your ","")
                        desc = desc.replace("Write a ","")
                        FileWrite(f"{desc}\n\n")
                    FileWrite(f"{example}\n\n")
