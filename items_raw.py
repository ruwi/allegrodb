#-*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen

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
    pass #TODO

def all_items(source):
    p =  pages(source)
    if not p:
        return items(source)
    it = [items(urlopen(i).read()) for i in p]
    it = reduce(lambda x,y:x+y,it)
    return it

if __name__ == '__main__':
    s = open("items.html").read()
    for i in pages(s):
        print i
  

    
