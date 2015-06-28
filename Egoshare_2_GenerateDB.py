#!coding: utf-8
#import psyco
from Isolated_Char_Generator import *
from Break_Egoshare_Captcha import *
import shutil


CAPTCHA_BASED = True # using captchas from the website
SIMULATION_BASED = False # using simulated captchas with various fonts


if SIMULATION_BASED:
    DEFAULT_SIZE = (30, 30)
    GENERATE_TRAINING_SET = False
    GENERATE_VALIDATION_SET = True

    if GENERATE_TRAINING_SET:
        print """
        ##############################################################################
        ##############   SIMULATION   BASED   TRAINING    SET   ######################
        ##############################################################################
        """

        GENERATE_CAPITAL_LETTERS = False
        GENERATE_DIGITS = True
        elem_to_gen = Generate_Element_List(GENERATE_CAPITAL_LETTERS, GENERATE_DIGITS)


        DESTINATION_FOLDER = 'Egoshare/DBTraining-Simulation_based'
        CLEAN_DESTINATION_FOLDER = True
        DISTORTION_W_MIN = 0
        DISTORTION_W_MAX = 1
        DISTORTION_H_MIN = 0
        DISTORTION_H_MAX = 1
        SCALE_MIN = 17
        SCALE_MAX = 23
        STEP = 1
        ALIGN_RANGEY = [0.5]
        ALIGN_RANGEX = [0.5]
        ROTATIONS = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
        FONTS = [("Fonts/comic.ttf", (145, 163)),
                 ("Fonts/vera.ttf", (160, 180)),
                 ("Fonts/califb.ttf", (171, 191))]
        Generate_Set(DESTINATION_FOLDER,CLEAN_DESTINATION_FOLDER,DISTORTION_W_MIN,DISTORTION_W_MAX,DISTORTION_H_MIN,
                     DISTORTION_H_MAX,SCALE_MIN,SCALE_MAX,STEP, elem_to_gen, FONTS, ALIGN_RANGEX, ALIGN_RANGEY, DEFAULT_SIZE, ROTATIONS)


    if GENERATE_VALIDATION_SET:
        print """
        ##############################################################################
        #################   SIMULATION   BASED   TEST    SET   #######################
        ##############################################################################
        """

        GENERATE_CAPITAL_LETTERS = False
        GENERATE_DIGITS = True
        elem_to_gen = Generate_Element_List(GENERATE_CAPITAL_LETTERS, GENERATE_DIGITS)

        DESTINATION_FOLDER = 'Egoshare/DBTest-Simulation_based'
        CLEAN_DESTINATION_FOLDER = True
        DISTORTION_W_MIN = 0
        DISTORTION_W_MAX = 2
        DISTORTION_H_MIN = 0
        DISTORTION_H_MAX = 2
        SCALE_MIN = 15
        SCALE_MAX = 20
        STEP = 2
        ALIGN_RANGEY = [0.7, 1]
        ALIGN_RANGEX = [0.5]
        ROTATIONS = [2, 9, 13, 22]
        FONTS = [("Fonts/comic.ttf", (140, 160)),
                 ("Fonts/vera.ttf", (160, 180)),
                 ("Fonts/califb.ttf", (160, 180))]
        Generate_Set(DESTINATION_FOLDER,CLEAN_DESTINATION_FOLDER,DISTORTION_W_MIN,DISTORTION_W_MAX,DISTORTION_H_MIN,
                     DISTORTION_H_MAX,SCALE_MIN,SCALE_MAX,STEP, elem_to_gen, FONTS, ALIGN_RANGEX, ALIGN_RANGEY, DEFAULT_SIZE, ROTATIONS)



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


if CAPTCHA_BASED:
    GENERATE_TRAINING_SET = True   # using hand-labelled captchas
    GENERATE_VALIDATION_SET = True # using hand-labelled captchas
    GENERATE_COMPUTER_LABELLED_SET = False

    if GENERATE_TRAINING_SET:
        print """
        ##############################################################################
        ##############   CAPTCHA   BASED   TRAINING    SET   #########################
        ##############################################################################
        """
        CAPTCHA_SOURCE_FOLDER = "Egoshare/Labelled Catpchas Training"
        DEST_FOLDER = "Egoshare/DBTraining-Captcha_based"
        Generate_Captcha_Based_set(CAPTCHA_SOURCE_FOLDER,DEST_FOLDER)

    if GENERATE_VALIDATION_SET:
        print """
        ##############################################################################
        #################   CAPTCHA   BASED   TEST    SET   ##########################
        ##############################################################################
        """
        CAPTCHA_SOURCE_FOLDER = "Egoshare/Labelled Catpchas Test"
        DEST_FOLDER = "Egoshare/DBTest-Captcha_based"
        Generate_Captcha_Based_set(CAPTCHA_SOURCE_FOLDER,DEST_FOLDER)


    if GENERATE_COMPUTER_LABELLED_SET:
        print """
        ##############################################################################
        ############   COMPUTER  LABELLED  CAPTCHA  BASED   SET   ####################
        ##############################################################################
        """
        DEST_FOLDER = "Egoshare/Computer Labelled Captcha based set"
        CAPTCHA_SOURCE_FOLDER = "Egoshare/Rough Captchas"

        MODEL_FILE = 'Egoshare/Models/captcha_based_TR=687_TEST=143_C=1000_KERNEL=1.svm'
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


    raw_input()
