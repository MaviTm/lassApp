import sys
import os
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * #QSize, QPoint
from PyQt5.QtGui import * #QIcon, QPixmap

class myWin(QWidget):

    uygulama = QApplication(sys.argv)

    def __int__(self):
        super().__int__()
        self.myWinApp()

    def myWinApp(self):
        return self

    #########################################################
    # SET METHODS
    #########################################################

    def winResize(self, en=640, boy=480):
        self.resize(QSize(en, boy))
        return self

    def winMove(self, x=300, y=300):
        self.move(QPoint(x, y))
        return self

    def winTitle(self, str='Form Name'):
        self.setWindowTitle(str)
        return self

    def winIcon(self,imgPath = None):
        if imgPath is None or os.path.exists(imgPath) != True or os.access(imgPath, os.R_OK):
            return self
        self.setWindowIcon(QIcon(imgPath))
        return self

    #########################################################
    # GET METHODS
    #########################################################

    def getWinResize(self, out='a'):
        if out == 'w' or out == 'width':
            return self.width()
        elif out == 'h' or out == 'height':
            return self.height()

        return [self.width(), self.height()]

    def getWinMove(self, out='a'):
        if out == 'x' or out == 'horizontal':
            return self.x()
        elif out == 'y' or out == 'vertical':
            return self.y()

        return [self.x(), self.y()]

    #########################################################
    # VİEWER METHODS
    #########################################################

    def winHeadText(self, str=''):
        self.layout = QVBoxLayout()
        label = QLabel('<p style="font-size: 22px; text-align:center;">'+str+'</p>', self)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)
        self.setLayout(self.layout)
        return self

    #########################################################
    # EVENTS METHODS
    #########################################################

    def winShow(self):
        #before trigger
        self.show();
        #after trigger
        myWin.uygulama.exec_()
        return self

    def winClose(self):
        #before tirgger
        self.close()
        #after trigger


class myForm(QWidget):
    def __int__(self):
            super().__int__()
            self.myWin = None
            self.jdata = {}
            self.fobj = {"a":None}

    def pencereSet(self, wind):
        self.myWin = wind
        return self

    def elemanSet(self, name, obj):
        self.fobj[name] = obj
        return self
    def elemanGet(self, name, obj):
        return self.fobj[name]

    def jsonUrlData(self, url):
        from urllib.request import urlopen
        try:
            response = urlopen(url)
            content = response.readall().decode("utf-8")
            data = json.loads(content)
            self.setFormJson(data)
        except:
            self.jdata.clear()
        return self

    def setFormJson(self, jSonData):
        """
        print(json.dumps(elemanlar.jdata, sort_keys=True, indent=4, separators=(',', ': ')))
        """
        self.jdata = jSonData

        if len(self.jdata['elemanlar']) > 0:
            for i in self.jdata['elemanlar']:
                if type(self.jdata['elemanlar'][i]) is list:
                    a = 2


        return self

    def formVizard(self):

        layaut = QGridLayout(self.myWin)

        if len(self.jdata['elemanlar']) < 1:
            return self
        x = 0
        for i in self.jdata['elemanlar']:
            rindex = "row"+str(x)
            #sıralama işlemi
            cx = 0 #y
            xx = 0 #x
            for z in self.jdata['elemanlar'][rindex]:
                zx = "a"+str(xx)
                try:
                    self.jdata['elemanlar'][rindex][zx]['obj'] = self.formElemanGet(self.jdata['elemanlar'][rindex][zx])
                    layaut.addWidget(self.jdata['elemanlar'][rindex][zx]['obj'], x, cx, self.jdata['elemanlar'][rindex][zx]['row'], self.jdata['elemanlar'][rindex][zx]['col'])
                    print(x, cx, self.jdata['elemanlar'][rindex][zx]['row'], self.jdata['elemanlar'][rindex][zx]['col'], self.jdata['elemanlar'][rindex][zx]['name'])
                    cx += 1
                except:
                    continue
                xx += 1
            x += 1

    def formElemanGet(self, aktifDict):
        if aktifDict['type'] == "textLabel":
            return self.textLabel(aktifDict)
        elif aktifDict['type'] == "htmlLabel":
            return self.htmlLabel(aktifDict)
        elif aktifDict['type'] == "inputText" or aktifDict['type'] == "inputReadonly" or aktifDict['type'] == "inputPassword":
            return self.inputText(aktifDict)
        elif aktifDict['type'] == "inputSelect":
            return self.inputSelect(aktifDict)

    def textLabel(self, dict):
        lbl = QLabel(self.myWin)
        lbl.setText(dict['value'])
        return lbl

    def htmlLabel(self,dict):
        return QLabel(dict['value'], self.myWin)

    def inputText(self, dict):
        lineEdit = QLineEdit(self.myWin)
        try:
            lineEdit.setPlaceholderText(dict['placeholder'])
        except:
            lineEdit.setPlaceholderText('')
        if dict['type'] == "inputPassword":
            lineEdit.setEchoMode(QLineEdit.Password)
        elif dict['type'] == "inputReadonly":
            lineEdit.setReadOnly(True)
        return lineEdit


    def inputSelect(self, opt):
        combo = QComboBox(self.myWin)
        try:
            values = opt['value']
        except:
            return combo

        try:
            selected = opt['selected']
        except:
            selected = None
        if type(values) is dict:
            for i in values:
                try:
                    combo.addItem(values[i], i)
                except (TypeError, AttributeError) as Hata:
                    print(opt['name'], " combobox ", i, values[i], "Eklenemedi", Hata)
                except:
                    print(opt['name'], " combobox ", i, values[i], "Eklenemedi", sys.exc_info()[0])

        try:
            value = values[selected]
            index = combo.findData(value)
            combo.setCurrentIndex(index)
        except:
            return combo

        return combo