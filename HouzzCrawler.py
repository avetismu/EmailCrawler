import httplib
from HTMLParser import HTMLParser
import threading
import json
import SiteCrawler



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

        try:
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
                return None
        except:
            print 'Connection Failed'
            print "Unexpected error:", sys.exc_info()[0]
            return 0

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
            try:
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
            except:
                print 'Connection Failed to'
                print "Unexpected error:", sys.exc_info()[0]


    def handle_starttag(self, tag, attrs):
        for i in range(0, len(attrs)):
            if (attrs[i][0] == 'compid' and attrs[i][1] == 'Profile_Website'):
                for j in range(0, len(attrs)):
                    if(attrs[j][0] == 'href'):
                        lock.acquire()

                        sites.append(attrs[j][1])
                        lock.release()
                        break
                break


def parse(page_num):
    houzz_crawler = HouzzCrawler(page_num)
    houzz_crawler.Crawl()

    profile_crawler = ProfileCrawler(houzz_crawler.list_of_pros)
    profile_crawler.Crawl()


def thread_spawn(iteration):
    still_active = False
    if(iteration > TIME_OUT):
        print '\n\n\n Timeout Error \n\n\n'
        return 0

    for t in threads:
        if t.isAlive():
            still_active = True

    if still_active:
        print '\n\n\n Indexing Directory... \n\n\n'

        threading.Timer(10.0, thread_spawn, (iteration+1,)).start()
    else:
        total_websites = len(sites)
        print 'Total Websites: ' + str(total_websites)
        json.dump(sites, f)
        f.close()
        print '\n\n\n Indexing Completed \n\n\n'
        SiteCrawler.thread_spawn(0, total_websites)
        SiteCrawler.thread_manager()
        return 0



#BEGIN
print 'Welcome to HouzzCrawler'

start_page = raw_input('At which page should I start crawling? ')
total_pages = raw_input('How many pages should I crawl? ')
total_websites = 0

#Global
lock = threading.Lock()
MAX_THREADS = 40
TIME_OUT = 8
f = open('architecture_websites.json', 'w')
sites = []
threads = []



for i in range (int(start_page), int(total_pages)):
    thread_name = 'thread ' + str(i)
    t = threading.Thread(target=parse, name = thread_name, args=(i, ))
    threads.append(t)
    t.start()

thread_spawn(0)
