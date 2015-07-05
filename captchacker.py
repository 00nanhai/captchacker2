#!coding: utf-8
import os, time
import shutil

from PIL import Image
from svm import *
from svmutil import *
from break_captcha_utils import *
import characters_generate_captcha_db 
import characters_generate_simulation_db
import characters_train_test_SVM
class captchacker:
    def __init__(self):
        self.mode = 0
        self.dst_folder = "tmp"
        self.svm_model_files = "models/captcha_based_TR=687_TEST=143_C=1000_KERNEL=1.svm"
        self.model = None
        self.split_mode = 0
        self.color = 0
        self.image_file = 0
        self.gray_im = 0

    def set_mode(self, mode):
        self.mode = mode
        return
    def set_svm_model(self, model_files):
        self.svm_model_files = model_files
        return
    def load_svm_models(self):
        if not os.path.isfile(self.svm_model_files):
            print 'The specified model file: \"'+self.svm_model_files +'\" was not found. Aborting.'
            sys.exit(1)
        else:
            print "####################################################################################"
            print "\tLoading model ", self.svm_model_files
            print "####################################################################################"
            self.model = svm_load_model(self.svm_model_files)
            print "Model successfully loaded."
        return
    def set_image(self,image_file):
        self.image_file = image_file
        return 
    def set_de_noise(self, mode):
        return 
    def set_color_filter(self, color):
        return 
    def set_split_mode(self, mode):
        return
    def clear_lines(self):
        return
    def get_result(self):
        self.load_svm_models()
        letters_path = preprocess_captcha_part(self.image_file)
        values,prob,predictions_detail = break_captcha(self.model, letters_path)

        new_filename = values+".jpg"
        while os.path.isfile(os.path.join(self.dst_folder, new_filename)):
            new_filename = new_filename[:-4]+"_"+new_filename[-4:]
        print "Changement file name:  ", new_filename
        shutil.copyfile(self.image_file,os.path.join(self.dst_folder, new_filename))

        return values,prob,predictions_detail
    def train_model(self):
        return

    def generate_simulation_base(self,GENERATE_TRAINING_SET = False,GENERATE_VALIDATION_SET = False,
        GENERATE_CAPITAL_LETTERS = False,GENERATE_SMALL_LETTERS = False, GENERATE_DIGITS = False):
        characters_generate_simulation_db.generate_simulation_base(GENERATE_TRAINING_SET,GENERATE_VALIDATION_SET,GENERATE_CAPITAL_LETTERS,GENERATE_SMALL_LETTERS,GENERATE_DIGITS )
        return
    def generate_simulation_based_model(self,KERNEL = SIGMOID,TRAINING_FOLDER = 'DBTraining-Simulation_based'):
        model_file = characters_train_test_SVM.generate_simulation_based_model()
        return model_file

    def generate_captcha_base(self,GENERATE_TRAINING_SET = False,GENERATE_VALIDATION_SET = False):
        characters_generate_captcha_db.generate_captcha_base(GENERATE_TRAINING_SET,GENERATE_VALIDATION_SET,GENERATE_COMPUTER_LABELLED_SET)
        return
    def generate_captcha_based_model(self,KERNEL = POLY,TRAINING_FOLDER = 'DBTraining-Captcha_based'):
        model_file = characters_train_test_SVM.generate_captcha_based_model()
        return model_file

    def test_based_model(self,MODEL_FILE,TEST_FOLDER = 'DBTest-Simulation_based'):
        characters_train_test_SVM.test_based_model(MODEL_FILE,TEST_FOLDER = 'DBTest-Simulation_based')
        return






