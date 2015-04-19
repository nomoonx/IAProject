__author__ = 'noMoon'
import requests, re, urlparse
import threading
from Queue import Queue
from bs4 import BeautifulSoup
import json
import time

start=time.time()

class Page:
    def __init__(self, url):

        self.url = url
        self.status = ""
        self.rawdata = ""
        self.error = True

        r = ""

        try:
            r = requests.get(self.url, headers={'User-Agent': 'noMoon spider'})
            self.error = False
        except requests.exceptions.RequestException as e:
            self.status = e
        else:
            # self.error=True
            if not r.history:
                self.status = r.status_code
            else:
                self.status = r.history[0]
        # print '%s status: %s' % (self.url,self.status)
        # if self.status is '200':
        # self.error=False
        # print r.headers['content-type']
        self.rawdata = r
        # print r

    def outlinks(self):
        # print "hoho"
        self.outlinks = []

        # links, contains URL, anchor text, nofollow
        raw = self.rawdata.text.lower()
        # print 1
        # print raw
        soup = BeautifulSoup(raw, 'html.parser')
        # print 2
        outlinks = soup.find_all('a', href=True)
        # print 'out link length %s' % len(outlinks)
        # print outlinks
        for link in outlinks:
            d = {"follow": "yes"}
            d['url'] = urlparse.urljoin(self.url, link.get('href'))
            # print d['url']
            d['anchortext'] = link.text
            if link.get('rel'):
                if "nofollow" in link.get('rel'):
                    d["follow"] = "no"
            if d not in self.outlinks and not d['url'].startswith('javascript'):
                self.outlinks.append(d)


def crawl_result(threadNum, largestNumber, seedUrls):
    pool = Queue()
    exist = []
    thread_num = threadNum
    lock = threading.Lock()
    # output = open("final.csv", "a")
    nodes = []
    links = []
    for seedUrl in seedUrls:
        # the domain is the start point
        domain = seedUrl
        if not seedUrl.startswith('http'):
            domain = 'http://%s' % seedUrl
        pool.put(domain)
        exist.append(domain)
        nodes.append({'url': domain, 'id': 0, 'numberOfIncome': 0, 'numberOfOutcome': 0})


    def crawl():

        while len(exist) <= largestNumber:
            # print len(exist)
            # print "%s crawls exist length before %s %s" % (threading.currentThread().getName(), len(exist),time.time()-start)
            # print "%s crawls pool length before %s" % (threading.currentThread().getName(), pool.qsize())
            if pool.qsize()==0:
                continue
            url = pool.get()
            print "%s , url:  %s %s" % (threading.currentThread().getName(), url,time.time()-start)
            p = Page(url)

            # write data to output file
            # lock.acquire()
            # output.write(p.url+" "+str(p.status)+"\n")
            # print "%s crawls %s %s %s" % (threading.currentThread().getName(), p.url,time.time()-start,p.error)
            # print "%s crawls exist length after %s" % (threading.currentThread().getName(), len(exist))
            # lock.release()

            if not p.error:
                # print 'in'
                p.outlinks()
                # print 'out'
                # print "%s crawls bllllllllllllllllllllll %s" % (threading.currentThread().getName(),time.time()-start)
                outlinks = p.outlinks
                this_node_index = exist.index(url)
                # if urlparse.urlparse(p.url)[1] == urlparse.urlparse(domain)[1] :
                for link in outlinks:
                    # print "%s crawls ----------------------------- %s" % (threading.currentThread().getName(),time.time()-start)
                    if link['url'] not in exist:
                        with lock:
                            # print "%s crawls looooooooooooooock %s" % (threading.currentThread().getName(),time.time()-start)
                            if (len(exist) <= 20):
                                pool.put(link['url'])
                            exist.append(link['url'])
                            nodes.append(
                                {'url': link['url'], 'id': len(exist) - 1, 'numberOfIncome': 1, 'numberOfOutcome': 0})
                            links.append(
                                {'source': this_node_index, 'target': len(exist) - 1, 'value': 1, 'type': 'suit'})
                            nodes[this_node_index]['numberOfOutcome'] += 1
                    else:
                        target_node_index = exist.index(link['url'])
                        with lock:
                            # print "%s crawls lOOOOOOOOOOOOOOOOOck %s" % (threading.currentThread().getName(),time.time()-start)
                            links.append(
                                {'source': this_node_index, 'target': target_node_index, 'value': 1, 'type': 'suit'})
                            nodes[this_node_index]['numberOfOutcome'] += 1
                            nodes[target_node_index]['numberOfIncome'] += 1

                            print "%s crawls exist length after %s" % (threading.currentThread().getName(), len(exist))
                            print "%s crawls pool length after %s" % (threading.currentThread().getName(), pool.qsize())

        print "%s crawls closed" % (threading.currentThread().getName())

    wokers = []

    for i in range(thread_num):
        t = threading.Thread(target=crawl)
        t.setDaemon(True)
        t.start()
        wokers.append(t)

    for worker in wokers:
        worker.join()

    # pool.join()
    # output.close()
    print len(exist)
    # print exist
    list={}
    list['nodes']=nodes
    list['links']=links
    return json.dumps(list)

# print crawl_result(10,20,['http://microso.me'])