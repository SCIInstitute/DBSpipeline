#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 13:30:09 2022

@author: jcagle
"""

import numpy as np
from scipy.stats import norm
from scipy import ndimage
import nibabel as nib

kernel = np.zeros((5,5,5))
centerIndex = np.array([(kernel.shape[0]-1)/2, (kernel.shape[1]-1)/2, (kernel.shape[2]-1)/2])

for x in range(kernel.shape[0]):
    for y in range(kernel.shape[1]):
        for z in range(kernel.shape[2]):
            kernel[x,y,z] = SPU.rssq(np.array([x,y,z])-centerIndex, axis=0)
            kernel[x,y,z] = norm.pdf(kernel[x,y,z])

kernel = np.abs(kernel / np.max(kernel))
normalizedKernel = kernel / np.sum(kernel)

Directory = "/home/jcagle/Storage/Imaging/SEG3D/"
raw = nib.load(Directory+"Threshold17TO17_atlas_left_resamp.nii.gz")

img = raw.get_fdata()
dialatedImg = ndimage.convolve(img, normalizedKernel, mode='constant', cval=0.0)
dialatedImg = dialatedImg > np.percentile(dialatedImg,100) * 0.05

raw = nib.Nifti1Image(dialatedImg, affine=raw.header.get_best_affine(), header=raw.header)
nib.save(raw, Directory+"testDialation.nii.gz")
