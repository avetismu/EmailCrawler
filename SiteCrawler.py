import httplib
import sys
import ssl
import json
import socket
import threading
import urllib2
import re
import CSVCleaner
from random import randint
from HTMLParser import HTMLParser


class PageCrawler(HTMLParser):

    #constructor
    def __init__(self, domain):
        HTMLParser.__init__(self)
        self.domain = domain[4:]
        self.domain_len = len(self.domain)
        self.emails = []
        self.new_pages = []
        self.latest_tag = 'html'

    def handle_starttag(self, tag, attrs):
        self.latest_tag = tag
        for i in range(0, len(attrs)):
            if (attrs[i][0] == 'href'):
                #print attrs[i][1]
                if("mailto" in attrs[i][1]):
                    if(attrs[i][1][7:] not in self.emails):
                        write_lock.acquire()
                        f_write.write(attrs[i][1][7:] + ',\n')
                        write_lock.release()
                        self.emails.append(attrs[i][1][7:])
                        return 0
                elif(self.domain in attrs[i][1]):
                    index = attrs[i][1].find(self.domain) + self.domain_len
                    if (attrs[i][1][index:] not in self.new_pages) and ("jpg" not in attrs[i][1]) and ("png" not in attrs[i][1]) and ("css" not in attrs[i][1]) and ("xml" not in attrs[i][1]) and ("pdf" not in attrs[i][1]):
                        if( 'contact' in attrs[i][1] or 'about' in attrs[i][1]):
                            self.new_pages.insert(0, attrs[i][1][index:])
                        else:
                            self.new_pages.append(attrs[i][1][index:])
                elif(attrs[i][1].startswith("/")):
                    if (attrs[i][1] not in self.new_pages) and ("jpg" not in attrs[i][1]) and ("png" not in attrs[i][1]) and ("css" not in attrs[i][1]):
                        if( 'contact' in attrs[i][1] or 'about' in attrs[i][1]):
                            self.new_pages.insert(0, attrs[i][1])
                        else:
                            self.new_pages.append(attrs[i][1])

    def handle_data(self, data):
        if(self.latest_tag != 'span' or self.latest_tag != 'p'):
            pass
        else:
            print '\n checking regex against: \n' + data + '\n\n'
            email = regex.match(data)
            if (email != None):
                write_lock.acquire()
                f_write.write(email)
                write_lock.release()


class SiteCrawler():


    def __init__(self, domain):
        self.visited = []
        self.todo = []
        self.emails = []
        self.domain = domain


    def SanitiseDomain(self):
        if("www." in self.domain):
            self.domain = self.domain[7:]
        else:
            self.domain = "www." + self.domain[7:]

        if(self.domain[len(self.domain)-1] == "/"):
            self.domain = self.domain[0:(len(self.domain)-1)]

        print self.domain


    def QuickCrawl(self, page):
        try:
            request = urllib2.Request('https://' + self.domain + page, headers=request_headers)
            response = urllib2.urlopen(request, context=cxt, timeout=2)
            if(response.getcode() == 200):
                print "HTTPS Connection Successful to " + self.domain + page
                HTML = response.read().decode('utf-8')
                page_crawler = PageCrawler(self.domain)
                page_crawler.feed(HTML)
                if(page_crawler.emails not in self.emails):
                    self.emails.extend(page_crawler.emails)
                #print page_crawler.emails
                self.todo.extend(page_crawler.new_pages)
                #print page_crawler.new_pages
            elif(response.getcode() == 301 or res.getcode() == 303):
                print response.getcode()
                print 'Connection Failed to ' + self.domain + page
                print res.read()
            else:
                print response.getcode()
                print response.read()
                print 'HTTPS Connection Failed to ' + self.domain + page

        except ssl.SSLError:
            print sys.exc_info()[0]
            print sys.exc_info()[1]
        except urllib2.HTTPError:
            print 'HTTPS Connection Failed to ' + self.domain + page
            print "Unexpected error:", sys.exc_info()[0]
            print sys.exc_info()[1]
        except:
            print 'HTTPS Connection Failed to ' + self.domain + page
            print "Unexpected error:", sys.exc_info()[0]
            print sys.exc_info()[1]

    def HTTPQuickCrawl(self, page):
            try:
                conn = httplib.HTTPConnection(self.domain, timeout=2)
                conn.request("GET", page)
                res = conn.getresponse()

                if(res.status == 200):
                    print res.status
                    print "Connection Successful to " + self.domain + page
                    HTML = res.read();
                    page_crawler = PageCrawler(self.domain);
                    page_crawler.feed(HTML)
                    write_lock.acquire()
                    #f_write.write(self.domain + page + '\n' + HTML + '\n\n\n')
                    write_lock.release()
                    if(page_crawler.emails not in self.emails):
                        self.emails.extend(page_crawler.emails)
                        return 0
                    #print page_crawler.emails
                    self.todo.extend(page_crawler.new_pages)
                    #print page_crawler.new_pages
                elif(res.status == 301 or res.status == 303):
                    print res.status
                    print 'Connection Failed to ' + self.domain + page
                    self.QuickCrawl(page)
                else:
                    print res.status
                    print res.read()
                    print 'Connection Failed to ' + self.domain + page
                    self.QuickCrawl(page)
            except TypeError:
                print sys.exc_info()[0]
                print sys.exc_info()[1]
            except:
                print 'Connection Failed to ' + self.domain + page
                print "Unexpected error:", sys.exc_info()[0]

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
                request = urllib2.Request('https://' + self.domain + page, headers=request_headers)
                response = urllib2.urlopen(request, context=cxt, timeout=2)
                if(response.getcode() == 200):
                    print "HTTPS Connection Successful to " + self.domain + page
                    HTML = response.read()
                    page_crawler = PageCrawler(self.domain);
                    page_crawler.feed(HTML)
                    if(page_crawler.emails not in self.emails):
                        self.emails.extend(page_crawler.emails)
                    #print page_crawler.emails
                    self.todo.extend(page_crawler.new_pages)
                    #print page_crawler.new_pages
                elif(response.getcode() == 301 or res.getcode() == 303):
                    print response.getcode()
                    print 'Connection Failed to ' + self.domain + page
                    print res.read()
                    self.RedirectedCrawl(page)
                else:
                    print response.getcode()
                    print response.read()
                    print 'HTTPS Connection Failed to ' + self.domain + page
                    if(len(self.todo) == 0):
                        return 0
                    else:
                        self.Crawl(self.todo.pop(0))

            except ssl.SSLError:
                print sys.exc_info()[0]
                print sys.exc_info()[1]
            except urllib2.HTTPError:
                print 'HTTPS Connection Failed to ' + self.domain + page
                print "Unexpected error:", sys.exc_info()[0]
                print sys.exc_info()[1]
                if(len(self.todo) == 0):
                    return 0
                else:
                    self.Crawl(self.todo.pop(0))
            except:
                print 'HTTPS Connection Failed to ' + self.domain + page
                print "Unexpected error:", sys.exc_info()[0]
                print sys.exc_info()[1]

        if(len(self.todo) == 0 or len(self.visited) > 10):
            return 0
        else:
            print self.visited
            print '+++++++++++++++++++++++++++++++++'
            print self.todo
            print '''



            '''
            self.Crawl(self.todo.pop(0))

    def CrawlHTTPS(self, page):
        if(page in self.visited):

            print 'Already crawled ' + self.domain + page + ' DISCARDING PAGE!'
            if len(self.todo) == 0:
                print self.emails
            else:
                self.Crawl(self.todo.pop(0))
        else:
            self.visited.append(page)
            try:
                conn = httplib.HTTPSConnection(self.domain, timeout=5, context=cxt)
                conn.request("GET", page)
                res = conn.getresponse()
                if(res.status == 200):
                    print "HTTPS Connection Successful to " + self.domain + page
                    HTML = res.read();
                    page_crawler = PageCrawler(self.domain);
                    page_crawler.feed(HTML)
                    if(page_crawler.emails not in self.emails):
                        self.emails.extend(page_crawler.emails)
                    #print page_crawler.emails
                    self.todo.extend(page_crawler.new_pages)
                    #print page_crawler.new_pages
                elif(res.status == 301 or res.status == 303):
                    print res.status
                    print 'Connection Failed to ' + self.domain + page
                    print res.read()
                    self.RedirectedCrawl(page)
                else:
                    print res.status
                    print res.read()
                    print 'HTTPS Connection Failed to ' + self.domain + page
                    if(len(self.todo) == 0):
                        print self.emails
                    else:
                        self.Crawl(self.todo.pop(0))
            except ssl.SSLError:
                print sys.exc_info()[0]
                print sys.exc_info()[1]
            except:
                print 'HTTPS Connection Failed to ' + self.domain + page
                print "Unexpected error:", sys.exc_info()[0]
                if(len(self.todo) == 0):
                    print self.emails
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


    def HTTPCrawl(self, page):

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
                    print res.status
                    print "Connection Successful to " + self.domain + page
                    HTML = res.read();
                    page_crawler = PageCrawler(self.domain);
                    page_crawler.feed(HTML)
                    write_lock.acquire()
                    #f_write.write(self.domain + page + '\n' + HTML + '\n\n\n')
                    write_lock.release()
                    if(page_crawler.emails not in self.emails):
                        self.emails.extend(page_crawler.emails)
                        print self.emails
                        return 0
                    #print page_crawler.emails
                    self.todo.extend(page_crawler.new_pages)
                    #print page_crawler.new_pages
                elif(res.status == 301 or res.status == 303):
                    print res.status
                    print 'Connection Failed to ' + self.domain + page
                    self.visited = []
                    self.Crawl(page)
                else:
                    print res.status
                    print res.read()
                    print 'Connection Failed to ' + self.domain + page
                    if(len(self.todo) == 0):
                        return 0
                    else:
                        self.Crawl(self.todo.pop(0))
            except TypeError:
                print sys.exc_info()[0]
                print sys.exc_info()[1]
            except:
                print 'Connection Failed to ' + self.domain + page
                print "Unexpected error:", sys.exc_info()[0]
                self.CrawlHTTPS(page)
                if(len(self.todo) == 0):
                    return 0
                else:
                    self.Crawl(self.todo.pop(0))

        if(len(self.todo) == 0 or len(self.visited) > 10):
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
            self.HTTPCrawl(self.todo.pop(0))

def parse(entry):

    read_lock.acquire()

    with open('architecture_websites.json', 'r') as f_read:
        try:
            website = json.load(f_read)[entry]
        except IndexError:
            print sys.exc_info()[0]
            print sys.exc_info()[1]
            print 'Index Error at Index ' + str(entry)
            return 0
    print website

    crawler = SiteCrawler(website)
    read_lock.release()
    crawler.SanitiseDomain()
    crawler.Crawl("/")

def starter(set, max_length):

    for i in range (50*set, 50*set + max_length):
        parse(i)



def thread_manager():
    still_active = False
    for t in threads:
        if t.isAlive():
            still_active = True

    if still_active:
        print '\n\n\n Crawling Websites... \n\n\n'

        threading.Timer(10.0, thread_manager).start()
    else:
        f_write.close()
        CSVCleaner.Clean()

def thread_spawn(entry, total_threads):
    print 'Site Crawler Started'
    total = total_threads / 50
    max_length = 50
    if total == 0:
        total = 1
        max_length = total_threads


    print 'Starting ' + str(total) + ' threads'
    for i  in range (0, total):
        thread_name = 'thread ' + str(i)
        t = threading.Thread(target=starter, name = thread_name, args=(i, max_length))
        threads.append(t)
        t.start()


#GLOBAL

cxt = ssl._create_unverified_context()

read_lock = threading.Lock()
write_lock = threading.Lock()

threads = []

sys.setrecursionlimit(1500)

request_headers = {
"Accept-Language": "en-US,en;q=0.5",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Referer": "http://thewebsite.com",
"Connection": "keep-alive"
}

pattern = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
regex = re.compile(pattern)

f_write =open('email_mine.csv', 'w')
f_write.write('Emails,\n')
#MAX_THREADS = 1




if __name__ == "__main__":
    total_websites = raw_input('How many websites should I crawl? ')
    for i in range(0, int(total_websites)):
        parse(i)
