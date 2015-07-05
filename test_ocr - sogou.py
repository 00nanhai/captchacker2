#!/usr/bin/env python
# -*- coding: UTF-8 -*-
###利用点的密度计算
import Image,ImageEnhance,ImageFilter,ImageDraw
import sys
import urllib
from pytesser import *
#计算范围内点的个数
import cv,cv2
import numpy as np 
#二值化

   
def numpoint(im):
    w,h = im.size
    data = list( im.getdata() )
    mumpoint=0
    for x in range(w):
        for y in range(h):
            if data[ y*w + x ] !=255:#255是白色
                mumpoint+=1
    return mumpoint
                
#计算5*5范围内点的密度
def pointmidu(im):
    w,h = im.size
    p=[]
    for y in range(0,h,5):
        for x in range(0,w,5):
            box = (x,y, x+5,y+5)
            im1=im.crop(box)
            a=numpoint(im1)
            if a<11:##如果5*5范围内小于11个点，那么将该部分全部换为白色。
                for i in range(x,x+5):
                    for j in range(y,y+5):
                        im.putpixel((i,j), 255)
    im.save(r'img.jpg')
        
def ocrend():##识别
    image_name = "img.jpg"
    im = Image.open(image_name)
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    im.save("1.tif")
    print image_file_to_string('1.tif')    
    
if __name__=='__main__':

    #下载样本图片

    for i in range(50):
        url = 'http://account.sogou.com/captcha?token=a48bfd1ef5ccf580220fa2b2c8a748ba&t=1406275496338' #验证码的地址
        print "download", i
        file("./pic_sogou/%04d.png" % i, "wb").write(urllib.urlopen(url).read())
        image_name ="./pic_sogou/%04d.png" %i
        print image_name
        image = cv2.imread(image_name)
        #灰度化
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('gray_image',gray_image)
        cv2.imwrite("./pic_sogou/%04dgray.png" %i,gray_image)
        #二值化
        ret,thresh1 = cv2.threshold(gray_image,100,255,cv2.THRESH_BINARY)
        #cv2.imshow('2_image',thresh1)
        cv2.imwrite("./pic_sogou/%04dthresh1.png" %i,thresh1)
        #自适应阈值
        threshold = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 11, 40)
        cv2.imwrite("./pic_sogou/%04dthreshold.png" %i,threshold)
        #定义核
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3, 3))
        
        Npkernel = np.uint8(np.zeros((2,2)))  
        Npkernel[1,1]=1
        Npkernel[0,0]=1
        
        
        #腐蚀图像
        eroded = cv2.erode(thresh1,kernel)
        cv2.imwrite("./pic_sogou/%04deroded.png"%i,eroded);

        #膨胀图像
        dilated = cv2.dilate(thresh1,kernel,iterations = 1)
        #print type(dilated)
        #
        cv2.imwrite("./pic_sogou/%04dDilated.png"%i,dilated);

        
        eroded = cv2.erode(dilated,kernel)
        cv2.imwrite("./pic_sogou/%04deroded.png"%i,eroded);
        
        #提取轮廓
        image_contours = cv2.imread("./pic_sogou/%04dDilated.png"%i) 
        contours, hierarchy = cv2.findContours(255-thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print contours, hierarchy
        cv2.drawContours(image_contours, contours, -1, (0,255,0), 1)
        #cv2.imshow("binary2", image_contours)
        cv2.imwrite("./pic_sogou/%04dcontours.png"%i,image_contours)

        #删除噪点
        image_decontours = cv2.imread("./pic_sogou/%04dDilated.png"%i)
        contours, hierarchy = cv2.findContours(255-thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        #print type(contours)
        contours_dele=[]
        for contour in contours:
            #print "contour"
            #print cv2.contourArea(contour)
            if cv2.contourArea(contour)<1500:
            #删除
                #print "contour delete"
                contours_dele.append(contour)

        cv2.drawContours(image_decontours,contours_dele,-1,(255,255,255),-1)
            
        cv2.imwrite("./pic_sogou/%04ddecontours.png"%i,image_decontours)
       
        
        
##        cv2.waitKey(0)
##        cv2.destroyAllWindows()

        #垂直直方图
        image2 = cv2.imread("./pic_sogou/%04ddecontours.png"%i)
        #灰度化
        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        #二值化
        ret,thresh1 = cv2.threshold(gray_image2,100,255,cv2.THRESH_BINARY)
        
        im=255-thresh1
        type(im)
        width = len(im[0,:])
        height= len(im[:,0])
        ps=[]
        #统计垂直像素
        for x in range(width):
            ps.append(0)
            for y in range(height):
                #print x,y
                if im[y,x]==255:  
                    ps[x]=ps[x]+1
            #print ps[x] 
        #print ps 
        dist_image=np.uint8(np.zeros((height,width)))
        #画图
        for x in range(width):
            for y in range(ps[x]):
                
                dist_image[height-y-1,x]=255
        cv2.imwrite("./pic_sogou/%04ddist.png"%i,255-dist_image); 

        #灰度分布直方图

        hist=cv2.calcHist([gray_image],[0],None,[256],[0.0,255.0])
        #print hist
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
        #print minVal, maxVal, minLoc, maxLoc
        
        histImg = np.zeros([256,256], np.uint8)
        #归一化256
        hpt = int(0.9* 256);
        for h in range(256):      
            intensity = int(hist[h]*hpt/maxVal)      
            cv2.line(histImg,(h,256), (h,256-intensity),(255))  
        cv2.imwrite("./pic_sogou/%04dcalcHist.png"%i,histImg);

        gray_image_tmp=np.uint8(np.zeros((height,width)))

        
        for gray in range(100):
            if hist[gray]>100:
                for x in range(width):
               
                    for y in range(height):
                        if gray_image[y,x]==gray:
                            gray_image_tmp[y,x]=0
                        else:
                           gray_image_tmp[y,x]=255
                #print i,gray
                gray_image_tmp_name="./pic_sogou/%04dgray%04d.png"%(i,gray)
                #print gray_image_tmp_name
                #gray_image_tmp = cv2.morphologyEx(gray_image_tmp, cv2.MORPH_CLOSE, kernel)
                #gray_image_tmp = cv2.morphologyEx(gray_image_tmp, cv2.MORPH_OPEN, kernel)
                cv2.imwrite(gray_image_tmp_name,gray_image_tmp)
                #中值滤波
                gray_image_tmp_name="./pic_sogou/%04dgray%04dMedian.png"%(i,gray)
            
                gray_image_tmp = cv2.erode(gray_image_tmp,kernel,iterations = 2)
                gray_image_tmp = cv2.dilate(gray_image_tmp,kernel,iterations = 2)
                gray_image_tmp2 = cv2.medianBlur(gray_image_tmp,3)
                cv2.imwrite(gray_image_tmp_name,gray_image_tmp2)
                im=gray_image_tmp2
                width = len(im[0,:])
                height= len(im[:,0])
                ps=[]
                #统计垂直像素
                for x in range(width):
                    ps.append(0)
                    for y in range(height):
                        #print x,y
                        if im[y,x]==255:  
                            ps[x]=ps[x]+1
                    #print ps[x] 
                #print ps 
                dist_image=np.uint8(np.zeros((height,width)))
                #画图
                for x in range(width):
                    for y in range(ps[x]):
                        
                        dist_image[height-y-1,x]=255
                cv2.imwrite("./pic_sogou/%04dgray%04dMedianYdist.png"%(i,gray),255-dist_image);
                #统计水平像素
                print height,width
                for x in range(height):
                    ps.append(0)
                    for y in range(width):
                        #print x,y
                        if im[x,y]==255:  
                            ps[x]=ps[x]+1
                    #print ps[x] 
                #print ps 
                dist_image=np.uint8(np.zeros((height,width)))
                #画图
                for x in range(width):
                    for y in range(ps[x]):
                        
                        dist_image[height-y-1,x]=255
                cv2.imwrite("./pic_sogou/%04dgray%04dMedianXdist.png"%(i,gray),255-dist_image);


        #三通道灰度分布直方图
        h = np.zeros((256,256,3))       
           
        bins = np.arange(256).reshape(256,1)       
        color = [ (255,0,0),(0,255,0),(0,0,255) ]       
        for ch, col in enumerate(color):      
            originHist = cv2.calcHist([image],[ch],None,[256],[0,256])      
            cv2.normalize(originHist, originHist,0,255*0.9,cv2.NORM_MINMAX)      
            hist=np.int32(np.around(originHist))      
            pts = np.column_stack((bins,hist))      
            cv2.polylines(h,[pts],False,col)      
           
        h=np.flipud(h)
        cv2.imwrite("./pic_sogou/%04dcalcThreeHist.png"%i,h);
        
        im = Image.open(image_name)
##        im = im.filter(ImageFilter.DETAIL)
##        im.save("./pic_sogou/%04dDETAIL.png" %i)
##        im = im.filter(ImageFilter.MedianFilter())
##        im.save("./pic_sogou/%04dMedianFilter.png" %i)
##        enhancer = ImageEnhance.Contrast(im)
##        im = enhancer.enhance(2)
##        im.save("./pic_sogou/%04denhance.png" %i)
        
        

        im = im.convert('1')
        im.save("./pic_sogou/%04dconvert.png" %i)
        ##a=remove_point(im)
        pointmidu(im)
        im.save("./pic_sogou/%04dpointmidu.png" %i)
        ocrend()
