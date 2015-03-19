import sqlite3
import urllib2
import re
from bs4 import BeautifulSoup as bs4

class GeeksforGeeks:

    def __init__(self, url):
        self.url = url
        self.cx = sqlite3.connect("geeksforgeeks.db")

    def parseCurrentUrl(self):
        response = urllib2.urlopen(self.url).read()
        soup = bs4(response)
        page_content = soup.find("div", class_ = "page-content").encode("utf-8")
        soup = bs4(page_content)
        paragrphs = soup.find_all("p")
        for p in paragrphs:
            if p.strong is not None:
                subject = p.strong.text.strip()
                if subject == "Misc:":
                    break
                soup = bs4(unicode(p))
                links = soup.find_all("a")
                urls = []
                cu = self.cx.cursor()
                for link in links:
                    sql = "INSERT INTO URLS VALUES (NULL, '%s', '%s')" % (subject, link["href"])
                    cu.execute(sql)

        self.cx.commit()

geek = GeeksforGeeks("http://www.geeksforgeeks.org/fundamentals-of-algorithms/")
geek.parseCurrentUrl()
