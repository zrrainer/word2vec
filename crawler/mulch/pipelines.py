# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import csv


class MulchPipeline:
    log = ""

    def open_spider(self, spider):
        self.log = ""
        self.log = self.log + "spider opened \n"
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

        self.log = self.log + "spider closed \n"

        f = open("output.txt", "w", encoding="utf-8")
        f.write(self.log)





    def process_item(self, item, spider):
        self.log = self.log + """processing item: \n
    
            INSERT INTO TABLE mulch(url,text,keywords) VALUES(\n
                \"""" + item["url"] + """\",\n
                \"""" + item["text"] + """\",\n
                \"""" + item["keywords"] + """\"\n\n
            )"""
        f = open("output.txt", "w", encoding="utf-8")
        f.write(self.log)



        self.cursor.execute("""
            INSERT INTO TABLE mulch(url,text,keywords) VALUES(\n
                \"""" + item["url"] + """\",\n
                \"""" + item["text"] + """\",\n
                \"""" + item["keywords"] + """\"\n\n
            )""")
        self.connection.commit()

        return item
