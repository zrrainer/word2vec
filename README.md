# word2vec

the word2vec model is built in word2vec.ipynb. Inspired by a conversation with friends about internet memes, this project aims to investigate:

1. is it possible to pinpoint the semantic meaning of a made up slang word ("mulch", for example) by feeding sample usage of said word into a word2vec model and looking at its embedding? 

2. in the case of words with multiple meaning (mulch being both a. gardening material and b. internet slang), is it possible to determine which definition is intended?

-------

currently writing a web scraper using the Scrapy library. crawler/mulch/ contains the scraper, and outputs are saved in crawler/

launch the crawler with command "scrapy crawl [crawler name]" in the crawler directory. 


2024.2.26
crawler testing phase 1

- does duplicate entry into scraped_link need additional handling?
- scraping all body text with response.xpath("//body//text()") is a bit ick. sometimes it returns scripts that are way too long. 
