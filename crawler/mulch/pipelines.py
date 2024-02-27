# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import logging


class MulchPipeline:
    logging.basicConfig(filename = "logging.txt", encoding='utf-8', level=logging.INFO)
 

    def open_spider(self, spider):
        logging.warning("spider opened")
        keyword = "mulch" ##testing 


        #open connection
        self.connection = mysql.connector.connect(
            user = "rainer",
            password = "13667090887Awa.",
            database = "rainer"
        )
        self.cursor = self.connection.cursor()


        #ckear table
        self.cursor.execute("DROP TABLE IF EXISTS mulch")
        self.cursor.execute("DROP TABLE IF EXISTS scraped_links")
        #create table if none exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS mulch(
                            id int NOT NULL auto_increment,
                            url TEXT,
                            text TEXT,
                            keywords SET("mulch"),
                            PRIMARY KEY (id)
            )""")
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scraped_links(
                            link VARCHAR(300), 
                            UNIQUE(link)
            )""") ##varchar key length max 3000 byte???
        
    def close_spider(self,*args):

        logging.warning("closing spider %s, %s"%(self, args)) 
        self.cursor.close()
        self.connection.close()

        logging.info("spider closed")



    def process_item(self, item, spider):

        logging.warning("""INSERT INTO mulch (url, text, keywords) VALUES (\"%s\", \"%s\", \"%s\");""" %(item["url"], item["text"], item["keywords"]))

        self.cursor.execute("""INSERT INTO mulch (url, text, keywords) VALUES (\"%s\", \"%s\", \"%s\");""" %(item["url"], item["text"], item["keywords"]))
        self.cursor.execute("""INSERT INTO scraped_links VALUES(\"%s\");""" %(item["url"]))
        self.connection.commit()

        return item
