# -*- coding: utf-8 -*-
# Wei Wang (ww8137@mail.ustc.edu.cn)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file, You
# can obtain one at http://mozilla.org/MPL/2.0/.
# ==============================================================================
from sys import getsizeof
import pandas as pd
import numpy
from PIL import Image
import binascii
import errno    
import os

PNG_SIZE = 28

#def getMatrixfrom_pcap(filename,width):
#    with open(filename, 'rb') as f:
#        content = f.read()
#    hexst = binascii.hexlify(content)  
#    fh = numpy.array([int(hexst[i:i+2],16) for i in range(0, len(hexst), 2)])  
#    rn = len(fh)//width
#    fh = numpy.reshape(fh[:rn*width],(-1,width))  
#    fh = numpy.uint8(fh)
#    return fh

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

#paths = [['3_ProcessedSession\TrimedSession\Train', '4_Png\Train'],['3_ProcessedSession\TrimedSession\Test', '4_Png\Test']]
#for p in paths:
#    for i, d in enumerate(os.listdir(p[0])):
#        dir_full = os.path.join(p[1], str(i))
#        mkdir_p(dir_full)
#        for f in os.listdir(os.path.join(p[0], d)):
#            bin_full = os.path.join(p[0], d, f)
#            im = Image.fromarray(getMatrixfrom_pcap(bin_full,PNG_SIZE))
#            png_full = os.path.join(dir_full, os.path.splitext(f)[0]+'.png')
#            im.save(png_full)




Location_Input = r'/one.csv'
headers = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8']
dtypes = {'col1': 'str', 'col2': 'str', 'col3': 'int', 'col4': 'int', 'col5': 'float', 'col6': 'float', 'col7': 'float', 'col8': 'float'}
data = pd.read_csv("one.csv", header=None, names=headers, dtype=dtypes)
padding = numpy.zeros(752, dtype =int)


def trsf(nrow):
    temperature = binascii.hexlify(data.iloc[nrow,4])
    humidity = binascii.hexlify(data.iloc[nrow,5])
    light = binascii.hexlify(data.iloc[nrow,6])
    voltage = binascii.hexlify(data.iloc[nrow,7])
    temperature = numpy.array([int(temperature[i:i+2],16) for i in range(0, len(temperature), 2)])
    humidity = numpy.array([int(humidity[i:i+2],16) for i in range(0, len(humidity), 2)])
    light = numpy.array([int(light[i:i+2],16) for i in range(0, len(light), 2)])
    voltage = numpy.array([int(voltage[i:i+2],16) for i in range(0, len(voltage), 2)])
    re = numpy.array(temperature)
    re = numpy.concatenate((re,humidity), axis= None)
    re = numpy.concatenate((re,light), axis= None)
    re = numpy.concatenate((re,voltage), axis= None)
    return re

def mkimg(path,name):
    mtr = numpy.concatenate((trsf(name), padding), axis= None)
    mtr = numpy.uint8(mtr)
    mtr = mtr.reshape(28,28)
    im = Image.fromarray(mtr)
    im.save(path+str(name)+".png")

mkdir_p("data\\1")
for i in range(int(data.shape[0])):
    mkimg("data\\1\\",i)

