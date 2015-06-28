#!coding: utf-8
import pickle
#import psyco
#psyco.full()

#Chargement des scores sauvegard�s
f=open('scores.pck')
liste_scores = pickle.load(f)
f.close()

liste_scores.sort()

#Max scores at ending point
posmax = 0
sizes = set([])
d = {}
for (pos, size, score, prediction) in liste_scores:
    d[pos] = {0 : [[], [], 0],
              1 : [[], [], 0],
              2 : [[], [], 0],
              3 : [[], [], 0],
              4 : [[], [], 0],
              5 : [[], [], 0],
              6 : [[], [], 0]}
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

    #print "position consid�r�e", pos


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




####ESSAI CHRONOLOGIQUE
##POSITION = 0
##pred = ""
##while POSITION != posmax:
##    l=[(score, size, pos, prediction) for (pos, size, score, prediction) in liste_scores if pos-size==POSITION]
##    #print l
##    l.sort(reverse=True)
##    print l[:2]
##    (score, size, pos, prediction) = l[0]
##    pred += prediction
##    POSITION += size
##
##print
##print "######################"
##print " Essai chronologique: "
##print "######################"
##print "Prediction: ", pred



##VRAIE COUPE
print
print "##############"
print " Vraie coupe: "
print "##############"
aretes_good = [0, 11, 28, 38, 51, 79, posmax]
#aretes_good = [0, 16, 30, 45, 70, 83, posmax]

l=[]
for index, elem in enumerate(aretes_good[1:]):
    l.append((aretes_good[index], aretes_good[index+1]))
aretes_good = l


SCORE = 0
pred = ""
for beg, fin in aretes_good:
    print beg, fin
    [(pos, size, score, prediction)] = [(pos, size, score, prediction) for (pos, size, score, prediction) in liste_scores if pos == fin and pos-size==beg]
    print prediction, score
    SCORE += score
    pred += prediction

print
print "Prediction: ", pred
print "Score total: ", SCORE
