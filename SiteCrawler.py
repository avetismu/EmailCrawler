import httplib

class Crawler:


    def __init__(self):
        pass


    def getHTML(self, domain, page):

        #establish HTTPS connection to web address
        conn = httplib.HTTPConnection(domain)
        conn.request("GET", page)
        res = conn.getresponse()
        print res.status
        HTML = res.read();
        print HTML


crawler = Crawler()
crawler.getHTML("www.tricklecreekhomes.ca", "/")
