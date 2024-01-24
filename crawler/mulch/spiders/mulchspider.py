import scrapy
from scrapy.linkextractors import LinkExtractor

class MulchSpider(scrapy.Spider):
    name = "mulch"
    urls = []
    link_extractor = LinkExtractor()

    def start_requests(self):
        self.urls.append("https://www.bloodborne-wiki.com/2017/12/dialogue-reference.html") #starting url

        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        texts = response.xpath("//li/text()")
        links = self.link_extractor.extract_links(response)
        text_out = ""
        links_out = ""




        #define how to output the text
        for text in texts.getall():
            if "mushy" in text:
                text_out = text_out + text + "\n"

        f = open("output.txt", "w")
        f.write(text_out)


    #output links
        for link in links:
            links_out = links_out + link.url + "\n"

        g = open("linksoutput.txt", "w")
        g.write(links_out)
