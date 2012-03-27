# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress_form.ui'
#
# Created: Fri Mar 23 14:42:26 2012
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_progress_dialog(object):
    def setupUi(self, progress_dialog):
        progress_dialog.setObjectName("progress_dialog")
        progress_dialog.resize(520, 187)
        self.verticalLayoutWidget = QtGui.QWidget(progress_dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 501, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.btnCancel = QtGui.QPushButton(self.verticalLayoutWidget)
        self.btnCancel.setObjectName("btnCancel")
        self.gridLayout.addWidget(self.btnCancel, 5, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 5, 2, 1, 1)
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
        self.prBar.setProperty("value", 24)
        self.prBar.setObjectName("prBar")
        self.gridLayout.addWidget(self.prBar, 1, 0, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(progress_dialog)
        QtCore.QMetaObject.connectSlotsByName(progress_dialog)

    def retranslateUi(self, progress_dialog):
        progress_dialog.setWindowTitle(QtGui.QApplication.translate("progress_dialog", "Progress", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("progress_dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.lblStatus.setText(QtGui.QApplication.translate("progress_dialog", "Progress", None, QtGui.QApplication.UnicodeUTF8))

