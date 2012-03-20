# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created: Tue Mar 20 21:41:51 2012
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(490, 178)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.btnInPath = QtGui.QPushButton(Dialog)
        self.btnInPath.setGeometry(QtCore.QRect(460, 10, 21, 27))
        self.btnInPath.setObjectName("btnInPath")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 181, 17))
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("label")
        self.chkDefault = QtGui.QCheckBox(Dialog)
        self.chkDefault.setGeometry(QtCore.QRect(10, 120, 101, 22))
        self.chkDefault.setChecked(True)
        self.chkDefault.setObjectName("chkDefault")
        self.txtInPath = QtGui.QLineEdit(Dialog)
        self.txtInPath.setGeometry(QtCore.QRect(200, 10, 261, 27))
        self.txtInPath.setObjectName("txtInPath")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 181, 17))
        self.label_2.setAutoFillBackground(False)
        self.label_2.setObjectName("label_2")
        self.btnOutPath = QtGui.QPushButton(Dialog)
        self.btnOutPath.setGeometry(QtCore.QRect(460, 40, 21, 27))
        self.btnOutPath.setObjectName("btnOutPath")
        self.txtOutPath = QtGui.QLineEdit(Dialog)
        self.txtOutPath.setGeometry(QtCore.QRect(200, 40, 261, 27))
        self.txtOutPath.setObjectName("txtOutPath")
        self.txtTmpPath = QtGui.QLineEdit(Dialog)
        self.txtTmpPath.setEnabled(False)
        self.txtTmpPath.setGeometry(QtCore.QRect(200, 100, 261, 27))
        self.txtTmpPath.setObjectName("txtTmpPath")
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 181, 17))
        self.label_3.setAutoFillBackground(False)
        self.label_3.setObjectName("label_3")
        self.btnTmpPath = QtGui.QPushButton(Dialog)
        self.btnTmpPath.setEnabled(False)
        self.btnTmpPath.setGeometry(QtCore.QRect(460, 100, 21, 27))
        self.btnTmpPath.setObjectName("btnTmpPath")
        self.btnGo = QtGui.QPushButton(Dialog)
        self.btnGo.setGeometry(QtCore.QRect(380, 140, 90, 27))
        self.btnGo.setObjectName("btnGo")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.btnInPath.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Select input data (metafile):", None, QtGui.QApplication.UnicodeUTF8))
        self.chkDefault.setText(QtGui.QApplication.translate("Dialog", "Use default", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Select folder for mask file:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOutPath.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.txtTmpPath.setText(QtGui.QApplication.translate("Dialog", "/tmp", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Select folder for tmp data:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnTmpPath.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGo.setText(QtGui.QApplication.translate("Dialog", "Go!", None, QtGui.QApplication.UnicodeUTF8))

