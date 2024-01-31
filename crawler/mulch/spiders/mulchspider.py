import scrapy
from scrapy.linkextractors import LinkExtractor

class MulchSpider(scrapy.Spider):
    name = "mulch"
    urls = ["https://www.bloodborne-wiki.com/p/story.html",
            "http://www.bloodborne-wiki.com/p/index.html"]
    count = 0
    link_extractor = LinkExtractor()
    log = "" #tesing purposes


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
        text_out = ""
        links_out = ""


        



        #define how to output the text
        # why isnt this working
        #ITS WORKING
        text_out = "".join(texts)
        f = open("output.txt", "w", encoding="utf-8")
        f.write(text_out)


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
        else:
            self.urls = self.urls[1:]
            self.log = self.log + "removing:" + self.urls[0] + "\n\n" ##

            #hault operation after scraping a given number of sites
            if self.count > 5:
                return
            yield scrapy.Request(url=self.urls[0], callback=self.parse)
            self.log = self.log + "test yielding request: " + self.urls[0] + "\n"
            self.count = self.count + 1
            self.log = self.log + "count: " + str(self.count) + "\n"
        





        g = open("log.txt", "w")
        g.write(self.log)

