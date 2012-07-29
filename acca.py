#!/usr/bin/env python
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

from PyQt4.QtCore import *
import sys
import osgeo.gdal as gdal
import numpy
import os
import time
import math

class CAcca(QThread):
    __NO_CLOUD=0
    __NO_DEFINED=1
    __IS_SHADOW=20
    __IS_COULD=1
    __COLD_CLOUD=30
    __WARM_CLOUD=50
    __IS_COLD_CLOUD=60
    __IS_WARM_CLOUD=90

    #printf from C
    def printf(self, fstr,*param):
        if (self.debuglevel==1):
            string=fstr % param
            sys.stdout.write (string)
            #sys.stdout.flush()

    def hist_put(self, band,band_mask,hist):
        #for i in numpy.ma.array(band,mask=band_mask).compressed():
        #    t=int(i*self.__metadata["hist_n"]/100.)
        #    if (t<1): t=1
        #    if (t>self.__metadata["hist_n"]): t=self.__metadata["hist_n"]
        #    hist[t-1]+=1

        #hist[0]=(numpy.array(hist[0])+numpy.array(numpy.histogram(numpy.ma.array(band,mask=band_mask).compressed(),99,(1,100))[0])).tolist()
        t0=numpy.array(hist[0])
        t1=numpy.ma.array(band,mask=band_mask).compressed()
        t2=numpy.histogram(t1,100,(1,101))
        t3=numpy.array(t2[0])
        t4=t0+t3
        t5=t4.tolist()
        hist[0]=t5

    def moment(self, n, hist, k):
        total=0
        mean=0
        j=0
        k=0
        for i in hist:
            total+=i
            mean+=(j*i)
            j+=1
        mean/=total
        value=0.
        j=0
        for i in hist:
            value+=(math.pow(j-mean,n)*i)
        value/=(total-k)
        return (value/math.pow(self.__metadata["hist_n"]/100.,n))

    def quantile(self, q, hist):
        total=0
        for i in hist:
            total+=i
        value=0.
        qmax=1.
        for i in range(self.__metadata["hist_n"]-1,-1,-1):
            qmin=qmax-(hist[i]/total)
            if (q>=qmin):
                value = (q-qmin)/(qmax-qmin)+(i-1)
                break
            qmax=qmin
        return (value/(self.__metadata["hist_n"]/100.))

    def __init__(self, metafile, maskfile, debuglevel=0, with_shadows=True, cloud_signature=True, single_pass=False, parent=None):
        self.metafile=metafile
        self.maskfile=maskfile
        self.debuglevel=debuglevel
        QThread.__init__(self,parent)
        self.WITH_SHADOW=with_shadows
        self.cloud_signature=cloud_signature
        self.single_pass=single_pass

    def shadow_algorithm(self,band,mask):
        numpy.putmask(mask[0],(mask[0]==self.__NO_DEFINED)&((band[3]<0.07) & (((1-band[4])*band[6])>240.) & ((band[4]/band[2]>1.)) & ((band[3]-band[5])/(band[3]+band[5])<0.10)),self.__IS_SHADOW)

    #Acca algorithm, first pass
    def acca_first(self,band, mask):
        boolmask=numpy.invert(numpy.zeros(band[2].shape,dtype=bool))

        th=self.__metadata["threshold"]
        ndsi=(band[2]-band[5])/(band[2]+band[5])
        rat56=(1.-band[5])*band[6]

        mask.append(numpy.empty(band[2].shape,dtype=numpy.uint8))
        mask[0][:]=self.__NO_DEFINED
        numpy.putmask(mask[0],((band[2]==0.) | (band[3]==0.) | (band[4]==0.) | (band[5]==0.) | (band[6]==0.)),self.__NO_CLOUD)

        if "WITH_SHADOW" in self.__metadata:
            if self.__metadata["WITH_SHADOW"]==True:
                self.shadow_algorithm(band,mask);

        boolmask_prev=(mask[0]==self.__NO_DEFINED)

        numpy.putmask(mask[0],boolmask_prev,self.__NO_CLOUD)

        self.__metadata["count"]["TOTAL"]+=numpy.sum(boolmask)
        boolmask=boolmask&boolmask_prev

        #filter 1                                                                          
        boolmask_prev = (band[3]>th["th_1"])
        numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask&(band[3]<th["th_1_b"]),self.__NO_CLOUD)
        numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask&(band[3]>th["th_1_b"]),self.__NO_DEFINED)
        boolmask=boolmask&boolmask_prev

        #filter 2 (ndsi)
        boolmask_prev = (ndsi>th["th_2"][0]) & (ndsi<th["th_2"][1])
        numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask,self.__NO_CLOUD)
        self.__metadata["count"]["SNOW"]+=numpy.sum(numpy.invert(boolmask_prev)&(ndsi>th["th_2_b"]))
        boolmask=boolmask&boolmask_prev

        #filter 3
        boolmask_prev = (band[6]<th["th_3"])
        numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask,self.__NO_CLOUD)
        boolmask=boolmask&boolmask_prev

        #filter 4
        boolmask_prev = (rat56<th["th_4"])
        numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask&(band[5]<th["th_4_b"]),self.__NO_CLOUD)
        numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask&(band[5]>th["th_4_b"]),self.__NO_DEFINED)
        boolmask=boolmask&boolmask_prev

        #filter 5
        boolmask_prev = ((band[4]/band[3])<th["th_5"])
        numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask,self.__NO_DEFINED)
        boolmask=boolmask&boolmask_prev

        #filter 6
        boolmask_prev = ((band[4]/band[2])<th["th_6"])
        self.__metadata["count"]["SOIL"]+=numpy.sum(boolmask_prev&boolmask)
        self.__metadata["count"]["SOIL"]+=numpy.sum(numpy.invert(boolmask_prev)&boolmask)
        numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask,self.__NO_DEFINED)
        boolmask=boolmask&boolmask_prev

        #filter 7
        boolmask_prev = ((band[4]/band[5])>th["th_7"])
        numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask,self.__NO_DEFINED)
        boolmask=boolmask&boolmask_prev

        numpy.putmask(mask[0],boolmask & (rat56<th["th_8"]),self.__COLD_CLOUD)
        numpy.putmask(mask[0],boolmask & (rat56>=th["th_8"]),self.__WARM_CLOUD)
        self.__metadata["stats"]["SUM_COLD"]+=numpy.sum(boolmask & (rat56<th["th_8"]))
        self.__metadata["stats"]["SUM_WARM"]+=numpy.sum(boolmask & (rat56>=th["th_8"]))
        self.__metadata["count"]["COLD"]+=numpy.sum(boolmask & (rat56<th["th_8"]))
        self.__metadata["count"]["WARM"]+=numpy.sum(boolmask & (rat56>=th["th_8"]))
        hist=[self.__metadata["hist_cold"]]
        self.hist_put((band[6]-self.__metadata["K_BASE"]),(boolmask&(rat56<th["th_8"])),hist)
        self.__metadata["hist_cold"]=hist[0]
        hist=[self.__metadata["hist_warm"]]
        self.hist_put((band[6]-self.__metadata["K_BASE"]),(boolmask&(rat56>=th["th_8"])),hist)
        self.__metadata["hist_warm"]=hist[0]
        tmax=numpy.max(band[6])
        tmin=numpy.min(band[6])
        if (tmax>self.__metadata["stats"]["KMAX"]): self.__metadata["stats"]["KMAX"]=tmax
        if (tmin<self.__metadata["stats"]["KMIN"]): self.__metadata["stats"]["KMIN"]=tmin

    def acca_second(self, band6, mask):
        boolmask0=(mask[0]==0)
        boolmask0=boolmask0&((mask[0]==self.__NO_DEFINED) | ((mask[0]==self.__WARM_CLOUD) & (self.__metadata["review_warm"]==1)))
        boolmask1=(band6>self.__metadata["value"]["KUPPER"])
        numpy.putmask(mask[0],boolmask0&boolmask1,0)
        boolmask2=(mask[0]<self.__metadata["value"]["KLOWER"])
        numpy.putmask(mask[0],boolmask0&numpy.invert(boolmask1)&boolmask2,self.__IS_WARM_CLOUD)
        numpy.putmask(mask[0],boolmask0&numpy.invert(boolmask1)&numpy.invert(boolmask2),self.__IS_COLD_CLOUD)
        boolmask1=None
        boolmask2=None

        boolmask1=((mask[0]==self.__COLD_CLOUD) | (mask[0]==self.__WARM_CLOUD))
        boolmask2=((mask[0]==self.__WARM_CLOUD) & (self.__metadata["review_warm"]==0))

        numpy.putmask(mask[0],numpy.invert(boolmask0)&boolmask1&boolmask2,self.__IS_WARM_CLOUD)
        numpy.putmask(mask[0],numpy.invert(boolmask0)&boolmask1&numpy.invert(boolmask2),self.__IS_COLD_CLOUD)
        boolmask2=None
        numpy.putmask(mask[0],numpy.invert(boolmask0)&numpy.invert(boolmask1),self.__IS_SHADOW)

    #Parsing metafile
    def parsing(self):
        self.__metadata={}
        path=self.metafile
        self.__metadata["WITH_SHADOW"]=self.WITH_SHADOW
        self.__metadata["cloud_signature"]=self.cloud_signature
        self.__metadata["single_pass"]=self.single_pass
        self.__metadata["MASK_FILE_NAME"]=self.maskfile
        if not os.path.exists(path):
            self.printf ("ERROR: Can`t open metafile\n")
            return None
        metafile=open(path)
        for line in metafile:
            key,param=line.strip().split('=')
            self.__metadata[key]=param
        for i in range(2,7):
            self.__metadata["BAND"+str(i)+"_FILE_NAME"]=os.path.join(os.path.dirname(path),os.path.basename(self.__metadata["BAND"+str(i)+"_FILE_NAME"]))
        self.__metadata["SCALE"]=200.
        self.__metadata["K_BASE"]=230.
        self.__metadata["hist_n"]=100
        self.__metadata["threshold"]={}

        self.__metadata["threshold"]["th_1"]=0.08
        self.__metadata["threshold"]["th_1_b"]=0.07
        self.__metadata["threshold"]["th_2"]=[-0.25,0.70]
        self.__metadata["threshold"]["th_2_b"]=0.8
        self.__metadata["threshold"]["th_3"]=300.
        self.__metadata["threshold"]["th_4"]=225.
        self.__metadata["threshold"]["th_4_b"]=0.08
        self.__metadata["threshold"]["th_5"]=2.35
        self.__metadata["threshold"]["th_6"]=2.16248
        self.__metadata["threshold"]["th_7"]=1.0
        self.__metadata["threshold"]["th_8"]=210.

        return self.__metadata

    #Loading bands from file
    def load_bands(self):
        gdalData=[]

        for i in 2,3,4,5,6:
            if "BAND"+str(i)+"_FILE_NAME" in self.__metadata:
                gdalData.append(gdal.Open(self.__metadata["BAND"+str(i)+"_FILE_NAME"], gdal.GA_ReadOnly))
                if gdalData[-1] is None:
                    self.printf ("ERROR: Can`t open raster")
                    return None
                #self.printf ("Driver short name", gdalData[-1].GetDriver().ShortName)
                #self.printf ("Driver long name", gdalData[-1].GetDriver().LongName)
                #self.printf ("Raster size", gdalData[-1].RasterXSize, "x", gdalData[-1].RasterYSize)
                #self.printf ("Number of bands", gdalData[-1].RasterCount)
                #self.printf ("Projection", gdalData[-1].GetProjection())
                #self.printf ("Geo transform", gdalData[-1].GetGeoTransform())
                #self.printf ("Channels count", gdalData[-1].RasterCount)
                self.printf ("INFO: File %s %s\n", self.__metadata["BAND"+str(i)+"_FILE_NAME"], "loaded")

            else:
                self.printf ("ERROR: Missing one or more band.")
                return None
        return gdalData

    def close_bands(self,gdalData):
        self.printf ("INFO: Closing dataset\n")
        gdalData[0]=None
        gdalData[1]=None
        gdalData[2]=None
        gdalData[3]=None
        gdalData[4]=None

    def processing(self,gdalData):
        raster=[]
        format="GTiff"
        driver=gdal.GetDriverByName(format)
        projection=gdalData[0].GetProjection()
        transform=gdalData[0].GetGeoTransform()
        xsize=gdalData[0].RasterXSize
        ysize=gdalData[0].RasterYSize
        drvMeta=driver.GetMetadata()
        if drvMeta.has_key( gdal.DCAP_CREATE ) and drvMeta[ gdal.DCAP_CREATE ] == "YES":
            mask=driver.Create(self.__metadata["MASK_FILE_NAME"], xsize, ysize, 1, gdal.GDT_Byte)
            mask.SetProjection(projection)
            mask.SetGeoTransform(transform)
        else:
            self.printf ("INFO: Driver %s does not support Create() method.\n", format)
            return None

        step=2000
        x=gdalData[0].RasterXSize
        y=gdalData[0].RasterYSize
        area=x*y
        processed_area=0
        need_new_row=True
        need_new_column=True
        self.printf ("INFO: Running first pass\n")
        self.__metadata["stats"]={"SUM_COLD":0.,"SUM_WARM":0.,"KMAX":0.,"KMIN":10000.}
        self.__metadata["count"]={"WARM":0.,"COLD":0.,"SNOW":0.,"SOIL":0.,"TOTAL":0.}
        self.__metadata["value"]={"WARM":0.,"COLD":0.,"SNOW":0.,"SOIL":0.}
        self.__metadata["hist_cold"]=[0]*self.__metadata["hist_n"]
        self.__metadata["hist_warm"]=[0]*self.__metadata["hist_n"]
        for i in range(0,x,step):
            need_new_row=True
            for j in range(0,y,step):
                if i+step > x:
                    stepx=x-i
                else:
                    stepx=step
                if j+step > y:
                    stepy=y-j
                else:
                    stepy=step
                mask_arg=[]
                self.acca_first ({2:gdalData[0].ReadAsArray(i,j,stepx,stepy).astype(numpy.float32),\
                            3:gdalData[1].ReadAsArray(i,j,stepx,stepy).astype(numpy.float32),\
                            4:gdalData[2].ReadAsArray(i,j,stepx,stepy).astype(numpy.float32),\
                            5:gdalData[3].ReadAsArray(i,j,stepx,stepy).astype(numpy.float32),\
                            6:gdalData[4].ReadAsArray(i,j,stepx,stepy).astype(numpy.float32)},\
                            mask_arg)
                if need_new_row:
                    mask_r=mask_arg[0].copy()
                    need_new_row=False
                else:
                    mask_r=numpy.vstack((mask_r,mask_arg[0]))
                processed_area+=stepx*stepy
                stat=processed_area*100.0/area
                self.printf ("\rACCA first pass: %.2f%s",stat,"%")
                self.emit(SIGNAL("progress(int, int, float)"), 1, 1, stat)
            if need_new_column:
                mask_c=mask_r.copy()
                need_new_column=False
            else:
                mask_c=numpy.hstack((mask_c,mask_r))
        self.printf ("\nINFO: Writing mask\n")
        mask.GetRasterBand(1).WriteArray(mask_c)
        self.printf ("INFO: Closing mask\n")
        mask=None
        for i in gdalData:
            i=None

        self.__metadata["value"]["WARM"]=self.__metadata["count"]["WARM"]/self.__metadata["count"]["TOTAL"]
        self.__metadata["value"]["COLD"]=self.__metadata["count"]["COLD"]/self.__metadata["count"]["TOTAL"]
        self.__metadata["value"]["SNOW"]=self.__metadata["count"]["SNOW"]/self.__metadata["count"]["TOTAL"]
        self.__metadata["value"]["SOIL"]=self.__metadata["count"]["SOIL"]/self.__metadata["count"]["TOTAL"]

        self.__metadata["value"]["TOTAL"]=self.__metadata["count"]["WARM"]+self.__metadata["count"]["COLD"]
        if (self.__metadata["value"]["TOTAL"]==0.):
            idesert=0.
        else:
            idesert=self.__metadata["value"]["SOIL"]

        if ((idesert<=.5) | (self.__metadata["value"]["SNOW"]>0.01)):
            self.__metadata["review_warm"]=1
        else:
            self.__metadata["review_warm"]=0
            self.__metadata["count"]["COLD"]+=self.__metadata["count"]["WARM"]
            self.__metadata["value"]["COLD"]+=self.__metadata["value"]["WARM"]
            self.__metadata["stats"]["SUM_COLD"]+=self.__metadata["stats"]["SUM_WARM"]
            i=0
            for j in hist_warm:
                hist_cold[i]+=j
                i+=1

        self.__metadata["stats"]["KMEAN"]=self.__metadata["SCALE"]*self.__metadata["stats"]["SUM_COLD"]/self.__metadata["count"]["COLD"]
        self.__metadata["stats"]["COVER"]=self.__metadata["count"]["COLD"]/self.__metadata["count"]["TOTAL"]

        if (self.__metadata["cloud_signature"] | ((idesert > .5) & (self.__metadata["stats"]["COVER"] > 0.004) & (self.__metadata["stats"]["KMEAN"] < 295.))):
            self.__metadata["value"]["MEAN"]=self.quantile(0.5,self.__metadata["hist_cold"])+self.__metadata["K_BASE"]
            self.__metadata["value"]["DSTD"]=math.sqrt(self.moment(2,self.__metadata["hist_cold"],1))
            self.__metadata["value"]["SKEW"]=self.moment(3,self.__metadata["hist_cold"],3)/math.pow(self.__metadata["value"]["DSTD"],3)
            shift=self.__metadata["value"]["SKEW"]
            if (shift>1.):
                shift=1.
            else:
                if (shift<0.):
                    shift=0.
            max=self.quantile(0.9875,self.__metadata["hist_cold"])+self.__metadata["K_BASE"]
            self.__metadata["value"]["KUPPER"]=self.quantile(0.975,self.__metadata["hist_cold"])+self.__metadata["K_BASE"]
            self.__metadata["value"]["KLOWER"]=self.quantile(0.835,self.__metadata["hist_cold"])+self.__metadata["K_BASE"]
            if (shift>0.):
                shift*=self.__metadata["value"]["DSTD"]
                if ((self.__metadata["value"]["KUPPER"]+shift)>max):
                    if ((self.__metadata["value"]["KLOWER"]+shift)>max):
                        self.__metadata["value"]["KLOWER"]+=(max-self.__metadata["value"]["KUPPER"])
                    else:
                        self.__metadata["value"]["KLOWER"]+=shift
                    self.__metadata["value"]["KUPPER"]=max
                else:
                    self.__metadata["value"]["KLOWER"]+=shift
                    self.__metadata["value"]["KUPPER"]+=shift
        else:
            if (self.__metadata["stats"]["KMEAN"]<295.):
                self.__metadata["review_warm"]=0.
                self.__metadata["value"]["KUPPER"]=0.
                self.__metadata["value"]["KLOWER"]=0.
            else:
                self.__metadata["review_warm"]=1.
                self.__metadata["value"]["KUPPER"]=0.
                self.__metadata["value"]["KLOWER"]=0.
        if (self.__metadata["single_pass"]):
                self.__metadata["review_warm"]=-1.
                self.__metadata["value"]["KUPPER"]=0.
                self.__metadata["value"]["KLOWER"]=0.

        mask=gdal.Open(self.__metadata["MASK_FILE_NAME"], gdal.GA_Update)
        band6=gdal.Open(self.__metadata["BAND6_FILE_NAME"], gdal.GA_ReadOnly)
        step=2000
        x=band6.RasterXSize
        y=band6.RasterYSize
        area=x*y
        processed_area=0
        need_new_row=True
        need_new_column=True
        self.printf ("INFO: Running second pass\n")
        for i in range(0,x,step):
            need_new_row=True
            for j in range(0,y,step):
                if i+step > x:
                    stepx=x-i
                else:
                    stepx=step
                if j+step > y:
                    stepy=y-j
                else:
                    stepy=step
                mask_arg=[mask.ReadAsArray(i,j,stepx,stepy).astype(numpy.float32)]
                self.acca_second (band6.ReadAsArray(i,j,stepx,stepy).astype(numpy.float32),mask_arg)
                if need_new_row:
                    mask_r=mask_arg[0].copy()
                    need_new_row=False
                else:
                    mask_r=numpy.vstack((mask_r,mask_arg[0]))
                processed_area+=stepx*stepy
                stat=processed_area*100.0/area
                self.printf ("\rACCA second pass: %.2f%s",stat,"%")
                self.emit(SIGNAL("progress(int, int, float)"), 1, 2, stat)
        if need_new_column:
            mask_c=mask_r.copy()
            need_new_column=False
        else:
            mask_c=numpy.hstack((mask_c,mask_r))
        self.printf ("\nINFO: Writing mask\n")
        #mask.GetRasterBand(1).WriteArray(mask_c)
        self.printf ("INFO: Closing mask\n")
        mask=None
        band6=None

    def run(self):
        self.__metadata=self.parsing()
        if (self.__metadata == None):
            return None
        gdalData=self.load_bands()
        if (gdalData == None):
            return None
        if (self.processing(gdalData) == None):
            return None
