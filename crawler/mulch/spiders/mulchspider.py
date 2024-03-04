import scrapy
from scrapy.linkextractors import LinkExtractor
from mulch.items import MulchItem
import re
import csv
import logging


class MulchSpider(scrapy.Spider):
    name = "mulch"
    urls = ["https://twitter.com/MARIMARI_EN/status/1726121501789999289"]
    count = 0
    link_extractor = LinkExtractor()
    explored_links = []
    keyword = "mulch"
    #implement visited links
    #sql for scraped link shou;ld be implemented here



    def start_requests(self, *args):
        logging.warning("start request called with args: " + str(args))
        logging.warning("frontier length: " + str(len(self.urls)))
        url = self.urls[0]

        #if url not in self.explored_links:
        yield scrapy.Request(url=url, callback=self.parse, errback = self.start_requests, dont_filter=True)
        logging.warning("start request: " + url)
        self.count += 1

        self.urls = self.urls[1:] 

        

    def parse(self, response):
        logging.warning(f"parsing: {response.url}")

        texts = response.xpath("//div/text()").getall()
        links = self.link_extractor.extract_links(response)

        #record content of current node
        texts = MulchSpider.cleanString(texts)
        texts = filter(lambda text: self.keyword in text, texts)  #define how to filter text
        for text in texts:
            item = MulchItem()
            item["url"] = response.url
            item["text"] = text
            item["keywords"] = self.keyword
            #logging.warning(f"yielding item {item['url']}") 
            yield item



        #explore current node
        for link in links:
            if link.url not in self.urls:
                self.urls.append(link.url)  
        self.explored_links.append(self.urls[0])


        #yield next request
        if (len(self.urls) > 0):
            yield from self.start_requests() #so this is never called?




    #param: a list of strings
    #output: same list of string, normalized. 
    @classmethod
    def cleanString(cls, strings):
        #format string properly
        
        #remove all extra line breaks, special characters, lowercase all
        new_strings = []
        for string in strings:
            string = string.replace('\n', ' ')
            string = re.sub(r"\W+|_", " ", string) 
            string = string.lower()
            if any(character.isalnum() for character in string): #if string contain alphanumericals
                new_strings.append(string)

        return new_strings
    





    @classmethod
    def writeCSV(cls, list):
        with open('CSVtest.csv', 'w', encoding="utf-8") as CSVtest:
            wr = csv.writer(CSVtest, quoting=csv.QUOTE_NONE)
            wr.writerow(list)


    #returns list
    #WORKS
    @classmethod
    def readCSV(cls, filepath):
        list = []
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                list.extend(row)

        return list