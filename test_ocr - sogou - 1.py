#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys,os
import urllib

import cv,cv2
import numpy as np 
                
#垂直像素分布
def Y_sum(im):
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
    #print ps 
    dist_image=np.uint8(np.zeros((height,width)))
    #画图
    for x in range(width):
        for y in range(ps[x]):    
            dist_image[height-y-1,x]=255

    return dist_image

#水平像素分布
def X_sum(im):
    width = len(im[0,:])
    height= len(im[:,0])
    ps=[]
    #统计垂直像素
    for x in range(height):
        ps.append(0)
        for y in range(width):
            #print x,y
            if im[y,x]==255:  
                ps[x]=ps[x]+1
    #print ps 
    dist_image=np.uint8(np.zeros((height,width)))
    #画图
    for x in range(height):
        for y in range(ps[x]):    
            dist_image[x,width-y-1]=255

    return dist_image


    
if __name__=='__main__':

    #下载样本图片

    for i in range(50):
        url = 'https://account.sogou.com/captcha?token=a48bfd1ef5ccf580220fa2b2c8a748ba&t=1406275496338' #验证码的地址
        #url = 'https://jaccount.sjtu.edu.cn/jaccount/captcha?0.6748697580769658'
        print "download", i
        file("./pic_sogou/%04d.png" % i, "wb").write(urllib.urlopen(url).read())
        image_name ="./pic_sogou/%04d.png" %i
        print image_name
        image = cv2.imread(image_name)
        #灰度化
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("./pic_sogou/%04dgray.png" %i,gray_image)
        #二值化
        ret,thresh1 = cv2.threshold(gray_image,100,255,cv2.THRESH_BINARY)
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
        #
        cv2.imwrite("./pic_sogou/%04dDilated.png"%i,dilated);

        
        eroded = cv2.erode(dilated,kernel)
        cv2.imwrite("./pic_sogou/%04deroded.png"%i,eroded);
        
        #提取轮廓
        image_contours = cv2.imread("./pic_sogou/%04dDilated.png"%i) 
        contours, hierarchy = cv2.findContours(255-thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print contours, hierarchy
        cv2.drawContours(image_contours, contours, -1, (0,255,0), 1)
        cv2.imwrite("./pic_sogou/%04dcontours.png"%i,image_contours)

        #删除噪点
        image_decontours = cv2.imread("./pic_sogou/%04dDilated.png"%i)
        contours, hierarchy = cv2.findContours(255-thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        #print type(contours)
        contours_dele=[]
        for contour in contours:
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
        #print ps 
        dist_image=np.uint8(np.zeros((height,width)))
        #画图
        for x in range(width):
            for y in range(ps[x]):
                
                dist_image[height-y-1,x]=255
        cv2.imwrite("./pic_sogou/%04ddist.png"%i,255-dist_image); 


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

        #按色彩提取数字
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


                
              
                #统计水平像素
                im=gray_image_tmp2
                width = len(im[0,:])
                height= len(im[:,0])
                Xdist=[]
                for x in range(height):
                    Xdist.append(0)
                    for y in range(width):
                        #print x,y
                        if im[x,y]==0:  
                            Xdist[x]=Xdist[x]+1
                    #print ps[x] 
                print "X"
                print Xdist
                
                dist_image=np.uint8(np.zeros((height,width)))
                #画图
                for x in range(height):
                    for y in range(Xdist[x]):
                        
                        dist_image[x,width-y-1]=255
                Xdist_name="./pic_sogou/%04dgray%04dMedianXdist.png"%(i,gray)   
                cv2.imwrite(Xdist_name,255-dist_image)
                #裁剪
                #滑动窗
                y_windows=10
                y_counter=0
                Xdist_sum=[]
                for y in range(height-y_windows):
                    Xdist_sum.append(sum(Xdist[y:y+y_windows]))
                    #print ps
                    #print "ps_sum"
                    #print Xdist_sum
                    if y_counter==0:
                        
                        if Xdist_sum[y]>5:
                            digit_up=y-3+y_windows
                            y_counter=1
                            
                    if  y_counter==1:
                        if Xdist_sum[y]<5:
                            if y-3+y_windows-digit_up>30:
                                digit_down=y+3
                                y_counter=2

                im=gray_image_tmp2
                width = len(im[0,:])
                height= len(im[:,0])
                Ydist=[]
                #统计垂直像素
                for x in range(width):
                    Ydist.append(0)
                    for y in range(height):
                        #print x,y
                        if im[y,x]==0:  
                            Ydist[x]=Ydist[x]+1
                 
                dist_image=np.uint8(np.zeros((height,width)))
                print "Y"
                print Ydist
                #画图
                for x in range(width):
                    for y in range(Ydist[x]):   
                        dist_image[height-y-1,x]=255
                Ydist_name="./pic_sogou/%04dgray%04dMedianYdist.png"%(i,gray)        
                cv2.imwrite(Ydist_name,255-dist_image);
                #裁剪
                #滑动窗
                x_windows=10
                x_counter=0
                Ydist_sum=[]
                for x in range(width-x_windows):
                    Ydist_sum.append(sum(Ydist[x:x+x_windows]))

                    if x_counter==0:
                        if Ydist_sum[x]>5:
                            digit_left=x-3+x_windows
                            print "digit_left"
                            print digit_left
                            
                            x_counter=1
                    if  x_counter==1:
                        if Ydist_sum[x]<5:
                            if x-3+x_windows-digit_left>10:
                                digit_right=x+3
                                print "digit_right"
                                print digit_right
                                x_counter=2
                        else:
                            digit_right=width 
                print "Ydist_sum"
                print Ydist_sum
                
                print digit_up,digit_down,digit_left,digit_right
                crop_image=gray_image_tmp2[digit_up:digit_down,digit_left:digit_right]
                crop_image_name="./pic_sogou/%04dgray%04dMediancrop.png"%(i,gray)
                cv2.imwrite(crop_image_name,255-crop_image)
                #resize_crop_image=cv2.resize(crop_image,(32,16),interpolation = cv2.INTER_CUBIC)
                resize_crop_image=cv2.resize(crop_image,(32,16))
                Resize_crop_image_name="./pic_sogou/01/%04dgray%04dMediancropResize.png"%(i,gray)
                cv2.imwrite(Resize_crop_image_name,255-crop_image)





        
        
        
