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



LIEN_IMAGES = "http://www.egoshare.com/captcha.php"




def save_image(i=0, path=""):
    while True:
        try:
            a, b, req1 = request(LIEN_IMAGES, param=1)
        except Exception, ex:
            print "Echec ("+str(Exception)+" "+str(ex)+", nouvelle tentative dans 1s..."
            time.sleep(1)
        else:
            break
    
    if path is "":
        file = "Egoshare/Rough Captchas/Image%03d.jpg"%i
        print i
    else:
        file = path
    write_file(file, a)
    
    return file


if __name__ == "__main__":
    for i in range(500):
        save_image(i)

