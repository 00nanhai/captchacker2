#!coding: utf-8
import os, sys
import time

from svm import *
from svmutil import *

from PIL import Image
from break_captcha_utils import *

MODEL_FOLDER = 'models'

def generate_captcha_based_model(KERNEL = POLY,TRAINING_FOLDER = 'DBTraining-Captcha_based'):
    CRANGE = [1000]
    
    for C in CRANGE:
        MODEL_FILE = "captcha_based_TR=1896_TEST=714_C="+str(C)+"_KERNEL="+str(KERNEL)+".svm"
        print """
        ##############################################################################
        ############################    TRAINING    ##################################
        ##############################################################################
        """

        labels = []
        samples = []

        print "LOADING IMAGES..."

        train_elem = '3de2mt'

        #Train everything
        train_elem = ''
        print TRAINING_FOLDER
        for folder, subfolders, files in os.walk(TRAINING_FOLDER):
            if (folder[0] != ".") and (folder[-1] in train_elem or train_elem == ''):
                loaded = False
                for file in [file for file in files if 'bmp' in file]:
                    if not loaded:
                        print "folder", folder, "loaded"
                        loaded = True
                    im = Image.open(os.path.join(folder, file))
                    #print ord(folder[-1])-65
                    labels.append(ord(folder[-1])-65)
                    #print map(lambda e:e/255., list(im.getdata()))
                    #samples.append(map(lambda e:e/255., list(im.getdata())))
                    samples.append(list(im.point(lambda i: (i/255.)).getdata()))
        print "Done.\n"

        print "GENERATING MODEL..."

        problem = svm_problem(labels, samples);
        size = len(samples)

        #param = svm_parameter(C = 10,nr_weight = 2,weight_label = [1,0],weight = [10,1], probability=1)
        #param = svm_parameter(kernel_type = KERNEL, C=C, probability = 1)
        param = svm_parameter('-t %s -c %s -b %s' % (KERNEL, C, 1))


        #kernels : LINEAR, POLY, RBF, and SIGMOID
        #types : C_SVC, NU_SVC, ONE_CLASS, EPSILON_SVR, and NU_SVR

        #model = svm_model(problem,param)
        #model = libsvm.svm_train(problem, param)
        #model = toPyModel(model)
        model = svm_train(problem, param)
        
        #model.save(os.path.join(MODEL_FOLDER, MODEL_FILE))
        svm_save_model(os.path.join(MODEL_FOLDER, MODEL_FILE),model)

        print "Done.\n"  
        return  os.path.join(MODEL_FOLDER, MODEL_FILE)

   
        
def generate_simulation_based_model(KERNEL = SIGMOID,TRAINING_FOLDER = 'DBTraining-Simulation_based'):
    CRANGE = [1000]

    for C in CRANGE:
        MODEL_FILE = "simulation_based_NEW_C="+str(C)+"_KERNEL="+str(KERNEL)+".svm"
        print MODEL_FILE
        print """
        ##############################################################################
        ############################    TRAINING    ##################################
        ##############################################################################
        """

        labels = []
        samples = []

        print "LOADING IMAGES..."

        train_elem = '3de2mt'

        #Train everything
        train_elem = ''
        print TRAINING_FOLDER
        for folder, subfolders, files in os.walk(TRAINING_FOLDER):
            if (folder[0] != ".") and (folder[-1] in train_elem or train_elem == ''):
                loaded = False
                for file in [file for file in files if 'bmp' in file]:
                    if not loaded:
                        print "folder", folder, "loaded"
                        loaded = True
                    im = Image.open(os.path.join(folder, file))
                    #print ord(folder[-1])-65
                    labels.append(ord(folder[-1])-65)
                    #print map(lambda e:e/255., list(im.getdata()))
                    #samples.append(map(lambda e:e/255., list(im.getdata())))
                    samples.append(list(im.point(lambda i: (i/255.)).getdata()))
        print "Done.\n"

        print "GENERATING MODEL..."

        problem = svm_problem(labels, samples);
        size = len(samples)

        #param = svm_parameter(C = 10,nr_weight = 2,weight_label = [1,0],weight = [10,1], probability=1)
        #param = svm_parameter(kernel_type = KERNEL, C=C, probability = 1)
        param = svm_parameter('-t %s -c %s -b %s' % (KERNEL, C, 1))


        #kernels : LINEAR, POLY, RBF, and SIGMOID
        #types : C_SVC, NU_SVC, ONE_CLASS, EPSILON_SVR, and NU_SVR

        #model = svm_model(problem,param)
        #model = libsvm.svm_train(problem, param)
        #model = toPyModel(model)
        model = svm_train(problem, param)
        
        #model.save(os.path.join(MODEL_FOLDER, MODEL_FILE))
        svm_save_model(os.path.join(MODEL_FOLDER, MODEL_FILE),model)

        print "Done.\n" 
        return  os.path.join(MODEL_FOLDER, MODEL_FILE)

        
def test_based_model(MODEL_FILE,TEST_FOLDER = 'DBTest-Simulation_based'):
    print """
    ##############################################################################
    ############################       TEST     ##################################
    ##############################################################################
    """

    set_files_errors = set([])
        
    model = svm_load_model( MODEL_FILE)
    
    nbs = 0
    errors = 0
    print TEST_FOLDER
    for folder, subfolders, files in os.walk(TEST_FOLDER):
        print folder
        if (folder[0] != "."):
            loaded = False
            print folder
            for file in [file for file in files if 'bmp' in file]:
                if not loaded:
                    print "Testing on ", folder
                    loaded = True
                print folder,file
                im = Image.open(os.path.join(folder, file))
                im = im.point(lambda e : e/255)
                
                char, max_score, scores = predict(model, im)


                if char == folder[-1]:
                    print "SUCCESS"
                    pass
                else:
                    print "FAILURE"
                    errors += 1
                    set_files_errors.add(file.split('number')[0])
                    #print "Error: ", char, "detected instead of", folder[-1]
                nbs += 1
                
    
    #nb_errors = len(set_files_errors)
    nb_errors = errors
    nb_captchas_tested = nbs
    print "\tnbs: ", nbs,"\tnb_errors: ", nb_errors
    print "\tSuccess rate: ", (1 - (1.*nb_errors/nb_captchas_tested))*100, "%"
    print 
    MODEL_FILE_TMP = MODEL_FILE + '\t' + str((1 - (1.*nb_errors/nb_captchas_tested))*100) + "%"
    svm_save_model(MODEL_FILE_TMP,model)         

def analyze_folder(folder):
    errors = 0
    nb = 0
    for folder, subfolders, files in os.walk(folder):
        for file in [file for file in files if 'bmp' in file]:
            prediction,prob,predictions_detail = predict(model, os.path.join(folder, file))
            if prediction != ord(folder[-1])-65:
                errors += 1
            nb += 1
    print "Errors: %d / %d\n" % (errors, nb)
    return 100.*errors/nb
            