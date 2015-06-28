#!coding: utf-8
import os
from PIL import Image
from PIL import ImageStat

SEUIL = 180

def preprocess_captcha(path, parent):

    if not os.path.isfile(path):
        print "FICHIER INEXISTANT"
        return

    im=Image.open(path)
    im = im.crop((24, 8, 151, 39)).convert('L')

    w = im.size[0]
    h = im.size[1]

    for i in xrange(w):
        for j in xrange(h):
            val = im.getpixel((i,j))
            if val < SEUIL:
                val = 0
            else:
                val = 255
            im.putpixel((i,j), val)

    #Si parent=None, on enl�ve le blanc sur les cot�s
    minx=100000
    maxx=0
    for i in xrange(w):
        for j in xrange(h):
            if im.getpixel((i,j)) == 0:
                if i<minx:
                    minx=i
                if i>maxx:
                    maxx=i

    im = im.crop((minx, 0, maxx, 31))

    DEST = path[:-4]+".bmp"
    im.save(DEST)

    return DEST


## Prend en argument le chemin de l'image, et la transforme en une liste � donner � la SVM
## Rescale et centre les donn�es
def load_image_with_mean(path):
    im = Image.open(path)

    #Puts all values between 0 and 1
    im = im.point(lambda e : e/255.)

    #Transforms into list
    data = list(im.getdata())

    #Centers data
    stat = ImageStat.Stat(im)
    mean = stat.mean[0]
    data = map(lambda e : e/mean, data)

    return data



def load_image(path):
    im = Image.open(path)

    #Puts all values between 0 and 1
    im = im.point(lambda e : e/255.)

    #Transforms into list
    data = list(im.getdata())

    return data
