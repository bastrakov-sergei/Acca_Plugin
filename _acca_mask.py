#!/usr/bin/env python
import sys
import osgeo.gdal as gdal
import numpy
import os
import time
import math

NO_CLOUD=0
NO_DEFINED=1
IS_SHADOW=20
IS_COULD=1
COLD_CLOUD=30
WARM_CLOUD=50
IS_COLD_CLOUD=6
IS_WARM_CLOUD=9


#printf from C
def printf(fstr,*param):
    string=fstr % param
    sys.stdout.write (string)
    sys.stdout.flush()

#Calculate Earth Sun distance form date (YYYY-mm-dd)
def ESD(date):
    days=[1,15,32,46,60,74,91,106,121,135,152,166,182,192,213,227,242,258,274,288,305,319,335,349,365]
    dist=[.98331,.98365,.98536,.98774,.99084,.99446,.99926,1.00353,1.00756,1.01087,1.01403,1.01577,1.01667,1.01646,1.01497,1.01281,1.00969,1.00566,1.00119,.99718,.99253,.98916,.98608,.98426,.98333]
    nday=int(time.strftime("%j",time.strptime(date,"%Y-%m-%d")))
    DIST=numpy.interp(nday,days,dist)
    return DIST

#using
def using():
    print "Using:\n\t", sys.argv[0],  "<metafile> <mask file>"

def toar(band,metadata):
    #Calculate radiance
    band[2]=((metadata["LMAX_BAND2"]-metadata["LMIN_BAND2"])/(metadata["QCALMAX_BAND2"]-metadata["QCALMIN_BAND2"]))*(band[2]-metadata["QCALMIN_BAND2"])+metadata["LMIN_BAND2"]
    band[3]=((metadata["LMAX_BAND3"]-metadata["LMIN_BAND3"])/(metadata["QCALMAX_BAND3"]-metadata["QCALMIN_BAND3"]))*(band[3]-metadata["QCALMIN_BAND3"])+metadata["LMIN_BAND3"]
    band[4]=((metadata["LMAX_BAND4"]-metadata["LMIN_BAND4"])/(metadata["QCALMAX_BAND4"]-metadata["QCALMIN_BAND4"]))*(band[4]-metadata["QCALMIN_BAND4"])+metadata["LMIN_BAND4"]
    band[5]=((metadata["LMAX_BAND5"]-metadata["LMIN_BAND5"])/(metadata["QCALMAX_BAND5"]-metadata["QCALMIN_BAND5"]))*(band[5]-metadata["QCALMIN_BAND5"])+metadata["LMIN_BAND5"]
    band[6]=((metadata["LMAX_BAND6"]-metadata["LMIN_BAND6"])/(metadata["QCALMAX_BAND6"]-metadata["QCALMIN_BAND6"]))*(band[6]-metadata["QCALMIN_BAND6"])+metadata["LMIN_BAND6"]
    #ESUN for 2,3,4,5 bands
    ESUN={"7":{2:1812.,3:1533.,4:1039.,5:230.8},"5":{2:1826.,3:1554.,4:1036.,5:215.0}}
    #Thermal band calibration metadataants
    TBCC={"7":{"K1":666.09,"K2":1282.71},"5":{"K1":607.76,"K2":1260.56}}
    #cosine of THETA
    COSTHETA=metadata["cos(THETA)"]
    DIST=ESD(metadata["date"])
    band[2]=(numpy.pi*band[2]*math.pow(DIST,2))/(COSTHETA*ESUN[metadata["sat"]][2])
    band[3]=(numpy.pi*band[3]*math.pow(DIST,2))/(COSTHETA*ESUN[metadata["sat"]][3])
    band[4]=(numpy.pi*band[4]*math.pow(DIST,2))/(COSTHETA*ESUN[metadata["sat"]][4])
    band[5]=(numpy.pi*band[5]*math.pow(DIST,2))/(COSTHETA*ESUN[metadata["sat"]][5])
    band[6]=TBCC[metadata["sat"]]["K2"]/numpy.log(TBCC[metadata["sat"]]["K1"]/band[6]+1)

def shadow_algorithm(band,mask):
    numpy.putmask(mask[0],(mask[0]==NO_DEFINED)&((band[3]<0.07) & (((1-band[4])*band[6])>240.) & ((band[4]/band[2]>1.)) & ((band[3]-band[5])/(band[3]+band[5])<0.10)),IS_SHADOW)

#Acca algorithm, first pass
def acca_first(band, mask, metadata):
    boolmask=numpy.invert(numpy.zeros(band[2].shape,dtype=bool))
    toar(band,metadata)

    ndsi=(band[2]-band[5])/(band[2]+band[5])
    rat56=(1.-band[5])*band[6]

    mask.append(numpy.empty(band[2].shape,dtype=numpy.uint8))
    mask[0][:]=NO_DEFINED
    numpy.putmask(mask[0],((band[2]==0.) | (band[3]==0.) | (band[4]==0.) | (band[5]==0.) | (band[6]==0.)),NO_CLOUD)

    if "WITH_SHADOW" in metadata:
        if metadata["WITH_SHADOW"]==True:
            shadow_algorithm(band,mask);

    boolmask_prev=(mask[0]==NO_DEFINED)

    numpy.putmask(mask[0],boolmask_prev,NO_CLOUD)

    metadata["count"]["TOTAL"]+=numpy.sum(boolmask)
    boolmask=boolmask&boolmask_prev

    #filter 1                                                                          
    boolmask_prev = (band[3]>0.08)
    numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask&(band[3]<0.07),NO_CLOUD)
    numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask&(band[3]>0.07),NO_DEFINED)
    boolmask=boolmask&boolmask_prev

    #filter 2 (ndsi)
    boolmask_prev = (ndsi>-0.25) & (ndsi<0.70)
    numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask,NO_CLOUD)
    metadata["count"]["SNOW"]+=numpy.sum(numpy.invert(boolmask_prev)&(ndsi>0.08))
    boolmask=boolmask&boolmask_prev

    #filter 3
    boolmask_prev = (band[6]<300)
    numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask,NO_CLOUD)
    boolmask=boolmask&boolmask_prev

    #filter 4
    boolmask_prev = (rat56<225)
    numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask&(band[5]<0.8),NO_CLOUD)
    numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask&(band[5]>0.8),NO_DEFINED)
    boolmask=boolmask&boolmask_prev

    #filter 5
    boolmask_prev = ((band[4]/band[3])<2.35)
    numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask,NO_DEFINED)
    boolmask=boolmask&boolmask_prev

    #filter 6
    boolmask_prev = ((band[4]/band[2])<2.16248)
    metadata["count"]["SOIL"]+=numpy.sum(boolmask_prev&boolmask)
    metadata["count"]["SOIL"]+=numpy.sum(numpy.invert(boolmask_prev)&boolmask)
    numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask,NO_DEFINED)
    boolmask=boolmask&boolmask_prev

    #filter 7
    boolmask_prev = ((band[4]/band[5])>1.0)
    numpy.putmask(mask[0],numpy.invert(boolmask_prev)&boolmask,NO_DEFINED)
    boolmask=boolmask&boolmask_prev

    numpy.putmask(mask[0],boolmask & (rat56<210.),COLD_CLOUD)
    numpy.putmask(mask[0],boolmask & (rat56>=210.),WARM_CLOUD)
    metadata["stats"]["SUM_COLD"]+=numpy.sum(boolmask & (rat56<210.))
    metadata["stats"]["SUM_WARM"]+=numpy.sum(boolmask & (rat56>=210.))
    tmax=numpy.max(band[6])
    tmin=numpy.min(band[6])
    if (tmax>metadata["stats"]["KMAX"]): metadata["stats"]["KMAX"]=tmax
    if (tmin<metadata["stats"]["KMIN"]): metadata["stats"]["KMIN"]=tmin

#    numpy.putmask(mask[0],boolmask==True,IS_COULD)

#Parsing metafile
def parsing(list):
    metadata={}
    path=list[0]
    metadata["MASK_FILE_NAME"]=list[1]
    if not os.path.exists(path):
        print "ERROR: Can`t open metafile"
        sys.exit(-1)
    metafile=open(path)
    for line in metafile:
        param=line.split('=')
        if param[0].strip() == "SPACECRAFT_ID":
            if param[1].strip() == "Landsat7":
                band61=True
                metadata['sat']="7"
            else:
                band61=False
                metadata['sat']="5"
        if param[0].strip() == "BAND2_FILE_NAME" or \
            param[0].strip() == "BAND3_FILE_NAME" or \
            param[0].strip() == "BAND4_FILE_NAME" or \
            param[0].strip() == "BAND5_FILE_NAME" or \
            param[0].strip() == "BAND6_FILE_NAME":
            metadata[param[0].strip()]=os.path.join(os.path.dirname(path),param[1].strip().replace('"',''))

        if param[0].strip() == "BAND61_FILE_NAME":
            metadata["BAND6_FILE_NAME"]=os.path.join(os.path.dirname(path),param[1].strip().replace('"',''))

        if param[0].strip() == "ACQUISITION_DATE":
            metadata["date"]=param[1].strip().replace('"','')

        if param[0].strip() == "SUN_ELEVATION":
            metadata["cos(THETA)"]=math.cos(90.-float(param[1].strip().replace('"','')))

        if param[0].strip() == "LMAX_BAND2" or \
            param[0].strip() == "LMIN_BAND2" or \
            param[0].strip() == "LMAX_BAND3" or \
            param[0].strip() == "LMIN_BAND3" or \
            param[0].strip() == "LMAX_BAND4" or \
            param[0].strip() == "LMIN_BAND4" or \
            param[0].strip() == "LMAX_BAND5" or \
            param[0].strip() == "LMIN_BAND5" or \
            param[0].strip() == "LMAX_BAND6" or \
            param[0].strip() == "LMIN_BAND6" or \
            param[0].strip() == "QCALMAX_BAND2" or \
            param[0].strip() == "QCALMIN_BAND2" or \
            param[0].strip() == "QCALMAX_BAND3" or \
            param[0].strip() == "QCALMIN_BAND3" or \
            param[0].strip() == "QCALMAX_BAND4" or \
            param[0].strip() == "QCALMIN_BAND4" or \
            param[0].strip() == "QCALMAX_BAND5" or \
            param[0].strip() == "QCALMIN_BAND5" or \
            param[0].strip() == "QCALMAX_BAND6" or \
            param[0].strip() == "QCALMIN_BAND6":
            metadata[param[0].strip()]=float(param[1].strip().replace('"',''))

        if param[0].strip() == "QCALMAX_BAND61":
            metadata['QCALMAX_BAND6']=float(param[1].strip().replace('"',''))
        if param[0].strip() == "QCALMIN_BAND61":
            metadata['QCALMIN_BAND6']=float(param[1].strip().replace('"',''))
        if param[0].strip() == "LMAX_BAND61":
            metadata['LMAX_BAND6']=float(param[1].strip().replace('"',''))
        if param[0].strip() == "LMIN_BAND61":
            metadata['LMIN_BAND6']=float(param[1].strip().replace('"',''))
    return metadata

#Loading bands from file
def load_bands(metadata):
    gdalData=[]

    for i in 2,3,4,5,6:
        if "BAND"+str(i)+"_FILE_NAME" in metadata:
            gdalData.append(gdal.Open(metadata["BAND"+str(i)+"_FILE_NAME"], gdal.GA_ReadOnly))
            if gdalData[-1] is None:
                print "ERROR: Can`t open raster"
                sys.exit(-1)
            #print "Driver short name", gdalData[-1].GetDriver().ShortName
            #print "Driver long name", gdalData[-1].GetDriver().LongName
            #print "Raster size", gdalData[-1].RasterXSize, "x", gdalData[-1].RasterYSize
            #print "Number of bands", gdalData[-1].RasterCount
            #print "Projection", gdalData[-1].GetProjection()
            #print "Geo transform", gdalData[-1].GetGeoTransform()
            #print "Channels count", gdalData[-1].RasterCount
            print "INFO: File ", metadata["BAND"+str(i)+"_FILE_NAME"], "loaded"

        else:
            print "ERROR: Missing one or more band."
            sys.exit(-1)
    return gdalData

def close_bands(gdalData):
    print "INFO: Closing dataset"
    gdalData[0]=None
    gdalData[1]=None
    gdalData[2]=None
    gdalData[3]=None
    gdalData[4]=None
    print "INFO: Closing mask file"
    gdalData[5]=None


def processing(metadata,gdalData):
    raster=[]
    format="GTiff"
    driver=gdal.GetDriverByName(format)
    gdalData.append(driver.CreateCopy(metadata["MASK_FILE_NAME"], gdalData[0], 0))
    step=2000
    x=gdalData[0].RasterXSize
    y=gdalData[0].RasterYSize
    area=x*y
    processed_area=0
    need_new_row=True
    need_new_column=True
    print "INFO: Running first pass"
    metadata["stats"]={"SUM_COLD":0.,"SUM_WARM":0.,"KMAX":0.,"KMIN":10000.}
    metadata["count"]={"WARM":0.,"COLD":0.,"SNOW":0.,"SOIL":0.,"TOTAL":0.}
    metadata["value"]={"WARM":0.,"COLD":0.,"SNOW":0.,"SOIL":0.}
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
            acca_first ({2:gdalData[0].ReadAsArray(i,j,stepx,stepy).astype(numpy.float32),\
                    3:gdalData[1].ReadAsArray(i,j,stepx,stepy).astype(numpy.float32),\
                    4:gdalData[2].ReadAsArray(i,j,stepx,stepy).astype(numpy.float32),\
                    5:gdalData[3].ReadAsArray(i,j,stepx,stepy).astype(numpy.float32),\
                    6:gdalData[4].ReadAsArray(i,j,stepx,stepy).astype(numpy.float32)},\
                    mask_arg,metadata)
            if need_new_row:
                mask_r=mask_arg[0].copy()
                need_new_row=False
            else:
                mask_r=numpy.vstack((mask_r,mask_arg[0]))
            processed_area+=stepx*stepy
            stat=processed_area*100.0/area
            printf ("\rACCA first pass: %.2f%s",stat,"%")
            #print i,"x",j, " ", i+stepx,"x",j+stepy, "s=", processed_area," area=",area

        if need_new_column:
            mask_c=mask_r.copy()
            need_new_column=False
        else:
            mask_c=numpy.hstack((mask_c,mask_r))
    print
    print "INFO: Writing mask"
    gdalData[5].GetRasterBand(1).WriteArray(mask_c)

def main():
    list = sys.argv[1:]
    if len(list) != 2:
        using()
    else:
        metadata=parsing(list)
        metadata["WITH_SHADOW"]=True
        gdalData=load_bands(metadata)
        processing(metadata, gdalData)
        close_bands(gdalData)

    sys.exit(0)

if __name__ == "__main__":
    main()
