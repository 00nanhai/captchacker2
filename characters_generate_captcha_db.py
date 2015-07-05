#!coding: utf-8
#import psyco
from characters_generate_element import *
from break_captcha_utils import *
import shutil

WIDTH = 20
WIDTH = 31
HEIGHT = 20
HEIGHT = 31

def Prepare_Dest_Folder(DEST_FOLDER):
    #Cr�ation du dossier de destination
    if not os.path.isdir(DEST_FOLDER):
        os.mkdir(DEST_FOLDER)

    #suppression des anciens fichiers
    print "Removing older files..."
    for subdir in os.listdir(DEST_FOLDER):
        print subdir
        if subdir[0] != ".": # to prevent removal of .svn folders !
            for file in os.listdir(os.path.join(DEST_FOLDER, subdir)):
                os.remove(os.path.join(DEST_FOLDER, subdir, file))
            try:
                os.rmdir(os.path.join(DEST_FOLDER, subdir))
            except Exception, ex:
                print "Impossible de supprimer le dossier", os.path.join(DEST_FOLDER, subdir), "..."
    print "Done..."

    #Cr�ation des sous-dossiers
    for i in range(10):
        folder = os.path.join(DEST_FOLDER, str(i))
        if not os.path.isdir(folder):
            os.mkdir(folder)



def Generate_Captcha_Based_set(CAPTCHA_SOURCE_FOLDER,DEST_FOLDER):
    Prepare_Dest_Folder(DEST_FOLDER)

    #Remplissage des sous-dossiers
    for folder, subfolders, files in os.walk(CAPTCHA_SOURCE_FOLDER):
        for file in [file for file in files if file[-4:] == ".jpg"]:
            filename = os.path.join(CAPTCHA_SOURCE_FOLDER, file)
            print file

            preprocess_captcha_part(os.path.join(folder, file),remove=False)

            name1 = file[:-4]+"number_1.bmp"
            name2 = file[:-4]+"number_2.bmp"
            name3 = file[:-4]+"number_3.bmp"

            shutil.move("letter1.bmp", os.path.join(DEST_FOLDER, file[0], name1))
            shutil.move("letter2.bmp", os.path.join(DEST_FOLDER, file[1], name2))
            shutil.move("letter3.bmp", os.path.join(DEST_FOLDER, file[2], name3))


def generate_captcha_base(GENERATE_TRAINING_SET,GENERATE_VALIDATION_SET,GENERATE_COMPUTER_LABELLED_SET):

    if GENERATE_TRAINING_SET:
        print """
        ##############################################################################
        ##############   CAPTCHA   BASED   TRAINING    SET   #########################
        ##############################################################################
        """
        CAPTCHA_SOURCE_FOLDER = "Labelled Catpchas Training"
        DEST_FOLDER = "DBTraining-Captcha_based"
        Generate_Captcha_Based_set(CAPTCHA_SOURCE_FOLDER,DEST_FOLDER)

    if GENERATE_VALIDATION_SET:
        print """
        ##############################################################################
        #################   CAPTCHA   BASED   TEST    SET   ##########################
        ##############################################################################
        """
        CAPTCHA_SOURCE_FOLDER = "Labelled Catpchas Test"
        DEST_FOLDER = "DBTest-Captcha_based"
        Generate_Captcha_Based_set(CAPTCHA_SOURCE_FOLDER,DEST_FOLDER)


    if GENERATE_COMPUTER_LABELLED_SET:
        print """
        ##############################################################################
        ############   COMPUTER  LABELLED  CAPTCHA  BASED   SET   ####################
        ##############################################################################
        """
        DEST_FOLDER = "Computer Labelled Captcha based set"
        CAPTCHA_SOURCE_FOLDER = "Egoshare/Rough Captchas"

        MODEL_FILE = 'models/captcha_based_TR=687_TEST=143_C=1000_KERNEL=1.svm'
        model = load_model(MODEL_FILE)

        Prepare_Dest_Folder(DEST_FOLDER)

        #Remplissage des sous-dossiers
        for folder, subfolders, files in os.walk(CAPTCHA_SOURCE_FOLDER):
            for file in [file for file in files if file[-4:] == ".jpg"]:
                filename = os.path.join(CAPTCHA_SOURCE_FOLDER, file)
                print file

                name1 = file[:-4]+"number_1.bmp"
                name2 = file[:-4]+"number_2.bmp"
                name3 = file[:-4]+"number_3.bmp"

                letter1_algo, letter2_algo, letter3_algo = preprocess_captcha_part(os.path.join(folder, file),remove=False)
                prediction = break_captcha(model, letter1_algo, letter2_algo, letter3_algo)

                shutil.move("letter1.bmp", os.path.join(DEST_FOLDER, prediction[0], name1))
                shutil.move("letter2.bmp", os.path.join(DEST_FOLDER, prediction[1], name2))
                shutil.move("letter3.bmp", os.path.join(DEST_FOLDER, prediction[2], name3))


        print """Done.

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!!!!!!!!   NOW CORRECT AND COPY MANUALLY COMPUTER LABELLED FILES   !!!!!!!!!!
        !!!!!!!!!        INTO CAPTCHA BASED TRAINING AND TEST FOLDERS       !!!!!!!!!!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """

