#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 14:26:54 2020

@author: anjakatzenberger
"""
import subprocess
import os
###########################################################
#                           LANDMASK                      #
#                          18.06.2020                     #
###########################################################
# ceils fx/sftlf variable to create landmasks


dir = "/pf/b/b381146"

files = os.listdir(os.sep.join((dir,"landmasks")))
files.remove('.DS_Store')

for file in files:
    file_dir = os.sep.join(("~","landmasks", file))
    print(file_dir)
    print(file)
    table = file.split('_')[1]
    vbl = file.split('_')[0]
    model = file.split('_')[2]
    
    
    outdir_ceil = os.sep.join(("~", "landmasks_masks",'_'.join((table, vbl, model, "masked.nc"))))
    cdo_cmd_ceil = ' '.join(("cdo expr,'mask=ceil(sftlf/100);' ", file, outdir_ceil))
    
    subprocess.check_call(cdo_cmd_ceil, shell=True)
    