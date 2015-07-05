import os, sys, time
import cv,cv2
#import psyco
#psyco.full()



WIDTH = 20
WIDTH = 31
HEIGHT = 20
HEIGHT = 31

#folder_to_process = "DBTraining-Simulation_based"
#folder_to_process = "Egoshare/DBTest-Simulation_based"
#folder_to_process = "Hotmail\DBTraining"

def process_file(filenameIN, WIDTH = 31, HEIGHT = 31):
    
    print "processing file: "+ filenameIN
    if not (os.path.exists(filenameIN)):
        print "file not found. Aborting."
        return
    else :
        srcImg = cv.LoadImage(filenameIN,0)
        res = cv.CreateImage( (WIDTH, HEIGHT), cv.IPL_DEPTH_8U, 1 )
        cv.Set(res, 255)
        xmin=WIDTH
        xmax=0
        ymin=HEIGHT
        ymax=0
        for i in range(srcImg.width):
            for j in range(srcImg.height):
                #print "xmax"
                #print cv.Get2D(srcImg, j, i)
                if cv.Get2D(srcImg, j, i)[0] == 0.0 :
                    #print "xin"
                    if i<xmin:
                        xmin = i
                    if i>xmax:
                        xmax = i
                    if j<ymin:
                        ymin=j
                    if j>ymax:
                        ymax=j
        
        offsetx = (WIDTH - (xmax-xmin))/2
        offsety = (HEIGHT - (ymax-ymin))/2
        #print 'WIDTH',WIDTH,"offset",offsety,offsetx
        for i in range(xmax-xmin):
            for j in range(ymax-ymin):
                if ((offsety+j>0) and (offsety+j<res.height) and (offsetx+i>0) and (offsetx+i<res.width)):
                    #print "haha"
                    cv.Set2D(res, offsety+j, offsetx+i, cv.Get2D(srcImg, ymin+j, xmin+i))

        cv.SaveImage(filenameIN, res)       
   
def process_folder(folder = "DBTraining-Simulation_based", WIDTH = 31, HEIGHT = 31):
    print "Processing " + folder + " folder... "
    if not (os.path.exists(folder ) ) :
        print "Folder not found. Aborting."
        return

    for folder, subfolders, files in os.walk(folder):
        for file in [file for file in files if 'bmp' in file]:
            process_file(os.path.join(folder, file),WIDTH, HEIGHT)
