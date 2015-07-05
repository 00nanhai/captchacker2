#!coding: utf-8
from svm import *
from svmutil import *
import os, sys
from PIL import Image
import time
import urllib2
import os
import cookielib

from characters_center import *
import cv,cv2
import copy 
#import psyco
#psyco.full()
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

def load_image(path):
    im = Image.open(path)
    im = im.point(lambda e : e/255.)
    data = list(im.getdata())
    return data

def save_image(i=0, image_url="http://www.egoshare.com/captcha.php", path=""):
    while True:
        try:
            a, b, req1 = request(image_url, param=1)
        except Exception, ex:
            print "Echec ("+str(Exception)+" "+str(ex)+", nouvelle tentative dans 1s..."
            time.sleep(1)
        else:
            break
    
    if path is "":
        file = "Rough Captchas/Image%03d.jpg"%i
        print i
    else:
        file = path
    write_file(file, a)
    
    return file

def predict(model, im):
    data = list(im.getdata())
    prediction,p_acc ,p_vals= svm_predict([1],[data],model,'-b 1')
    labels = []
    for label in model.get_labels():
       labels.append(chr(65 + label)) 

    dict_p_vals = dict(zip(labels,p_vals[0]))
    return chr(65+int(prediction[0])), str(max(p_vals[0])),dict_p_vals 

def break_captcha(model, letters_path):
    letters = []
    values = ''
    prob = []
    predictions_detail = []
    for i in range(len(letters_path)):
        im = Image.open(letters_path[i])
        im = im.point(lambda e : e/255)
        tmp = []
        
        prediction, max_score, dico = predict(model, im)
        #print prediction
        tmp.append(prediction)
        tmp.append(max_score)
        tmp.append(dico)
        predictions_detail.append(tmp)

    for i in range(len(predictions_detail)):
        values += str(predictions_detail[i][0])
        prob.append(float (predictions_detail[i][1]))

    return values,min(prob), predictions_detail



WIDTH = 20
HEIGHT = 20 
class CC:
    comp = None
    mask = None  

def func_compare_area_cc(a, b):
    return int (b.comp[0] - a.comp[0])

def func_compare_pos_cc(a, b):
    return  int (a.comp[2][0] - b.comp[2][0])

def split_captcha( filenameIN):
    threshold = 150
    threshold = 200
    maxValue = 255
    thresholdType = cv.CV_THRESH_BINARY
    srcImg = cv.LoadImage(filenameIN,1)
    grayThresh = cv.CreateImage( (srcImg.width, srcImg.height), cv.IPL_DEPTH_8U, 1 )
    cv.CvtColor(srcImg, grayThresh, cv.CV_BGR2GRAY )
    cv.Threshold(grayThresh, grayThresh, threshold, maxValue, thresholdType)
    cv.SaveImage((filenameIN+"grayThresh.bmp"), grayThresh)
    connectivity = 4
    CCs4 = []

    gray4 = cv.CloneImage(grayThresh)

    for  i in range(gray4.width):
        for j in range(gray4.height):
            if (cv.Get2D(gray4, j, i)[0] == 0): 
                cc = CC()
                cc.mask = cv.CreateImage((gray4.width+2, gray4.height+2), cv.IPL_DEPTH_8U, 1)
                cv.Zero(cc.mask)
                cc.comp = cv.FloodFill(gray4, (i,j), cv.Scalar(128),cv.ScalarAll(0),cv.ScalarAll(0), connectivity, cc.mask)
                CCs4.append(cc)
    
    CCs4.sort(cmp = func_compare_area_cc)            

    size = len(CCs4)
    for i in range (size):
        if (CCs4[size - 1 -i].comp[0] < 20):
            CCs4.pop()

    connectivity = 8
    CCs8 = []
    gray8 = cv.CloneImage(grayThresh)
    for i in range (gray8.width):
        for j in range (gray8.height):
            if (cv.Get2D(gray8, j, i)[0] == 0):    
                cc = CC()
                cc.mask = cv.CreateImage((gray8.width+2, gray8.height+2), cv.IPL_DEPTH_8U, 1)
                cv.Zero(cc.mask)
                cc.comp = cv.FloodFill(gray8, (i,j), cv.Scalar(128),cv.ScalarAll(0),cv.ScalarAll(0), connectivity, cc.mask)
                CCs8.append(cc)
    CCs8.sort(cmp = func_compare_area_cc)            


    size = len(CCs8)
    for i in range (size):
        if (CCs8[size - 1 -i].comp[0] < 20):
            CCs8.pop()

    CCs = []
    CCs = copy.copy(CCs8)
    # if (len(CCs8) < 3):
    #     CCs = copy.copy(CCs4)
    # else :
    #     if (CCs4[2].comp[0] < 20):
    #         CCs = copy.copy(CCs8)
    #     else:
    #         CCs = copy.copy(CCs4)
    CCs.sort(cmp = func_compare_pos_cc)
    letters = []
    letters_path = []

    for i in range(len(CCs)):
        letter = cv.CreateImage( (WIDTH, HEIGHT), cv.IPL_DEPTH_8U, 1 )
        cv.Set(letter, 255)
        letters.append(letter) 
    for index_image in range (len(letters)):
        letter = letters[index_image]
        cc = CCs[index_image]
 
        offsetx = (WIDTH -  cc.comp[2][2])/2
        offsety = (HEIGHT - cc.comp[2][3])/2
    
        for i in range(1,cc.mask.width-1):
            for j in range (1,cc.mask.height-1):
                if (cv.Get2D(cc.mask, j, i)[0] == 1):
                    Y = j - cc.comp[2][1] + offsety
                    X = i - cc.comp[2][0] + offsetx

                    if ((X>0) and (X<WIDTH) and (Y>0) and (Y<HEIGHT)):
                        cv.Set2D(letter,
                            j - cc.comp[2][1] + offsety,
                            i - cc.comp[2][0] + offsetx,
                            cv.Scalar(0))
        letters_path.append(filenameIN+str(index_image+1)+".bmp")
        cv.SaveImage((filenameIN+str(index_image+1)+".bmp"), letters[index_image]) 
        process_file(letters_path[index_image], WIDTH = 31, HEIGHT = 31)
    return letters_path

def preprocess_captcha_part(file):
    letter_algo = []
    letters = split_captcha(file)
    
    for i in range (len(letters)):

        #letter = Image.fromstring("L", cv.GetSize(letters[i]), letters[i].tostring())
        letter = Image.open(letters[i])
        letter_algo.append(letter.point(lambda i: (i/255.)))

    return letters



