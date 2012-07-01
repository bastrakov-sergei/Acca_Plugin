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

