# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress_form.ui'
#
# Created: Fri Apr 27 19:11:35 2012
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_progress_dialog(object):
    def setupUi(self, progress_dialog):
        progress_dialog.setObjectName("progress_dialog")
        progress_dialog.resize(520, 98)
        self.verticalLayoutWidget = QtGui.QWidget(progress_dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 501, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lblStatus = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblStatus.sizePolicy().hasHeightForWidth())
        self.lblStatus.setSizePolicy(sizePolicy)
        self.lblStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.lblStatus.setObjectName("lblStatus")
        self.gridLayout.addWidget(self.lblStatus, 0, 1, 1, 1)
        self.prBar = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.prBar.setProperty("value", 0)
        self.prBar.setObjectName("prBar")
        self.gridLayout.addWidget(self.prBar, 1, 0, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(progress_dialog)
        QtCore.QMetaObject.connectSlotsByName(progress_dialog)

    def retranslateUi(self, progress_dialog):
        progress_dialog.setWindowTitle(QtGui.QApplication.translate("progress_dialog", "Progress", None, QtGui.QApplication.UnicodeUTF8))
        self.lblStatus.setText(QtGui.QApplication.translate("progress_dialog", "Progress", None, QtGui.QApplication.UnicodeUTF8))

