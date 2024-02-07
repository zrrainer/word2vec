import scrapy
from scrapy.linkextractors import LinkExtractor
import re

class MulchSpider(scrapy.Spider):
    name = "mulch"
    urls = ["https://www.bloodborne-wiki.com/p/story.html",
            "https://www.bloodborne-wiki.com/p/firearms.html"]
    count = 0
    link_extractor = LinkExtractor()
    text_out = ""
    #implement visited links



    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)    
 

    def parse(self, response):
        texts = response.xpath("//body//text()").getall()
        links = self.link_extractor.extract_links(response)
        links_out = ""


        #record content of current node
        texts = MulchSpider.cleanString(texts)
        #texts = filter(lambda text: "vergil" in text, texts)  #define how to filter text
        self.text_out = self.text_out + "\n".join(texts)

        #search algortithm
        explored_links = []

        #explore current node
        for link in links:
            if link.url not in self.urls:
                self.urls.append(link.url)  
        explored_links.append(self.urls[0])


            
        if (len(self.urls) > 0 and self.count < 10):
            self.text_out = self.text_out + "\n\n\n ----------------------------------------\nif condition met"
            self.start_requests() #debugging.................
            # self.urls = self.urls[1:]
            # self.count = self.count + 1
            # yield scrapy.Request(url=self.urls[0], callback=self.parse)

        f = open("output.txt", "w", encoding="utf-8")
        f.write(self.text_out)




    #param: a list of strings
    #output: same list of string, normalized. 
    @classmethod
    def cleanString(cls, strings):
        #format string properly
        
        #remove all \n, special characters, lowercase all
        new_strings = []
        for string in strings:

            string = string.replace('\n', ' ')
            string = re.sub(r"\W+|_", " ", string) 
            string = string.lower()
            if any(character.isalnum() for character in string): #if string contain alphanumericals
                new_strings.append(string)

        return new_strings
    

    #def yield request
        #remove current node
        #yielf request 
        #count ++
    def yieldRequest(self):
        self.urls = self.urls[1:]
        self.count = self.count + 1
        yield scrapy.Request(url=self.urls[0], callback=self.parse) #this is the problem everything else is reached