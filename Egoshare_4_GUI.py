#!coding: utf-8
import thread
import os
import time
import wx
import traceback
from PIL import Image

import  wx.lib.newevent
import Break_Egoshare_Captcha


#TRACEBACK
import traceback
import sys
def Myexcepthook(type, value, tb):
        lines=traceback.format_exception(type, value, tb)
        f=open('log.txt', 'a')
        f.write("\n".join(lines))
        f.close()
sys.excepthook=Myexcepthook



MODEL_FOLDER = "Egoshare/Models"
DEFAULT_MODEL_FILE="model.svm"

CAPTCHA_FOLDER = "Egoshare/Rough Captchas"

DEFAULT_CAPTCHA_FILE = "Image011.jpg"



CAPTCHA_WIDTH = 80
CAPTCHA_HEIGHT = 25
PATCH_WIDTH = 20


class MyFrame(wx.Frame):

    def __init__(self, zoom):
        self.zoom = zoom
        self.model = 1
        wx.Frame.__init__(self, None, -1, "Egoshare Captcha Breaker", size=(600, 420))

        taille = (CAPTCHA_WIDTH*zoom, CAPTCHA_HEIGHT*zoom)
        self.image_input_window = wx.StaticBitmap(self, -1, size = taille, bitmap = wx.EmptyBitmap(*taille))
        self.image_input_window.SetMinSize(taille)


        ##CHIFFRE1
        taille = (PATCH_WIDTH*zoom,PATCH_WIDTH*zoom)
        self.image_chiffre1 = wx.StaticBitmap(self, -1, size = taille, bitmap = wx.EmptyBitmap(*taille))
        self.image_chiffre1.SetMinSize(taille)
        self.text_resultat_chiffre1 = wx.StaticText(self, -1, "Resultat")
        self.text_resultat_chiffre1.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.resultat_chiffre1 = wx.StaticText(self, -1)
        self.resultat_chiffre1.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.text_score_chiffre1 = wx.StaticText(self, -1, "Best score")
        self.text_score_chiffre1.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.score_chiffre1 = wx.StaticText(self, -1)
        self.score_chiffre1.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        self.sizer_chiffre1 = wx.GridBagSizer()
        self.sizer_chiffre1.Add(self.image_chiffre1, (1,1), span=(2,1), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.sizer_chiffre1.Add(self.text_resultat_chiffre1, (1,2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.sizer_chiffre1.Add(self.text_score_chiffre1, (1,3), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.sizer_chiffre1.Add(self.resultat_chiffre1, (2,2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.sizer_chiffre1.Add(self.score_chiffre1, (2,3), flag=wx.ALIGN_CENTER | wx.ALL, border=5)


        ##chiffre2
        taille = (PATCH_WIDTH*zoom,PATCH_WIDTH*zoom)
        self.image_chiffre2 = wx.StaticBitmap(self, -1, size = taille, bitmap = wx.EmptyBitmap(*taille))
        self.image_chiffre2.SetMinSize(taille)
        self.text_resultat_chiffre2 = wx.StaticText(self, -1, "Resultat")
        self.text_resultat_chiffre2.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.resultat_chiffre2 = wx.StaticText(self, -1)
        self.resultat_chiffre2.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.text_score_chiffre2 = wx.StaticText(self, -1, "Best score")
        self.text_score_chiffre2.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.score_chiffre2 = wx.StaticText(self, -1)
        self.score_chiffre2.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        self.sizer_chiffre2 = wx.GridBagSizer()
        self.sizer_chiffre2.Add(self.image_chiffre2, (1,1), span=(2,1), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.sizer_chiffre2.Add(self.text_resultat_chiffre2, (1,2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.sizer_chiffre2.Add(self.text_score_chiffre2, (1,3), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.sizer_chiffre2.Add(self.resultat_chiffre2, (2,2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.sizer_chiffre2.Add(self.score_chiffre2, (2,3), flag=wx.ALIGN_CENTER | wx.ALL, border=5)


        ##chiffre3
        taille = (PATCH_WIDTH*zoom,PATCH_WIDTH*zoom)
        self.image_chiffre3 = wx.StaticBitmap(self, -1, size = taille, bitmap = wx.EmptyBitmap(*taille))
        self.image_chiffre3.SetMinSize(taille)
        self.text_resultat_chiffre3 = wx.StaticText(self, -1, "Resultat")
        self.text_resultat_chiffre3.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.resultat_chiffre3 = wx.StaticText(self, -1)
        self.resultat_chiffre3.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.text_score_chiffre3 = wx.StaticText(self, -1, "Best score")
        self.text_score_chiffre3.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.score_chiffre3 = wx.StaticText(self, -1)
        self.score_chiffre3.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        self.sizer_chiffre3 = wx.GridBagSizer()
        self.sizer_chiffre3.Add(self.image_chiffre3, (1,1), span=(2,1), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.sizer_chiffre3.Add(self.text_resultat_chiffre3, (1,2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.sizer_chiffre3.Add(self.text_score_chiffre3, (1,3), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.sizer_chiffre3.Add(self.resultat_chiffre3, (2,2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.sizer_chiffre3.Add(self.score_chiffre3, (2,3), flag=wx.ALIGN_CENTER | wx.ALL, border=5)




        self.main_sizer = wx.GridBagSizer()
        self.main_sizer.Add(self.image_input_window, (1,1), span = (1,2), flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        self.main_sizer.Add(self.sizer_chiffre1, (2,1), flag=wx.ALIGN_CENTER | wx.ALL)
        self.main_sizer.Add(self.sizer_chiffre2, (3,1), flag=wx.ALIGN_CENTER | wx.ALL)
        self.main_sizer.Add(self.sizer_chiffre3, (4,1), flag=wx.ALIGN_CENTER | wx.ALL)



        ## PARTIE DE GAUCHE
        self.sizer_model = wx.FlexGridSizer(rows = 1)
        self.open_image = wx.Bitmap("open.bmp", wx.BITMAP_TYPE_BMP)
        self.text_model = wx.StaticText(self, -1, "Ouvrir le modele")
        self.text_model.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.path_model = wx.TextCtrl(self, -1, size = (100, -1))
        self.path_model.SetEditable(False)
        self.bouton_model = wx.BitmapButton(self, -1, self.open_image)
        self.bouton_model.Bind(wx.EVT_BUTTON, self.OnSelectModel)
        self.sizer_model.Add(self.text_model, flag = wx.ALIGN_CENTER | wx.RIGHT, border = 12)
        self.sizer_model.Add(self.path_model, flag = wx.ALIGN_CENTER)
        self.sizer_model.Add(self.bouton_model, flag = wx.ALIGN_CENTER)

        self.sizer_captcha = wx.FlexGridSizer(rows = 1)
        self.text_captcha = wx.StaticText(self, -1, "Selectionner le captcha")
        self.text_captcha.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.bouton_captcha = wx.BitmapButton(self, -1, self.open_image)
        self.bouton_captcha.Bind(wx.EVT_BUTTON, self.OnSelectCaptcha)
        self.sizer_captcha.Add(self.text_captcha, flag = wx.ALIGN_CENTER | wx.RIGHT, border = 12)
        self.sizer_captcha.Add(self.bouton_captcha, flag = wx.ALIGN_CENTER)

        self.launchButton = wx.Button(self, -1, "Lancer le calcul")
        self.launchButton.Bind(wx.EVT_BUTTON, self.OnLaunch)

        self.sizer_params = wx.FlexGridSizer(cols = 1)
        self.sizer_params.Add(self.sizer_model, flag = wx.ALIGN_CENTER | wx.BOTTOM | wx.UP, border = 3)
        self.sizer_params.Add(self.sizer_captcha, flag = wx.ALIGN_CENTER | wx.BOTTOM | wx.UP, border = 3)
        self.sizer_params.Add(self.launchButton, flag = wx.ALIGN_CENTER | wx.UP, border = 40)


        self.sizer = wx.FlexGridSizer(rows = 1)
        self.sizer.Add(self.sizer_params, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
        self.sizer.Add(self.main_sizer, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)

        self.SetSizer(self.sizer)


        self.Fit()

        self.captcha_selected = False
        self.model_selected = False


        ###############################################################################
        ############################# CREATION EVENEMENTS #############################
        ###############################################################################
        self.SomeNewSetPathLabelEvent, self.EVT_SET_PATH_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(self.EVT_SET_PATH_EVENT, self.OnSetPathLabel)

        self.SomeNewSetCaptchaImageEvent, self.EVT_SET_CAPTCHA_IMAGE_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(self.EVT_SET_CAPTCHA_IMAGE_EVENT, self.OnsetCaptchaImage)

        self.SomeNewSetResultsEvent, self.EVT_SET_RESULTS_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(self.EVT_SET_RESULTS_EVENT, self.OnSetResults)

        self.SomeNewSetThumbsEvent, self.EVT_SET_THUMBS_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(self.EVT_SET_THUMBS_EVENT, self.OnSetThumbs)
        ###############################################################################
        ###############################################################################



###############################################################################
############################# COMPATIBILITE LINUX #############################
###############################################################################
    def setThumbs(self, pil_image1, pil_image2, pil_image3):
        #create the event
        evt = self.SomeNewSetThumbsEvent(image1=self.PIL_to_WX(pil_image1).ConvertToBitmap(),
                                         image2=self.PIL_to_WX(pil_image2).ConvertToBitmap(),
                                         image3=self.PIL_to_WX(pil_image3).ConvertToBitmap())
        #post the event
        wx.PostEvent(self, evt)
    def OnSetThumbs(self, evt):
        self.image_chiffre1.SetBitmap(evt.image1)
        self.image_chiffre2.SetBitmap(evt.image2)
        self.image_chiffre3.SetBitmap(evt.image3)
 ###############################################################################
    def setResults(self, resultat1, score1, resultat2, score2, resultat3, score3, dico1={}, dico2={}, dico3={}):
        #create the event
        evt = self.SomeNewSetResultsEvent(resultat1=resultat1, score1=score1, resultat2=resultat2,
                                          score2=score2, resultat3=resultat3, score3=score3,
                                          dico1=dico1, dico2=dico2, dico3=dico3)
        #post the event
        wx.PostEvent(self, evt)
    def OnSetResults(self, evt):
        self.score_chiffre1.SetLabel(evt.score1)
        self.score_chiffre2.SetLabel(evt.score2)
        self.score_chiffre3.SetLabel(evt.score3)
        self.resultat_chiffre1.SetLabel(evt.resultat1)
        self.resultat_chiffre2.SetLabel(evt.resultat2)
        self.resultat_chiffre3.SetLabel(evt.resultat3)
        
        items1 = evt.dico1.items()
        items1 = map(lambda (a,b) : (b,a), items1)
        items1.sort(reverse=True)
        
        self.score_chiffre1.SetToolTipString("\n".join(map(lambda (b,a) : chr(65+int(a))+" : "+str(b), items1)))
        items2 = evt.dico2.items()
        items2 = map(lambda (a,b) : (b,a), items2)
        items2.sort(reverse=True)
        
        self.score_chiffre2.SetToolTipString("\n".join(map(lambda (b,a) : chr(65+int(a))+" : "+str(b), items2)))
        items3 = evt.dico3.items()
        items3 = map(lambda (a,b) : (b,a), items3)
        items3.sort(reverse=True)
        
        self.score_chiffre3.SetToolTipString("\n".join(map(lambda (b,a) : chr(65+int(a))+" : "+str(b), items3)))
        self.resultat_chiffre1.SetToolTipString("zefzhefzhefz\t:\tzjfgzhegfz\nzefzhefzhefz\t:\tzjfgzhegfz")
 # ###############################################################################
    def setCaptchaImage(self, pil_image):
        #create the event
        evt = self.SomeNewSetCaptchaImageEvent(image=self.PIL_to_WX(pil_image).ConvertToBitmap())
        #post the event
        wx.PostEvent(self, evt)
    def OnsetCaptchaImage(self, evt):
        self.image_input_window.SetBitmap(evt.image)
  ###############################################################################
    def SetPathLabel(self, filename):
        #create the event
        evt = self.SomeNewSetPathLabelEvent(name=filename)
        #post the event
        wx.PostEvent(self, evt)
    def OnSetPathLabel(self, evt):
        self.path_model.SetLabel(evt.name)
###############################################################################
###############################################################################


###############################################################################
########################### EVEMENEMENTS GRAPHIQUES ###########################
###############################################################################
    def OnLaunch(self, evt):
        if not self.captcha_selected:
            wx.MessageBox("Selectionner le Captcha !", "Donnee manquante")
            return
        if not self.model_selected:
            wx.MessageBox("Selectionner le modele SVM !", "Donnee manquante")
            return

        thread.start_new_thread(Break_Egoshare_Captcha.break_captcha,
                                (self.model, self.letter1_algo, self.letter2_algo, self.letter3_algo, self))



    def OnSelectModel(self, evt):
        dlg = wx.FileDialog(self, "Selectionnez le modele", os.path.join(os.getcwd(),MODEL_FOLDER), DEFAULT_MODEL_FILE,
                            wildcard = "Model files (*.svm)|*.svm",
                            style = wx.OPEN)
        retour = dlg.ShowModal()
        self.chemin = dlg.GetPath().encode("latin-1")
        fichier = dlg.GetFilename().encode("latin-1")
        dlg.Destroy()

        if retour == wx.ID_OK and fichier != "":
            self.model = Break_Egoshare_Captcha.load_model(self.chemin, self, fichier)
            self.Update()

            if self.captcha_selected and self.model_selected:
                #Lancement du calcul
                self.OnLaunch(None)




    def OnSelectCaptcha(self, evt):
        dlg = wx.FileDialog(self, "Selectionnez l'image", os.path.join(os.getcwd(), CAPTCHA_FOLDER), DEFAULT_CAPTCHA_FILE,
                            wildcard = "Image files (*.jpg;)|*.jpg",
                            style = wx.OPEN)
        retour = dlg.ShowModal()
        self.chemin = dlg.GetPath().encode("latin-1")
        self.folder = dlg.GetDirectory().encode("latin-1")
        fichier = dlg.GetFilename()
        dlg.Destroy()

        if retour == wx.ID_OK and fichier != "":
            self.beau_captcha, self.letter1, self.letter2, self.letter3, self.letter1_algo, self.letter2_algo, self.letter3_algo = Break_Egoshare_Captcha.preprocess_captcha_part(self.chemin, self.folder, self)
            self.setCaptchaImage(self.beau_captcha)
            self.setThumbs(self.letter1, self.letter2, self.letter3)
            self.captcha_selected = True
            self.setResults("", "", "", "", "", "")

            self.Update()

            if self.captcha_selected and self.model_selected:
                #Lancement du calcul
                self.OnLaunch(None)




###############################################################################
###############################################################################



    def PIL_to_WX(self, pil):
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        data = pil.tostring()
        image.SetData(data)
        return image




class MyApp(wx.App):
    def OnInit(self):
        self.MyFrame = MyFrame(2)
        self.MyFrame.Center(wx.BOTH)
        self.MyFrame.Show()
        return True


app = MyApp(False)

#TRACEBACK
import traceback
import sys
def Myexcepthook(type, value, tb):
        lines=traceback.format_exception(type, value, tb)
##        f=open('log.txt', 'a')
##        f.write("\n".join(lines))
##        f.close()
        wx.MessageBox("\n".join(lines), "Traceback Error")
sys.excepthook=Myexcepthook


app.MainLoop()
