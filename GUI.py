#!coding: utf-8
import thread
import os
import time
import wx
import traceback
from PIL import Image

import  wx.lib.newevent


import Break_Captcha_util
import Hotmail_5_ComputeScores


WIDTH=31

class MyFrame(wx.Frame):

    def __init__(self, zoom):
        self.zoom = 2
        self.model = 1
        wx.Frame.__init__(self, None, -1, "CaptcHacker", size=(600, 420))

        taille = (WIDTH*zoom,31*zoom)
        self.image_input_window = wx.StaticBitmap(self, -1, size = taille, bitmap = wx.EmptyBitmap(*taille))
        self.image_input_window.SetMinSize(taille)

        self.text_resultat = wx.StaticText(self, -1, "Resultat :")
        self.text_resultat.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.resultat = wx.StaticText(self, -1)
        self.resultat.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.text_score = wx.StaticText(self, -1, "Best score :")
        self.text_score.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.score = wx.StaticText(self, -1)
        self.score.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        self.res = wx.StaticText(self, -1)
        self.res.SetFont(wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        self.main_sizer = wx.GridBagSizer()
        self.main_sizer.Add(self.image_input_window, (1,1), span = (2,1), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.main_sizer.Add(self.text_resultat, (1,2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.main_sizer.Add(self.resultat, (1,3), flag=wx.ALIGN_CENTER | wx.ALL, border=0)
        self.main_sizer.Add(self.text_score, (2,2), flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.main_sizer.Add(self.score, (2,3), flag=wx.ALIGN_CENTER | wx.ALL, border=0)

        taille = (127*zoom,31*zoom)
        self.image_input_window_orig = wx.StaticBitmap(self, -1, size = taille, bitmap = wx.EmptyBitmap(*taille))
        self.image_input_window_orig.SetMinSize(taille)

        self.graph_image = wx.EmptyImage(127,31)
        self.image_graph_window_orig = wx.StaticBitmap(self, -1, size = taille) #, bitmap = self.graph_bitmap)
        self.image_graph_window_orig.SetMinSize(taille)

        self.sizer_algo = wx.FlexGridSizer(cols = 1)
        self.sizer_algo.Add(self.image_input_window_orig, flag = wx.ALIGN_CENTER | wx.ALL, border= 5)
        self.sizer_algo.Add(self.main_sizer)
        self.sizer_algo.Add(self.image_graph_window_orig, flag = wx.ALIGN_CENTER | wx.ALL, border = 10)
        self.sizer_algo.Add(self.res, flag = wx.ALIGN_CENTER | wx.BOTTOM, border = 7 )



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

        self.sizer_width = wx.FlexGridSizer(rows = 1)
        self.text_width = wx.StaticText(self, -1, "Largeur de fenetre")
        self.text_width.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.width_picker = wx.SpinCtrl(self, size = (50, -1), max=WIDTH)
        self.width_picker.SetValue(16)
        self.sizer_width.Add(self.text_width, flag = wx.ALIGN_CENTER | wx.RIGHT, border = 12)
        self.sizer_width.Add(self.width_picker, flag = wx.ALIGN_CENTER)

        self.launchButton = wx.Button(self, -1, "Lancer l'animation")
        self.launchButton.Bind(wx.EVT_BUTTON, self.OnLaunch)

        self.launchPredictionButton = wx.Button(self, -1, "Lancer la prediction")
        self.launchPredictionButton.Bind(wx.EVT_BUTTON, self.OnLaunchPrediction)

        self.sizer_params = wx.FlexGridSizer(cols = 1)
        self.sizer_params.Add(self.sizer_model, flag = wx.ALIGN_CENTER | wx.BOTTOM | wx.UP, border = 3)
        self.sizer_params.Add(self.sizer_captcha, flag = wx.ALIGN_CENTER | wx.BOTTOM | wx.UP, border = 3)
        self.sizer_params.Add(self.sizer_width, flag = wx.ALIGN_CENTER | wx.BOTTOM | wx.UP, border = 3)
        self.sizer_params.Add(self.launchButton, flag = wx.ALIGN_CENTER | wx.UP, border = 40)
        self.sizer_params.Add(self.launchPredictionButton, flag = wx.ALIGN_CENTER | wx.UP, border = 40)


        self.sizer = wx.FlexGridSizer(rows = 1)
        self.sizer.Add(self.sizer_params, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
        self.sizer.Add(self.sizer_algo, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)

        self.SetSizer(self.sizer)


        self.Fit()

        self.captcha_selected = False
        self.model_selected = False
        self.actif = False


        ###############################################################################
        ############################# CREATION EVENEMENTS #############################
        ###############################################################################
        self.SomeNewSetPathLabelEvent, self.EVT_SET_PATH_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(self.EVT_SET_PATH_EVENT, self.OnSetPathLabel)

        self.SomeNewSetCaptchaImageEvent, self.EVT_SET_CAPTCHA_IMAGE_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(self.EVT_SET_CAPTCHA_IMAGE_EVENT, self.OnsetCaptchaImage)

        self.SomeNewSetGraphImageEvent, self.EVT_SET_GRAPH_IMAGE_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(self.EVT_SET_GRAPH_IMAGE_EVENT, self.OnSetGraphImage)

        self.SomeNewSetResultEvent, self.EVT_SET_RESULT_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(self.EVT_SET_RESULT_EVENT, self.OnSetResult)

        self.SomeNewSetRGBEvent, self.EVT_SET_RGB_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(self.EVT_SET_RGB_EVENT, self.OnSetRGB)
        ###############################################################################
        ###############################################################################



###############################################################################
############################# COMPATIBILITE LINUX #############################
###############################################################################
    def SetRGB(self, pos1, pos2):
        #create the event
        evt = self.SomeNewSetRGBEvent(pos1 = pos1, pos2 = pos2)
        #post the event
        wx.PostEvent(self, evt)
    def OnSetRGB(self, evt):
        self.graph_image.SetRGB(evt.pos1, evt.pos2, 255, 0, 0)
 ###############################################################################
    def setResult(self, pil_image, resultat, score_in):
        #create the event
        evt = self.SomeNewSetResultEvent(image=self.PIL_to_WX(pil_image).ConvertToBitmap(), result = resultat, score = score_in)
        #post the event
        wx.PostEvent(self, evt)
    def OnSetResult(self, evt):
        self.image_input_window.SetBitmap(evt.image)
        self.resultat.SetLabel(str(evt.result))
        self.score.SetLabel(str(evt.score))
 ###############################################################################
    def SetGraphImage(self, image):
##        imag1 = image.Copy()
##        #create the event
##        evt = self.SomeNewSetGraphImageEvent(image=imag1.Rescale(self.zoom*127, self.zoom*31).ConvertToBitmap())
##        #post the event
##        wx.PostEvent(self, evt)

        #create the event
        imag1 = self.PIL_to_WX(image)
        #imag1 = self.PIL_to_WX(self.captcha.convert("RGB"))
        evt = self.SomeNewSetGraphImageEvent(image=imag1.ConvertToBitmap())
        #post the event
        wx.PostEvent(self, evt)
        self.launchPredictionButton.SetLabel("Lancer le calcul")

    def OnSetGraphImage(self, evt):
        self.image_graph_window_orig.SetBitmap(evt.image)
        #self.image_graph_window_orig.Update()
        self.Update()
        #self.Fit()
 ###############################################################################
    def setCaptchaImage(self, pil_image):
        #create the event
        evt = self.SomeNewSetCaptchaImageEvent(image=self.PIL_to_WX(pil_image).ConvertToBitmap())
        #post the event
        wx.PostEvent(self, evt)
        self.Fit()
        self.Update()
    def OnsetCaptchaImage(self, evt):
        self.image_input_window_orig.SetBitmap(evt.image)
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
        if not self.actif:
            if not self.captcha_selected:
                wx.MessageBox("Selectionner le Captcha !", "Donnee manquante")
                return
            if not self.model_selected:
                wx.MessageBox("Selectionner le modele SVM !", "Donnee manquante")
                return

            self.actif = not self.actif
            self.launchButton.SetLabel("Arreter le calcul")
            thread.start_new_thread(Break_Captcha_util.break_captcha, (self.model, self.captcha, self.width_picker.GetValue(), self, self.graph_image))
        else:
            self.launchButton.SetLabel("Relancer le calcul")
            self.graph_image = wx.EmptyImage(127,31)
            self.actif = not self.actif

    def OnLaunchPrediction(self, evt):
        if not self.actif:
            if not self.captcha_selected:
                wx.MessageBox("Selectionner le Captcha !", "Donnee manquante")
                return
            if not self.model_selected:
                wx.MessageBox("Selectionner le modele SVM !", "Donnee manquante")
                #return

            self.actif = not self.actif
            self.launchPredictionButton.SetLabel("Arreter le calcul")
            thread.start_new_thread(Hotmail_5_ComputeScores.get_prediction, (self.model, self.captcha, self))
        else:
            self.launchPredictionButton.SetLabel("Relancer le calcul")
            self.graph_image = wx.EmptyImage(127,31)
            self.actif = not self.actif




    def OnSelectModel(self, evt):
        dlg = wx.FileDialog(self, "Selectionnez le modele", os.path.join(os.getcwd(),MODEL_FOLDER), DEFAULT_MODEL_FILE,
                            wildcard = "Model files (*.svm)|*.svm",
                            style = wx.OPEN)
        retour = dlg.ShowModal()
        self.chemin = dlg.GetPath().encode("latin-1")
        fichier = dlg.GetFilename().encode("latin-1")
        dlg.Destroy()

        if retour == wx.ID_OK and fichier != "":
            self.model = Break_Captcha_util.load_model(self.chemin, self, fichier)
        self.Update()



    def OnSelectCaptcha(self, evt):
        dlg = wx.FileDialog(self, "Selectionnez l'image", os.path.join(os.getcwd(), CAPTCHA_FOLDER), DEFAULT_CAPTCHA_FILE,
                            wildcard = "Image files (*.jpg;)|*.jpg",
                            style = wx.OPEN)
        retour = dlg.ShowModal()
        self.chemin = dlg.GetPath().encode("latin-1")
        fichier = dlg.GetFilename()
        dlg.Destroy()

        if retour == wx.ID_OK and fichier != "":
            self.captcha, self.beau_captcha = Break_Captcha_util.preprocess_captcha_part(self.chemin, self)
            self.setCaptchaImage(self.beau_captcha)
            self.captcha_selected = True
        self.Update()
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
