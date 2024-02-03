import scrapy
from scrapy.linkextractors import LinkExtractor
import re

class MulchSpider(scrapy.Spider):
    name = "mulch"
    urls = ["https://www.bloodborne-wiki.com/p/story.html"]
    count = 0
    link_extractor = LinkExtractor()
    log = "" #tesing purposes
    text_out = ""



    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
            self.count = self.count =+ 1
            self.log = self.log + "start request: " + url + "\n count: " + str(self.count) + "\n"

            if self.count > 5:
                break


    def parse(self, response):
        texts = response.xpath("//body//text()").getall()
        links = self.link_extractor.extract_links(response)
        links_out = ""


        



        #record content ofcurrent node


        #define how to filter text
        texts = MulchSpider.cleanstring(texts)
        texts = filter(lambda text: "maintenance" not in text, texts)
        self.text_out = self.text_out + "\n".join(texts)

        
    


        #search algortithm
        explored_links = []

        #explore current node
        explored_links.append(self.urls[0])
        self.log = self.log + "exploring:" + self.urls[0] + "\n\n" ##

        for link in links:
            if link.url not in self.urls:
                self.urls.append(link.url)  
                self.log = self.log + "found:" + link.url + "\n" ##

        #remove self 
        self.log = self.log + "frontier lengths" + str(len(self.urls)) + "\n" ##
        if len(self.urls) == 0:
            self.log = self.log + "search finished \n"
            f = open("output.txt", "w", encoding="utf-8")
            f.write(self.text_out)
        else:
            self.urls = self.urls[1:]
            self.log = self.log + "removing:" + self.urls[0] + "\n\n" ##

            #hault operation after scraping a given number of sites
            if self.count > 10:
                f = open("output.txt", "w", encoding="utf-8")
                f.write(self.text_out)
                return
            yield scrapy.Request(url=self.urls[0], callback=self.parse)
            self.log = self.log + "test yielding request: " + self.urls[0] + "\n"
            self.text_out = self.text_out + "----------------------------new request----------------------------\n"
            self.count = self.count + 1
            self.log = self.log + "count: " + str(self.count) + "\n"


        f = open("output.txt", "w") #this is not writing
        f.write(self.text_out)

        g = open("log.txt", "w")
        g.write(self.log)




    #param: a list of strings
    #output: same list of string, normalized. 
    @classmethod
    def cleanstring(cls, strings):
        #format string properly
        
        #remove all \n, special characters, lowercase all
        new_strings = []
        for string in strings:

            string = string.replace('\n', ' ')
            string=re.sub(r"\W+|_", " ", string) 
            string = string.lower()
            if any(character.isalnum() for character in string): #if string contain alphanumericals
                new_strings.append(string)

        return new_strings