# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import logging


class MulchPipeline:
    #logging.basicConfig(encoding='utf-8', level=logging.INFO)
    log = ""

    def open_spider(self, spider):
        logging.warning("spider opened")

        self.connection = mysql.connector.connect(
            user = "rainer",
            password = "13667090887Awa.",
            database = "rainer"
        )
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS mulch(
                            id int NOT NULL auto_increment,
                            url TEXT,
                            text TEXT,
                            keywords SET("mulch"),
                            PRIMARY KEY (id)
            )""")
        
    def close_spider(self):
        self.cursor.close()
        self.connection.close()

        logging.info("spider closed")

        f = open("output.txt", "w", encoding="utf-8")
        f.write(self.log)



    def process_item(self, item, spider):

        logging.warning(f"""processing item: \n  
                        INSERT INTO mulch(url,text,keywords) VALUES( \n 
                        {item["url"]}, \n 
                        {item["text"]}, \n 
                        {item["keywords"]})""")



        self.cursor.execute(f"""INSERT INTO mulch(url,text,keywords) VALUES( \n 
                        {item["url"]}, \n 
                        {item["text"]}, \n 
                        {item["keywords"]});""")
        self.connection.commit()

        return item
