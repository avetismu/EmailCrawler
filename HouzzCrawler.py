import httplib
from HTMLParser import HTMLParser
from threading import *

class HouzzCrawler(HTMLParser):

    #constructor
    def __init__(self, page_num):
        HTMLParser.__init__(self)
        self.current_p = page_num
        self.http_address = "www.houzz.com"
        self.list_of_pros = []

    def Crawl(self):

        if (self.current_p == 0):
            page = "/professionals/architect/"
        else:
            page = "/professionals/architect/p/" + str(15*self.current_p)

        print "Crawling " + self.http_address + page

        #establish HTTPS connection to web address
        conn = httplib.HTTPSConnection(self.http_address)
        conn.request("GET", page)
        res = conn.getresponse()
        if( res.status ):
            print 'Connection Successful'
            HTML = res.read();
            conn.close()
            self.feed(HTML);
        else:
            print res.status
            print 'Connection Error'

        print 'List of Pros on Page ' + str(self.current_p)
        print self.list_of_pros


    def handle_starttag(self, tag, attrs):
        for i in range(0, len(attrs)):
            if (attrs[i][0] == 'itemprop' and attrs[i][1] == 'name'):
                for j in range(0, len(attrs)):
                    if(attrs[j][0] == 'href'):
                        self.list_of_pros.append(attrs[j][1][21:])

class ProfileCrawler(HTMLParser):

    #constructor
    def __init__(self, list_of_pros):
        HTMLParser.__init__(self)
        self.current_p = 0
        self.http_address = "www.houzz.com"
        self.list_of_pros = list_of_pros
        self.list_of_websites = []

    def Crawl(self):

        for i in range(0, len(self.list_of_pros)):

            page = self.list_of_pros[i]


            #print "Crawling " + self.http_address + page

            #establish HTTPS connection to web address
            conn = httplib.HTTPSConnection(self.http_address)
            conn.request("GET", page)
            res = conn.getresponse()
            if( res.status ):
                HTML = res.read();
                conn.close()
                self.feed(HTML);
            else:
                print res.status
                print 'Connection Error'


    def handle_starttag(self, tag, attrs):
        for i in range(0, len(attrs)):
            if (attrs[i][0] == 'compid' and attrs[i][1] == 'Profile_Website'):
                for j in range(0, len(attrs)):
                    if(attrs[j][0] == 'href'):
                        lock.acquire()
                        f.write(attrs[j][1] + '\n')
                        lock.release()
                        break
                break


def parse(page_num):
    houzz_crawler = HouzzCrawler(page_num)
    houzz_crawler.Crawl()

    profile_crawler = ProfileCrawler(houzz_crawler.list_of_pros)
    profile_crawler.Crawl()


#BEGIN
print 'Welcome to HouzzCrawler'

total_pages = raw_input('How many pages should I crawl')

#Global
lock = Lock()
f = open('architecture_websites.txt', 'a')

if __name__ == '__main__':
    for i in range (0, total):
        thread_name = 'thread ' + str(i)
        t = Thread(target=parse, name = thread_name, args=(i, ))
        t.start()
