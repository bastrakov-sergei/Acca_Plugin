#!/usr/bin/env python
#This file is part of Acca plugin.

#    Acca plugin is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Acca plugin is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Acca plugin.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import resources
import sys
import os
import tempfile
import threading
import time
import toar
from main_form import Ui_Dialog
from progress_form import Ui_progress_dialog
from __init__ import name
from toar import *
from acca import *

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
        self.main = Ui_Dialog()
        self.main.setupUi(self.window)
        self.main.btnOk.clicked.connect(self.btnOkClick)
        self.main.btnCancel.clicked.connect(self.btnCancelClick)
        self.main.btnOpenMetafile.clicked.connect(self.btnOpenMetafileClick)
        self.main.btnOpenMaskfile.clicked.connect(self.btnOpenMaskfileClick)
        self.main.btnOpenTmpfolder.clicked.connect(self.btnOpenTmpfolderClick)
        self.main.chkDefault.stateChanged.connect(self.chkDefaultChange)
        self.useDefault=True
        self.main.txtTmpfolder.setText(tempfile.gettempdir())
        self.window.exec_()

    def btnOkClick(self):
        self.metafile=self.main.txtMetafile.text().toUtf8().data()
        self.tmpfolder=self.main.txtTmpfolder.text().toUtf8().data()
        self.maskfile=self.main.txtMaskfile.text().toUtf8().data()
        self.shadows=self.main.chkShadows.isChecked()
        self.cloud=self.main.chkCloud.isChecked()
        self.single_pass=self.main.chkPass.isChecked()
        self.toar=CToar(self.metafile,self.tmpfolder,1,None)
        QObject.connect(self.toar, SIGNAL("progress(int, int, float)"),self.updateProgress,Qt.QueuedConnection)
        QObject.connect(self.toar, SIGNAL("finished()"),self.toarDone)
        self.window.close()
        self.progressWindow = QDialog()
        self.progressWindow.setWindowTitle("Progress")
        self.slave = Ui_progress_dialog()
        self.slave.setupUi(self.progressWindow)
        self.toar.start()
        self.progressWindow.exec_()

    def toarDone(self):
        self.new_metafile=os.path.join(self.tmpfolder,os.path.basename(self.metafile))
        self.acca=CAcca(self.new_metafile,self.maskfile,1,self.shadows,self.cloud,self.single_pass,None)
        QObject.connect(self.acca, SIGNAL("progress(int, int, float)"),self.updateProgress, Qt.QueuedConnection)
        QObject.connect(self.acca, SIGNAL("finished()"), self.accaDone)
        self.acca.start()

    def accaDone(self):
        self.progressWindow.close()

    def btnCancelClick(self):
        self.window.close()

    def btnOpenMetafileClick(self):
        self.main.txtMetafile.setText(QFileDialog.getOpenFileName(None,"Open Metafile",self.main.txtMetafile.text(), "Metafile (*.txt);; Other (*)",))

    def btnOpenMaskfileClick(self):
        self.main.txtMaskfile.setText(QFileDialog.getSaveFileName(None,"Save mask file",self.main.txtMaskfile.text(), "TIFF Image (*.tif)"))

    def btnOpenTmpfolderClick(self):
        self.main.txtTmpfolder.setText(QFileDialog.getExistingDirectory(None,"Select temp folder",self.main.txtTmpfolder.text()))

    def chkDefaultChange(self):
        self.useDefault=self.main.chkDefault.isChecked()
        self.main.lblTmpfolder.setEnabled(not self.main.chkDefault.isChecked())
        self.main.txtTmpfolder.setEnabled(not self.main.chkDefault.isChecked())
        self.main.btnOpenTmpfolder.setEnabled(not self.main.chkDefault.isChecked())

    def updateProgress(self,i,step,stat):
        if (i==0):
            self.slave.lblStatus.setText("Toar: step {0} of 5".format(step+1))
        else:
            self.slave.lblStatus.setText("Acca: step {0} of 2".format(step))
        self.slave.prBar.setValue(stat)
