#!coding: utf-8
from Break_Egoshare_Captcha import *

MODEL_FOLDER = 'Egoshare/Models'
MODEL_FILES = ['simulation_based_C=1000_KERNEL=1.svm']
#TEST_FOLDER = 'Egoshare/DBTest-Simulation_based'
TEST_FOLDER = 'Egoshare/DBTest-Captcha_based'

try:
    print MODEL_FILE
except:
    pass
else:
    MODEL_FILES = [MODEL_FILE]

set_files_errors = set([])

for MODEL_FILE in MODEL_FILES:
    print MODEL_FILE
    model = load_model(os.path.join(MODEL_FOLDER, MODEL_FILE))
    
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
                    #print "SUCCESS"
                    pass
                else:
                    #print "FAILURE"
                    set_files_errors.add(file.split('number')[0])
                    #print "Error: ", char, "detected instead of", folder[-1]
                nbs += 1
                
    
    nb_errors = len(set_files_errors)
    nb_captchas_tested = nbs/3
    print nbs,nb_errors,nb_captchas_tested
    print "\tSuccess rate: ", (1 - (1.*nb_errors/nb_captchas_tested))*100, "%"
    print 
    write(MODEL_FILE + '\t' + str((1 - (1.*nb_errors/nb_captchas_tested))*100) + "%")






