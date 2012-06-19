#-*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import time
from threading import Thread

def pages(source):
    soup = BeautifulSoup(source)
    last = soup.find('div',id="pagerBottom").findAll(
                        'a', {'class':'alleLink'})[-1]
    www = last['href']
    if www[0] == '/':
        www = 'http://www.allegro.pl' + www
    a = dict([i.split('=') for i in www[www.index('?')+1:].split('&')])
    max_no = int(a['p'])
    pages_ = [www[:www.index('p=')]+'p=' + str(i)
                    for i in range(max_no+1)[1:]]
    return pages_

def items(source):
    soup = BeautifulSoup(source)
    im = soup.findAll('a',{'class':'iImg'})
    im += soup.findAll('a',{'class':'iImg noPhoto'})
    href = [i['href'] for i in im]
    href = [(i[0]=='/')*'http://www.allegro.pl'+i for i in href]
    s = range(len(href))
    if len(im)==0:
        print "zero itemów"
        return []
    #threads:
    def read(www,id_ , out):
        for i in range(5):
            try:
                out[id_]=(www, urlopen(www).read())
                return None
            except:
                print "item: " + www
                time.sleep(1)
        print "errItem: " + www
    w = [Thread(target=read,args=(href[i],i,s)) for i in range(len(href))]
    for i in w:
        while True:
            try:
                i.start()
                break
            except:
                time.sleep(0.01)
    [i.join() for i in w]
    control_len=len(s)
    s = [i for i in s if type(i) != int]
    if control_len!=len(s):
        print "miss items: %i from %i" % (control_len-len(s), len(s))
    return s
        

def all_items(source):
    p =  pages(source)
    if not p:
        return items(source)
    it = range(len(p))
    #threads:
    def read(www,id_,out):
        for i in range(5):
            try:
                out[id_]=items(urlopen(www).read())
                return None
            except:
                print "page: " + www
                time.sleep(1)
        print "errPage: " + www
    w = [Thread(target=read,args=(p[i],i,it)) for i in range(len(p))]
    for i in w:
        while True:
            try:
                i.start()
                break
            except:
                time.sleep(0.01)
    [i.join() for i in w]
    control_len=len(it)
    it = [i for i in it if type(i) != int]
    if control_len!=len(it):
        print "miss pages: %i from %i" % (control_len-len(it), len(it))
    it = reduce(lambda x,y:x+y,it)
    return it

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print sys.argv[0] + " -www <www-adress>"
        print sys.argv[0] + " -cat <name_of_category>"
        print sys.argv

    s = open("items.html").read()
    for i in pages(s):
        print i
  

    
