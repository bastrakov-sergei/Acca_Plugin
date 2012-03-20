from PyQt4.QtCore import *
from PyQt4.QtGui import *
import osgeo.gdal as gdal
import resources
import sys
import tempfile
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
#        QObject.connect(self.ui.chkDefault, SIGNAL("stateChanged()"), self.chkFDefault)
        self.ui.chkDefault.stateChanged.connect(self.chkFDefault)
        self.tmpdir="/tmp"
        self.window.exec_()

    def chkFDefault(self):
        self.tmpDefault=self.ui.chkDefault.isChecked()
        self.ui.txtTmpPath.setEnabled(not self.tmpDefault)
        self.ui.btnTmpPath.setEnabled(not self.tmpDefault)

    def btnFGo(self):
        self.tmpmask=toar.main((self.metafile,self.tmpdir))
        acca_mask.main((self.tmpmask,self.maskfile))
        self.window.close()

    def btnFInPath(self):
        self.metafile = QFileDialog.getOpenFileName(None, "Open Metafile", QDir.currentPath(), "Metafile (*.txt *.txt);; Other (*)").toUtf8().data()
        self.ui.txtInPath.setText(self.metafile)

    def btnFOutPath(self):
        self.maskfile = QFileDialog.getSaveFileName(None, "Save mask file", QDir.currentPath(), "TIFF Image (*.tif)").toUtf8().data()
        self.ui.txtOutPath.setText(self.maskfile)

    def btnFTmpPath(self):
        self.tmpdir = QFileDialog.getExistingDirectory(None, "Select temp folder", tempfile.gettempdir()).toUtf8().data()
        self.ui.txtTmpPath.setText(self.tmpdir)
