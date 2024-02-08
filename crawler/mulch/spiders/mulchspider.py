import scrapy
from scrapy.linkextractors import LinkExtractor
import re
import csv

class MulchSpider(scrapy.Spider):
    name = "mulch"
    urls = ["https://www.bloodborne-wiki.com/p/story.html",
            "https://www.bloodborne-wiki.com/p/firearms.html"]
    count = 0
    link_extractor = LinkExtractor()
    explored_links = []
    text_out = ""
    #implement visited links



    def start_requests(self):
        url = self.urls[0]

        if url not in self.explored_links:
            yield scrapy.Request(url=url, callback=self.parse)
            self.count += 1

        self.urls = self.urls[1:] 


    def parse(self, response):
        texts = response.xpath("//body//text()").getall()
        links = self.link_extractor.extract_links(response)

        #record content of current node
        texts = MulchSpider.cleanString(texts)
        #texts = filter(lambda text: "vergil" in text, texts)  #define how to filter text
        self.text_out = self.text_out + "\n".join(texts)

        #explore current node
        for link in links:
            if link.url not in self.urls:
                self.urls.append(link.url)  
        self.explored_links.append(self.urls[0])

        #next node
        while (len(self.urls) > 0 and self.count < 10):
            yield from self.start_requests() 

        #writing output
        f = open("output.txt", "w", encoding="utf-8")
        f.write(self.text_out)

        self.writeCSV(self.explored_links)




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
    @classmethod
    def readCSV(cls, filepath):
        list = []
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                list.append(row)

        return list