#!/usr/bin/env python
import sys
import osgeo.gdal as gdal
import numpy
import os
import time
import math

#printf from C
def printf(fstr,*param):
    string=fstr % param
    sys.stdout.write (string)
    sys.stdout.flush()

#using
def using():
    print "Using:\n\t", sys.argv[0],  "<metafile> <path>"

#Calculate Earth Sun distance form date (YYYY-mm-dd)
def ESD(date):
    days=[1,15,32,46,60,74,91,106,121,135,152,166,182,192,213,227,242,258,274,288,305,319,335,349,365]
    dist=[.98331,.98365,.98536,.98774,.99084,.99446,.99926,1.00353,1.00756,1.01087,1.01403,1.01577,1.01667,1.01646,1.01497,1.01281,1.00969,1.00566,1.00119,.99718,.99253,.98916,.98608,.98426,.98333]
    nday=int(time.strftime("%j",time.strptime(date,"%Y-%m-%d")))
    DIST=numpy.interp(nday,days,dist)
    return DIST

def toar(band,metadata, i):
    #Calculate radiance
    band[0]=((metadata["LMAX_BAND"+str(i)]-metadata["LMIN_BAND"+str(i)])/(metadata["QCALMAX_BAND"+str(i)]-metadata["QCALMIN_BAND"+str(i)]))*(band[0]-metadata["QCALMIN_BAND"+str(i)])+metadata["LMIN_BAND"+str(i)]
    #ESUN for 2,3,4,5 bands
    ESUN={"7":{2:1812.,3:1533.,4:1039.,5:230.8},"5":{2:1826.,3:1554.,4:1036.,5:215.0}}
    #Thermal band calibration metadataants
    TBCC={"7":{"K1":666.09,"K2":1282.71},"5":{"K1":607.76,"K2":1260.56}}
    #cosine of THETA
    COSTHETA=metadata["cos(THETA)"]
    DIST=ESD(metadata["date"])
    if i<6:
        band[0]=(numpy.pi*band[0]*math.pow(DIST,2))/(COSTHETA*ESUN[metadata["sat"]][i])
    else:
        band[0]=TBCC[metadata["sat"]]["K2"]/numpy.log(TBCC[metadata["sat"]]["K1"]/band[0]+1)

#Parsing metafile
def parsing(list):
    metadata={}
    path=list[0]
    metadata["METAFILE"]=path
    metadata["PATH"]=list[1]
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


def processing(metadata,gdalData):
    format="GTiff"
    driver=gdal.GetDriverByName(format)
    gdalDataOut=[]
    projection=[]
    transform=[]
    xsize=[]
    ysize=[]

    for i in range(0,5):
        projection.append(gdalData[i].GetProjection())
        transform.append(gdalData[i].GetGeoTransform())
        xsize.append(gdalData[i].RasterXSize)
        ysize.append(gdalData[i].RasterYSize)
        drvMeta=driver.GetMetadata()

        if drvMeta.has_key( gdal.DCAP_CREATE ) and drvMeta[ gdal.DCAP_CREATE ] == "YES":
            gdalDataOut.append(driver.Create(os.path.join(metadata["PATH"],os.path.basename(metadata["BAND"+str(i+2)+"_FILE_NAME"])), xsize[i], ysize[i], 1, gdal.GDT_Float32))
            gdalDataOut[i].SetProjection(projection[i])
            gdalDataOut[i].SetGeoTransform(transform[i])
        else:
            print "INFO: Driver %s does not support Create() method." % format
            sys.exit(-1)

    for band in gdalDataOut:
        if band is None:
            print "ERROR: Missing one or more band."
            sys.exit(-1)
    for band_i in range(0,5):
        step=2000
        x=gdalData[band_i].RasterXSize
        y=gdalData[band_i].RasterYSize
        area=x*y
        processed_area=0
        need_new_row=True
        need_new_column=True
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
                band=[gdalData[band_i].ReadAsArray(i,j,stepx,stepy).astype(numpy.float32)]

                toar(band, metadata, band_i+2)

                if need_new_row:
                    band_r=[]
                    band_r.append(band[0].copy())
                    need_new_row=False
                else:
                    band_r[0]=numpy.vstack((band_r[0],band[0]))
                processed_area+=stepx*stepy
                stat=processed_area*100.0/area
                printf ("\rINFO: Toar, step %i of 5: %.2f%s",band_i+1,stat,"%")

            if need_new_column:
                band_c=[]
                band_c.append(band_r[0].copy())
                need_new_column=False
            else:
                band_c[0]=numpy.hstack((band_c[0],band_r[0]))
        print
        print "INFO: Writing data"
        gdalDataOut[band_i].GetRasterBand(1).WriteArray(band_c[0])
        #time.sleep(30)
        print "INFO: Closing band"
        gdalDataOut[band_i]=None
        band_r=[]
        band_c=[]

def save_metadata(metadata):
    file=open(os.path.join(metadata["PATH"],os.path.basename(metadata["METAFILE"])),"w")
    if file is None:
        print "ERROR: Can`t write data to metafile"
        sys.exit(-1)

    for key in metadata:
        if ((key=="sat")|\
           (key=="BAND2_FILE_NAME")|\
           (key=="BAND3_FILE_NAME")|\
           (key=="BAND4_FILE_NAME")|\
           (key=="BAND5_FILE_NAME")|\
           (key=="BAND6_FILE_NAME")):
            s="{0}={1}\n".format(key,metadata[key],)
            file.write(s)
    file.close()

def main(list):
    if len(list) != 2:
        using()
        return False
    else:
        metadata=parsing(list)
        gdalData=load_bands(metadata)
        processing(metadata, gdalData)
        save_metadata(metadata)
        close_bands(gdalData)
    return True

if __name__ == "__main__":
    if (main(sys.argv[1:])):
        sys.exit(0)
    sys.exit(-1)
