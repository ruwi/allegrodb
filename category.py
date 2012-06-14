#-*- coding: utf-8 -*-
import sys
import urllib2 as url
from HTMLParser import HTMLParser

class CategoryParser(HTMLParser):
    def init(self,*args,**argv):
        self.p = 0
        if 'p' in args:
            self.p = 1
        if 'db' in args:
            self.conn = psycopg2.connect("dbname=test user=postgres") #FIXME
            self.cur = self.conn.cursor()
        self.clean()
        
    def clean(self):
        self.n = 0
        self.lvl = -1
        self.www = ''
        self.title = ''
        self.quantity = ''
        
    def handle_starttag(self,tag,attrs):
        for i in range(1,5):
            if (tag == 'a') and (('class',
                    "alleLink lvl" + str(i)) in attrs):
                self.n=1
                self.lvl=i
                self.www = [i[1] for i in attrs
                        if i[0]=='href'][0]
        q =[i[1] for i in attrs    if i[0] =='class']
        if q:
            if (tag == 'span') and ("small" in q[0]):
                self.n=2

    def handle_endtag(self,tag):
        if self.n == 1 and tag == 'a':
            self.n = 0
        if self.n == 2 and tag == 'span':
            self.n = 0
        if tag == 'div' and self.www:
            self.push_to_db()

    def handle_data(self,data):
        if self.n == 1:
            self.title = data
        elif self.n == 2:
            try:
                self.quantity = data[1:-1]
            except:
                print "error: niewłaściwy format: '"+data+''
                print "self.title",self.title
                print "self.www",self.www
                sys.exit(2)
                self.quality = data 

    def push_to_db(self):
        self.cat_title[self.lvl]=self.title
        if self.p:
            #wypisanie danych
            print 'lvl=      ',self.lvl
            print 'www=      ',self.www
            print 'title=    ',self.title
            print 'quantity= ',self.quantity
            print ''

        if self.cur:
            self.cur.execute("""INSERT INTO category(name,url,cat_id) """)
            pass #TODO: zapis do db
        self.clean()
            

www = 'http://allegro.pl/category_map.php'
try:
    s = url.urlopen(www).read()
except:
    print "błąd przy pobieraniu głównego źródła"
    sys.exit(1)
c = CategoryParser()
c.init('p')
c.feed(s)

