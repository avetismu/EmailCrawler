import httplib
from HTMLParser import HTMLParser

class HouzzCrawler(HTMLParser):

    #constructor
    def __init__(self):
        HTMLParser.__init__(self)
        self.current_p = 0
        self.http_address = "www.houzz.com"

    def getPageHTML(self):

        if (self.current_p == 0):
            page = "/professionals/architect/"
        else:
            page = "/professionals/architect/" + 15*self.current_p

        print "Crawling " + self.http_address + page

        #establish HTTPS connection to web address
        conn = httplib.HTTPSConnection(self.http_address)
        conn.request("GET", page)
        res = conn.getresponse()
        print res.status
        
        HTML = res.read();
        print HTML

        self.feed(HTML);

    def handle_starttag(self, tag, attrs):
        print "Encountered an attribute:", attrs

    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        pass

    def handle_data(self, data):
        #print "Encountered some data  :", data
        pass

parser = HouzzCrawler()
parser.getPageHTML()
