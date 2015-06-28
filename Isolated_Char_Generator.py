#!coding: utf-8
#import psyco
#psyco.full()

from Captcha.Visual import Text, Backgrounds, Distortions, ImageCaptcha
from Captcha import Words
import random
import os
from PIL import ImageFont
from PIL import ImageChops

from PIL import Image

### CAPTCHA GENERATOR ###

class MyCaptcha(ImageCaptcha):

    def __init__(self, scale = 35, distortion = (5,5), solution = "9C8G5D",
                 font = "califfb/califb.ttf", alignx = 0.5, aligny = 0.5,
                 size = (38, 31)):
        self.distortion = distortion
        self.scale = scale
        self.fontFactory = Text.FontFactory(scale, font)
        self.solution = solution
        self.alignx = alignx
        self.aligny = aligny
        print self.fontFactory.pick()

        font = ImageFont.truetype(*self.fontFactory.pick())
        #textSize = font.getsize(self.solution)
        #print textSize
        #self.defaultSize = (38, self.distortion[0]+10+self.scale)
        self.defaultSize = size
        ImageCaptcha.__init__(self)


    def getLayers(self):
        #self.addSolution(self.solution)

        textLayer = Text.TextLayer(self.solution,
                                   fontFactory = self.fontFactory,
                                   alignment = (self.alignx, self.aligny))

        return [
            Backgrounds.SolidColor(),
            textLayer,
            Distortions.SineWarp(amplitudeRange = self.distortion)
            ]


### SET GENERATOR ###

def Generate_Set(DESTINATION_FOLDER,CLEAN_DESTINATION_FOLDER,
                 DISTORTION_W_MIN,DISTORTION_W_MAX, DISTORTION_H_MIN,DISTORTION_H_MAX,
                 SCALE_MIN,SCALE_MAX,STEP, elem_to_gen, fonts, ALIGN_RANGEX, ALIGN_RANGEY, DEFAULT_SIZE, ROTATION_RANGE=[], DXDY=[]):
    if not os.path.isdir(DESTINATION_FOLDER, ):
        os.mkdir(DESTINATION_FOLDER)
    else:
        if CLEAN_DESTINATION_FOLDER:
            print "Removing older files..."
            for subdir in os.listdir(DESTINATION_FOLDER):
                if subdir[0] != ".": # to prevent removal of .svn folders !
                    for file in os.listdir(os.path.join(DESTINATION_FOLDER, subdir)):
                        os.remove(os.path.join(DESTINATION_FOLDER, subdir, file))
                    try:
                        os.rmdir(os.path.join(DESTINATION_FOLDER, subdir))
                    except:
                        print "Impossible de supprimer le dossier", os.path.join(DESTINATION_FOLDER, subdir), "..."
            print "Done..."
            print

    print elem_to_gen,fonts
    for elem in elem_to_gen:
        print "Generating", elem, "..."
        if not os.path.isdir(os.path.join(DESTINATION_FOLDER,elem)):
            os.mkdir(os.path.join(DESTINATION_FOLDER,elem))

        for font, SEUILRANGE in fonts:
            font_name = font.split('/')[-1].split('.')[0]
            for scale in range(SCALE_MIN, SCALE_MAX, STEP):
                for distort_w in range(DISTORTION_W_MIN,DISTORTION_W_MAX, STEP):
                    for distort_h in range(DISTORTION_H_MIN,DISTORTION_H_MAX, STEP):
                        for alignx in ALIGN_RANGEX:
                            for aligny in ALIGN_RANGEY:
                                for SEUIL in SEUILRANGE:
                                    print scale,(distort_w,distort_h),elem,font,alignx,aligny, DEFAULT_SIZE
                                    captcha=MyCaptcha(scale, distortion = (distort_w,distort_h), solution = elem, font=font, alignx=alignx, aligny=aligny, size = DEFAULT_SIZE)
                                    image=captcha.render().convert('L')

                                    for i in xrange(DEFAULT_SIZE[0]):
                                        for j in xrange(DEFAULT_SIZE[1]):
                                            val = image.getpixel((i,j))
                                            if val < SEUIL:
                                                val = 0
                                            else:
                                                val = 255
                                            image.putpixel((i,j), val)


                                    if DXDY:
                                        for (i,j) in DXDY:
                                            if (i,j) != (0,0):
                                                file = os.path.join(DESTINATION_FOLDER,elem,elem+'_'+font_name+'_'+str(scale)+'_'+str(distort_w)+'_'+str(distort_h)+'_'+str(SEUIL)+'_'+str(alignx)+'_'+str(aligny)+'_0'+str(i)+'_'+str(j)+'.bmp')
                                                image1= image.resize((DEFAULT_SIZE[0] + i, DEFAULT_SIZE[1]+ j))
                                                image1.save(file)
                                                #print file



                                    if ROTATION_RANGE:
                                        #invert = image.point(lambda i : 255 - i)
                                        invert = ImageChops.invert(image)
                                        for rotation in ROTATION_RANGE:
                                            image1 = invert.rotate(rotation)
                                            file = os.path.join(DESTINATION_FOLDER,elem,elem+'_'+font_name+'_'+str(scale)+'_'+str(distort_w)+'_'+str(distort_h)+'_'+str(SEUIL)+'_'+str(alignx)+'_'+str(aligny)+'_'+str(rotation)+'.bmp')
                                            image1 = ImageChops.invert(image1)
                                            image1.save(file)
                                            #print file

                                            image1 = invert.rotate(-rotation)
                                            file = os.path.join(DESTINATION_FOLDER,elem,elem+'_'+font_name+'_'+str(scale)+'_'+str(distort_w)+'_'+str(distort_h)+'_'+str(SEUIL)+'_'+str(alignx)+'_'+str(aligny)+'_'+str(-rotation)+'.bmp')
                                            image1 = ImageChops.invert(image1)
                                            image1.save(file)
                                            #print file

        print elem + " files generated.\n"


### ELEMENT LIST GENERATOR ###

def Generate_Element_List(GENERATE_CAPITAL_LETTERS, GENERATE_DIGITS):
        elem_to_gen = []

        if GENERATE_CAPITAL_LETTERS:
            for i in range(65,91):
                elem_to_gen.append(chr(i))

        if GENERATE_DIGITS:
            for i in range(48,58):
                elem_to_gen.append(chr(i))

        return elem_to_gen
