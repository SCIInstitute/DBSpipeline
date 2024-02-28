# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 11:24:18 2024

@author: Matthew
"""
import glob
import nibabel.freesurfer.io as fsio
import scipy.io as scio

files = glob.glob(r'*.HCPMMP1.*')

for file in files:
    filename = file.split('\\')[-1] + '.mat'
    labels, ctab, names = fsio.read_annot(file)
    label_data = ctab[labels, 4]
    scio.savemat(filename, {"labels_tab" : label_data, "labels": labels, "names" : names })