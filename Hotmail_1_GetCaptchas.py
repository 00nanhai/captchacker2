#!coding: utf-8
import urllib2
import os
import cookielib
import time

#TRACEBACK
import traceback
import sys
def Myexcepthook(type, value, tb):
        lines=traceback.format_exception(type, value, tb)
        f=open('error.txt', 'a')
        f.write("\n".join(lines))
        f.close()
        print "\n".join(lines)
sys.excepthook=Myexcepthook


#INSTALLATION DU COOKIE
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'), ('Connection' , 'Keep-Alive')]
urllib2.install_opener(opener)

def html(s):
    f=open("a.html","w")
    f.write(s)
    f.close()
    os.startfile("a.html")

def request(URL, data=None, headers={}, param=0):
    req = urllib2.Request(URL, data)
    for key, content in headers.items():
        req.add_header(key, content)
    handle = urllib2.urlopen(req)
    data=handle.read()
    if not param:
        return data, handle
    else:
        return data, handle, req

def write_file(file, s):
    f=open(file, 'wb')
    f.write(s)
    f.close()



LIEN_IMAGES = "https://login.live.com/pp600/hip.srf?int=login"




def save_image(i):
    a, b, req1 = request(LIEN_IMAGES, param=1)
    write_file('Hotmail/Rough Catpchas/Image%03d.jpg'%i, a)
    print i



for i in range(851, 1000):
    save_image(i)

