# -*- coding: utf-8 -*-

#    This file is part of Acca plugin.

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

# Form implementation generated from reading ui file 'main_form.ui'
#
# Created: Thu May 10 22:51:21 2012
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(583, 208)
        self.gridLayoutWidget = QtGui.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 0, 566, 201))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lblMetafile = QtGui.QLabel(self.gridLayoutWidget)
        self.lblMetafile.setObjectName("lblMetafile")
        self.gridLayout_2.addWidget(self.lblMetafile, 0, 0, 1, 1)
        self.lblMaskfile = QtGui.QLabel(self.gridLayoutWidget)
        self.lblMaskfile.setObjectName("lblMaskfile")
        self.gridLayout_2.addWidget(self.lblMaskfile, 1, 0, 1, 1)
        self.txtMetafile = QtGui.QLineEdit(self.gridLayoutWidget)
        self.txtMetafile.setObjectName("txtMetafile")
        self.gridLayout_2.addWidget(self.txtMetafile, 0, 1, 1, 1)
        self.txtMaskfile = QtGui.QLineEdit(self.gridLayoutWidget)
        self.txtMaskfile.setObjectName("txtMaskfile")
        self.gridLayout_2.addWidget(self.txtMaskfile, 1, 1, 1, 1)
        self.btnOpenMetafile = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnOpenMetafile.setObjectName("btnOpenMetafile")
        self.gridLayout_2.addWidget(self.btnOpenMetafile, 0, 2, 1, 1)
        self.btnOpenMaskfile = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnOpenMaskfile.setObjectName("btnOpenMaskfile")
        self.gridLayout_2.addWidget(self.btnOpenMaskfile, 1, 2, 1, 1)
        self.chkDefault = QtGui.QCheckBox(self.gridLayoutWidget)
        self.chkDefault.setChecked(True)
        self.chkDefault.setTristate(False)
        self.chkDefault.setObjectName("chkDefault")
        self.gridLayout_2.addWidget(self.chkDefault, 3, 0, 1, 1)
        self.lblTmpfolder = QtGui.QLabel(self.gridLayoutWidget)
        self.lblTmpfolder.setEnabled(False)
        self.lblTmpfolder.setObjectName("lblTmpfolder")
        self.gridLayout_2.addWidget(self.lblTmpfolder, 4, 0, 1, 1)
        self.txtTmpfolder = QtGui.QLineEdit(self.gridLayoutWidget)
        self.txtTmpfolder.setEnabled(False)
        self.txtTmpfolder.setObjectName("txtTmpfolder")
        self.gridLayout_2.addWidget(self.txtTmpfolder, 4, 1, 1, 1)
        self.btnOpenTmpfolder = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnOpenTmpfolder.setEnabled(False)
        self.btnOpenTmpfolder.setObjectName("btnOpenTmpfolder")
        self.gridLayout_2.addWidget(self.btnOpenTmpfolder, 4, 2, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.chkShadows = QtGui.QCheckBox(self.gridLayoutWidget)
        self.chkShadows.setChecked(True)
        self.chkShadows.setObjectName("chkShadows")
        self.horizontalLayout_2.addWidget(self.chkShadows)
        self.chkCloud = QtGui.QCheckBox(self.gridLayoutWidget)
        self.chkCloud.setChecked(True)
        self.chkCloud.setObjectName("chkCloud")
        self.horizontalLayout_2.addWidget(self.chkCloud)
        self.chkPass = QtGui.QCheckBox(self.gridLayoutWidget)
        self.chkPass.setObjectName("chkPass")
        self.horizontalLayout_2.addWidget(self.chkPass)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.btnOk = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnOk.setObjectName("btnOk")
        self.gridLayout_4.addWidget(self.btnOk, 0, 1, 1, 1)
        self.btnCancel = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnCancel.setObjectName("btnCancel")
        self.gridLayout_4.addWidget(self.btnCancel, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_4)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.txtMetafile, self.btnOpenMetafile)
        Dialog.setTabOrder(self.btnOpenMetafile, self.txtMaskfile)
        Dialog.setTabOrder(self.txtMaskfile, self.btnOpenMaskfile)
        Dialog.setTabOrder(self.btnOpenMaskfile, self.chkDefault)
        Dialog.setTabOrder(self.chkDefault, self.txtTmpfolder)
        Dialog.setTabOrder(self.txtTmpfolder, self.btnOpenTmpfolder)
        Dialog.setTabOrder(self.btnOpenTmpfolder, self.btnOk)
        Dialog.setTabOrder(self.btnOk, self.btnCancel)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Acca Plugin", None, QtGui.QApplication.UnicodeUTF8))
        self.lblMetafile.setText(QtGui.QApplication.translate("Dialog", "Select metafile", None, QtGui.QApplication.UnicodeUTF8))
        self.lblMaskfile.setText(QtGui.QApplication.translate("Dialog", "Select maskfile", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOpenMetafile.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOpenMaskfile.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.chkDefault.setText(QtGui.QApplication.translate("Dialog", "Use default path", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTmpfolder.setText(QtGui.QApplication.translate("Dialog", "Select tmp folder", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOpenTmpfolder.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.chkShadows.setText(QtGui.QApplication.translate("Dialog", "With shadows", None, QtGui.QApplication.UnicodeUTF8))
        self.chkCloud.setText(QtGui.QApplication.translate("Dialog", "Cloud sign.", None, QtGui.QApplication.UnicodeUTF8))
        self.chkPass.setText(QtGui.QApplication.translate("Dialog", "Single pass", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOk.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

