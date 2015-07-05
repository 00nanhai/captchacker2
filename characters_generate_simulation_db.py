#!coding: utf-8
#import psyco
from characters_generate_element import Generate_Element_List,Generate_Set
from characters_center import process_folder
from break_captcha_utils import *
import shutil




#CAPTCHA_BASED = False # using captchas from the website
#SIMULATION_BASED = True # using simulated captchas with various fonts

def generate_simulation_base(GENERATE_TRAINING_SET,GENERATE_VALIDATION_SET, GENERATE_CAPITAL_LETTERS,GENERATE_SMALL_LETTERS,GENERATE_DIGITS):
    
    DEFAULT_SIZE = (30, 30)
  

    if GENERATE_TRAINING_SET:
        print """
        ##############################################################################
        ##############   SIMULATION   BASED   TRAINING    SET   ######################
        ##############################################################################
        """
        elem_to_gen = Generate_Element_List(GENERATE_CAPITAL_LETTERS,GENERATE_SMALL_LETTERS, GENERATE_DIGITS)


        DESTINATION_FOLDER = 'DBTraining-Simulation_based'
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
        process_folder(DESTINATION_FOLDER)

    if GENERATE_VALIDATION_SET:
        print """
        ##############################################################################
        #################   SIMULATION   BASED   TEST    SET   #######################
        ##############################################################################
        """


        elem_to_gen = Generate_Element_List(GENERATE_CAPITAL_LETTERS, GENERATE_SMALL_LETTERS,GENERATE_DIGITS)

        DESTINATION_FOLDER = 'DBTest-Simulation_based'
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
        process_folder(DESTINATION_FOLDER)



