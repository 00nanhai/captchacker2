#!coding: utf-8
from svm import *
import os, sys
from PIL import Image

#import psyco
#psyco.full()

from Preprocess import load_image
from cross_validation import *


#TRACEBACK
import traceback
import sys
def Myexcepthook(type, value, tb):
        lines=traceback.format_exception(type, value, tb)
        f=open('log.txt', 'a')
        f.write("\n".join(lines))
        f.close()
        print lines
        raw_input()
sys.excepthook=Myexcepthook


print "Loading characters..."

TRAINING_FOLDER = 'Egoshare/DBTraining-Captcha_based'

labels = []
samples = []

for folder, subfolders, files in os.walk(TRAINING_FOLDER):
    if folder[0] != ".":
        loaded = False
        for file in [file for file in files if 'bmp' in file]:
            if not loaded:
                print "Loading ", folder
                loaded = True
            im = Image.open(os.path.join(folder, file))
            labels.append(ord(folder[-1])-65)
            samples.append(map(lambda e:e/255., list(im.getdata())))
print "Loading done."


print "\nStarting cross-validation..."
rates = []
CRANGE = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]
for C in CRANGE:
    param = svm_parameter(kernel_type = RBF, C=C, probability = 1) #, gamma=1./(2*1.25**2))
    rate = do_cross_validation(samples, labels, param, 10)

    f=open('cross-validation_results.txt', 'a')
    f.write("C="+str(C)+"\tgamma=default\t=>\t"+str(rate)+'\n')
    f.close()

    rates.append(rate)


print "Cross-validation done\n"
print "SUCCES RATES: ", rates
print "\nOPTIMAL PARAMETERS: "
index = rates.index(max(rates))
print "C = ", CRANGE[index]
print "Optimal success rate: ", max(rates)

raw_input()
