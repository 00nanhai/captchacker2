#!coding: utf-8
import Break_Captcha_util
import pickle
import os
from PIL import Image
import math

#import psyco
#psyco.full()

#TRACEBACK
import traceback
import sys
def Myexcepthook(type, value, tb):
        lines=traceback.format_exception(type, value, tb)
        f=open('log.txt', 'a')
        f.write("\n".join(lines))
        f.close()
sys.excepthook=Myexcepthook



def compute_scores_list(model, captcha, parent=None):
        #Liste des scores
        liste_scores = []

        #Compute scores for all widths and starting positions
        for size in range(8, 30, 1):
            print size, "/", 30
            for starting_pos in range(0, captcha.size[0] - size):
                preprocessed_captcha_part = captcha.crop((starting_pos, 0, starting_pos+size, 31))


                #Si parent=None, on enl�ve le blanc sur les cot�s
                miny=100000
                maxy=0
                for i in xrange(size):
                    for j in xrange(31):
                        if preprocessed_captcha_part.getpixel((i,j)) == 0:
                            if j<miny:
                                miny=j
                            if j>maxy:
                                maxy=j
                preprocessed_captcha_part = preprocessed_captcha_part.crop((0, miny, size, maxy+1))
                sizei = maxy-miny+1

                im = Image.new('L', (31, 31), 1)
                im.paste(preprocessed_captcha_part, ((31-size)/2, (31-sizei)/2))

                prediction, max_score = Break_Captcha_util.predict(model, im, None, 0)
                #liste_scores.append((starting_pos+size, size, 1/(1-max_score), prediction))
                liste_scores.append((starting_pos+size, size, math.log(max_score), prediction))


        if not parent:
            f=open('scores.pck', 'w')
            pickle.dump(liste_scores, f)
            f.close()

        return liste_scores





def use_dynamic_programming(liste_scores):
    liste_scores.sort()

    #Max scores at ending point
    posmax = 0
    sizes = set([])
    d = {}
    for (pos, size, score, prediction) in liste_scores:
        d[pos] = {0 : [[], [], -10000],
                  1 : [[], [], -10000],
                  2 : [[], [], -10000],
                  3 : [[], [], -10000],
                  4 : [[], [], -10000],
                  5 : [[], [], -10000],
                  6 : [[], [], -10000]}
        sizes.add(size)
        if pos>posmax:
            posmax=pos

    d[0] = {0 : [[], [], 0],
          1 : [[], [], 0],
          2 : [[], [], 0],
          3 : [[], [], 0],
          4 : [[], [], 0],
          5 : [[], [], 0],
          6 : [[], [], 0]}

    sizes = list(sizes)
    sizes.sort()

    sizemax = sizes[-1]


    for (pos, size, score, prediction) in liste_scores:
        #Pour mettre � jour le plus haut score, il faut que:
        #- le score de l'intervalle consid�r� soit plus grand que le score courant (LE PLUS HAUT SCORE)
        #- il y ait une entr�e dans le dico correspondant au d�but de l'intervalle consid�r� (LES INTERVALLES SE TOUCHENT)
        #- l'intervalle consid�r�

        if d.has_key(pos-size):
            #Trajectoires pr�c�dentes
            precedent = d[pos-size]

            #Rajout de la trajectoire consid�r� � la pr�c�dente
            for [sommets, predicts, old_score] in precedent.values():
                path_length_old = len(predicts)

                #print 'path_length_old: ', path_length_old
                if path_length_old < 6:
                    if d[pos][path_length_old+1][2] < old_score + score:
                        d[pos][path_length_old+1] = [sommets+[pos], predicts+[prediction], old_score+score]

    ##        print "append at ", pos,
    ##        raw_input()

            del precedent


    segs, preds, score = d[posmax][6]

    print
    print "##########################"
    print " Programmation dynamique: "
    print "##########################"
    print "Segmentation: ", segs
    print "Prediction: ", "".join(preds)
    print "Score total: ", score

    return "".join(preds), segs



def get_prediction(model, captcha, parent):
    print
    print "Computing scores..."
    liste_scores = compute_scores_list(model, captcha, parent=None)
    print "Done."
    print

    print "Solving optimization problem..."
    preds, segs = use_dynamic_programming(liste_scores)
    print "Done."
    print

    #Pr�diction
    parent.res.SetLabel(preds)

    #Image segment�e
    segmented_captcha = parent.beau_captcha.convert("RGB")
    h = segmented_captcha.size[1]
    for x in segs:
        for y in xrange(0, h):
            segmented_captcha.putpixel((x*parent.zoom, y), (255,0,0))

    parent.SetGraphImage(segmented_captcha)
    parent.actif = False
    parent.launchPredictionButton.SetLabel("Lancer la pr�diction")



if __name__ == "__main__":
        MODEL_FILE = "Hotmail/Models/model_31x31_3DE2MT_DXDY.svm"
        #MODEL_FILE = "Hotmail/Models/model_31x31_3DE2MT_classes.svm"
        CAPTCHA_FILE = os.path.join("Hotmail", "Rough Captchas", 'Image011.jpg')

        #Chargement du mod�le
        model = Break_Captcha_util.load_model(MODEL_FILE)

        #Pr�processing du captcha
        captcha, beau_captcha = Break_Captcha_util.preprocess_captcha_part(CAPTCHA_FILE)

        #Calcul des scores
        liste_scores = compute_scores_list(model, captcha)

        #Chargement des scores sauvegard�s
##        f=open('scores.pck')
##        liste_scores = pickle.load(f)
##        f.close()
        use_dynamic_programming(liste_scores)

        raw_input()
