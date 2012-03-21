from PyQt4.QtCore import *
from PyQt4.QtGui import *
import osgeo.gdal as gdal
import resources
import sys
import tempfile
import threading
import time
import toar
import acca_mask
from form import Ui_Dialog
from __init__ import name

class Acca_Plugin:

    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction(QIcon(":/plugins/000_testplugin/icon.png"), "Acca plugin", self.iface.mainWindow())
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Acca plugin", self.action)

    def unload(self):
        self.iface.removePluginMenu("&Acca plugin", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        self.window = QDialog()
        self.window.setWindowTitle("Acca");
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.window)

        QObject.connect(self.ui.btnGo, SIGNAL("clicked()"), self.btnFGo)
        QObject.connect(self.ui.btnInPath, SIGNAL("clicked()"), self.btnFInPath)
        QObject.connect(self.ui.btnOutPath, SIGNAL("clicked()"), self.btnFOutPath)
        QObject.connect(self.ui.btnTmpPath, SIGNAL("clicked()"), self.btnFTmpPath)
        self.ui.progressBar.setEnabled(False)
        self.ui.chkDefault.stateChanged.connect(self.chkFDefault)
        self.tmpdir="/tmp"
        self.window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.window.setFixedSize(self.window.width(), self.window.height())
        self.ui.secondW.setVisible(False)
        self.window.exec_()

    def chkFDefault(self):
        self.tmpDefault=self.ui.chkDefault.isChecked()
        self.ui.txtTmpPath.setEnabled(not self.tmpDefault)
        self.ui.btnTmpPath.setEnabled(not self.tmpDefault)

    def runAcca(self):
        self.tmpmask=toar.main((self.metafile,self.tmpdir),self.state)
        acca_mask.main((self.tmpmask,self.maskfile),self.state)

    def btnFGo(self):
        self.metafile=self.ui.txtInPath.text().toUtf8().data()
        self.tmpdir=self.ui.txtTmpPath.text().toUtf8().data()
        self.maskfile=self.ui.txtOutPath.text().toUtf8().data()
        self.state=[0,0,0]
        shPr=threading.Thread(target=self.runAcca)
        shPr.daemon=True
        shPr.start()
        self.ui.mainW.setVisible(False)
        self.ui.secondW.setVisible(True)
        while (shPr.isAlive()):
            if (self.state[0]==0):
                self.ui.lblStatus.setText("Toar step {0}".format(self.state[1]))
            else:
                self.ui.lblStatus.setText("Acca running")
            self.ui.progressBar.setValue(self.state[2])
        self.window.close()

    def btnFInPath(self):
        self.ui.txtInPath.setText(QFileDialog.getOpenFileName(None, "Open Metafile", QDir.currentPath(), "Metafile (*.txt *.txt);; Other (*)").toUtf8().data())

    def btnFOutPath(self):
        self.ui.txtOutPath.setText(QFileDialog.getSaveFileName(None, "Save mask file", QDir.currentPath(), "TIFF Image (*.tif)").toUtf8().data())

    def btnFTmpPath(self):
        self.ui.txtTmpPath.setText(QFileDialog.getExistingDirectory(None, "Select temp folder", tempfile.gettempdir()).toUtf8().data())
