#!coding: utf-8
from svm import *
from svmutil import *
import os, sys
from PIL import Image

##import psyco
##psyco.full()

##C=10
##KERNEL = RBF

if not os.path.isfile(os.path.join(MODEL_FOLDER, MODEL_FILE)) or GENERATE_ANYWAY:
    #Si le modèle n'existe pas ou que l'on veut spécifie GENERATE_ANYWAY=True, on le génère. Sinon, on le charge.

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

else:
    model = svm_model(os.path.join(MODEL_FOLDER, MODEL_FILE))
    print "Model successfully loaded."


def predict(model, chemin_image):

    if not os.path.isfile(chemin_image):
        print "FICHIER INEXISTANT"
        return

    data = list(Image.open(chemin_image).convert('L').getdata())
    data = map(lambda e:e/255., data)

    prediction = model.predict(data)
    probability = model.predict_probability(data)

    

    if VERBOSE:
        print probability

    return prediction


def analyze_folder(folder):
    errors = 0
    nb = 0
    for folder, subfolders, files in os.walk(folder):
        for file in [file for file in files if 'bmp' in file]:
            prediction = predict(model, os.path.join(folder, file))
            if prediction != ord(folder[-1])-65:
                errors += 1
            nb += 1
    print "Errors: %d / %d\n" % (errors, nb)
    return 100.*errors/nb



##print """
################################################################################
##############################    TEST MODEL    ################################
################################################################################
##"""
##
##error_rate_tr = 0
##nb_tr = 0
##print "Test on training set:"
##print "---------------------"
##for subdir in os.listdir(TRAINING_FOLDER):
##    if subdir[0] != ".":
##        print "Testing on", subdir[-1]
##        error_rate_tr += analyze_folder(os.path.join(TRAINING_FOLDER, subdir))
##        nb_tr += 1
##error_rate_tr /= nb_tr
##
##error_rate_test = 0
##nb_test = 0
##print "Test on test set:"
##print "-----------------"
##for subdir in os.listdir(TEST_FOLDER):
##    if subdir[0] != ".":
##        print "Testing on", subdir[-1]
##        error_rate_test += analyze_folder(os.path.join(TEST_FOLDER, subdir))
##        nb_test += 1
##error_rate_test /= nb_test
##
##print
##print "Error on training set:", error_rate_tr, '%'
##print "Error on test set:", error_rate_test, '%'
