from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import osgeo.gdal as gdal
import cv
import resources
import time

from form import Ui_Dialog
from __init__ import name

class TestPlugin:

    def __init__(self, iface):
        self.iface = iface
        
    def showImage(self,image):
        cv.NamedWindow(name(), cv.CV_WINDOW_AUTOSIZE)
        cv.ShowImage(name(),image)
        key=cv.WaitKey(10)

    def openFolder(self):
        print self.fileName.toUtf8().data()
        gdalData = gdal.Open(self.fileName.toUtf8().data(), gdal.GA_ReadOnly)
        if gdalData is None:
            QMessageBox.information(self.window,name(),"ERROR: Can`t open raster")
            return
        print "Driver short name", gdalData.GetDriver().ShortName
        print "Driver long name", gdalData.GetDriver().LongName
        print "Raster size", gdalData.RasterXSize, "x", gdalData.RasterYSize
        print "Number of bands", gdalData.RasterCount
        print "Projection", gdalData.GetProjection()
        print "Geo transform", gdalData.GetGeoTransform()
        print "Channels count", gdalData.RasterCount
        image=cv.CreateImage((256,256),cv.IPL_DEPTH_8U,1)
        self.showImage(image)



    def initGui(self):
        self.action = QAction(QIcon(":/plugins/000_testplugin/icon.png"), "Test plugin", self.iface.mainWindow())
        self.action.setWhatsThis("Configuration for test plugin")
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Test plugin", self.action)

    def unload(self):
        self.iface.removePluginMenu("&Test plugin", self.action)
        self.iface.removeToolBarIcon(self.action)
    
    def run(self):
        self.window = QDialog()
        self.window.setWindowTitle("Test");
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.window)
        QObject.connect(self.ui.pushButton, SIGNAL("clicked()"), lambda: self.buttonClick(self))
        self.window.exec_()
    
    def buttonClick(self, param):
        self.fileName = QFileDialog.getExistingDirectory(None, "Open directory", QDir.currentPath())
        self.ui.label.setText(self.fileName)
        self.openFolder()
