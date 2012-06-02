#!/usr/bin/env python

from toar import *
from acca import *
from plugin import *

#t=CToar("/mnt/vbox_share/L5171021_02120110811_MTL.txt","/usr/tmp",1)
#t.run()
a=CAcca("/usr/tmp/L5171021_02120110811_MTL.txt","/usr/tmp/mask.tif",1,True,True,False)
a.start()
a.wait()
