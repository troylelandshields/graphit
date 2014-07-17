import zipfile
import os
from graphit.models import *



def fileiterator(zipf):
  with zipfile.ZipFile(zipf, "r", zipfile.ZIP_STORED) as openzip:
    filelist = openzip.infolist()
    for f in filelist:
        openzip.extract(f, "temp")
