#!coding: utf-8
import os, time

MODEL_FILE = "Egoshare/Models/captcha_based_TR=687_TEST=143_C=1000_KERNEL=1.svm"

TRAINING_FOLDER = "Egoshare/Labelled Catpchas Training"
TEST_FOLDER = "Egoshare/Labelled Catpchas Test"
DEST_FOLDER = "Egoshare/Rough Captchas"

from Egoshare_1_GetCaptchas import save_image
from Break_Egoshare_Captcha import load_model, preprocess_captcha_part, break_captcha

model = load_model(MODEL_FILE)
print

for i in range(1000):
    file = save_image(path = os.path.join(DEST_FOLDER, "0"))
    
    letter1_algo, letter2_algo, letter3_algo = preprocess_captcha_part(file)
    prediction = break_captcha(model, letter1_algo, letter2_algo, letter3_algo)

    new_filename = prediction+".jpg"
    #On ne veut pas que le fichier ait le meme nom qu'un fichier déjà présent dans le dossier de training ou de destination
    # (pour pouvoir faire ensuite un copier-coller sans conflit)
    
    while os.path.isfile(os.path.join(DEST_FOLDER, new_filename)) or os.path.isfile(os.path.join(TRAINING_FOLDER, new_filename)) or os.path.isfile(os.path.join(TEST_FOLDER, new_filename)):
        new_filename = new_filename[:-4]+"_"+new_filename[-4:]
        print "Changement de nom: ", new_filename

    os.rename(file, os.path.join(DEST_FOLDER, new_filename))
    print new_filename
    
    time.sleep(1)
    
raw_input()