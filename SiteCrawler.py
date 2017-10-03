import httplib
import sys
import ssl
import socket
from HTMLParser import HTMLParser


class PageCrawler(HTMLParser):

    #constructor
    def __init__(self, domain):
        HTMLParser.__init__(self)
        self.domain = domain[4:]
        self.domain_len = len(self.domain)
        self.emails = []
        self.new_pages = []

    def handle_starttag(self, tag, attrs):
        for i in range(0, len(attrs)):
            if (attrs[i][0] == 'href'):
                if("mailto" in attrs[i][1]):
                    if(attrs[i][1][7:] not in self.emails):
                        self.emails.append(attrs[i][1][7:])
                elif(self.domain in attrs[i][1]):
                    index = attrs[i][1].find(self.domain) + self.domain_len
                    if (attrs[i][1][index:] not in self.new_pages) and ("jpg" not in attrs[i][1]) and ("png" not in attrs[i][1]) and ("css" not in attrs[i][1]) and ("xml" not in attrs[i][1]) and ("pdf" not in attrs[i][1]):
                        self.new_pages.append(attrs[i][1][index:])
                elif(attrs[i][1].startswith("/")):
                    if (attrs[i][1] not in self.new_pages) and ("jpg" not in attrs[i][1]) and ("png" not in attrs[i][1]) and ("css" not in attrs[i][1]):
                        self.new_pages.append(attrs[i][1])


class SiteCrawler():


    def __init__(self, domain):
        self.visited = []
        self.todo = []
        self.emails = []
        self.domain = domain
        self.f = open('crawl_log.txt', 'w')


    def SanitiseDomain(self):
        if("www." in self.domain):
            self.domain = self.domain[7:]
        else:
            self.domain = "www." + self.domain[7:]

        if(self.domain[len(self.domain)-1] == "/"):
            self.domain = self.domain[0:(len(self.domain)-1)]

        print self.domain


    def Crawl(self, page):

        if(page in self.visited):

            print 'Already crawled ' + self.domain + page + ' DISCARDING PAGE!'
            if len(self.todo) == 0:
                return 0
            else:
                self.Crawl(self.todo.pop(0))
        else:
            self.visited.append(page)
            try:
                conn = httplib.HTTPConnection(self.domain, timeout=2)
                conn.request("GET", page)
                res = conn.getresponse()
                if(res.status == 200):
                    print "Connection Successful to " + self.domain + page
                    HTML = res.read();
                    page_crawler = PageCrawler(self.domain);
                    page_crawler.feed(HTML)
                    if(page_crawler.emails not in self.emails):
                        self.emails.extend(page_crawler.emails)
                    #print page_crawler.emails
                    self.todo.extend(page_crawler.new_pages)
                    #print page_crawler.new_pages
                else:
                    print res.status
                    print res.read()
                    print 'Connection Failed to ' + self.domain + page
                    if(len(self.todo) == 0):
                        return 0
                    else:
                        self.Crawl(self.todo.pop(0))
            except:
                print 'Connection Failed to ' + self.domain + page
                print "Unexpected error:", sys.exc_info()[0]
                if(len(self.todo) == 0):
                    return 0
                else:
                    self.Crawl(self.todo.pop(0))

        if(len(self.todo) == 0):
            return 0
        else:
            self.f.write(str(self.visited))
            self.f.write('+++++++++++++++++++++++++++++++++')
            self.f.write('\n \n \n')
            self.f.write(str(self.todo))
            print self.visited
            print '+++++++++++++++++++++++++++++++++'
            print self.todo
            print '''



            '''
            self.Crawl(self.todo.pop(0))


print socket.ssl
cxt = ssl._create_unverified_context()
crawler = SiteCrawler("http://www.tricklecreekhomes.ca/")
crawler.SanitiseDomain()
crawler.Crawl("/")
self.f.close()
print crawler.emails
