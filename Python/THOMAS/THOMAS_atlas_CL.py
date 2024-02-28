# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 10:15:05 2023

@author: Matthew
"""

import nibabel as nib
import numpy as np
from scipy import ndimage
import os

# Generate kernals for CL Dilation
kernal_square = ndimage.generate_binary_structure(3,2)
kernal_diag = ndimage.generate_binary_structure(3,1)

for hemi in ['left', 'right']:
    nuclei = os.listdir(os.getcwd()+r'/'+hemi+'/Resample')
    Thalamus = nib.load(os.getcwd()+r'/'+hemi+'/Resample/1-THALAMUS_resamp.nii.gz')
    thal_data = Thalamus.get_fdata()
    
    atlas_old = nib.load('atlas_'+hemi+'_resamp.nii.gz')
    data = atlas_old.get_fdata()
    
    atlas_new = np.zeros(data.shape, dtype=np.int16) #New atlas
    atlas_new[thal_data==1] = 1

    x, y, z = np.where(data == 18) #threshold out VPM
    VPM = np.zeros(data.shape, dtype=np.int16)
    VPM[x, y, z] = 1 #just for dilation
    VPM_square = ndimage.binary_dilation(VPM, structure=kernal_diag).astype(VPM.dtype)
    VPM_sphere = ndimage.binary_dilation(VPM_square, structure=kernal_diag).astype(VPM.dtype)
    VPM_new = VPM_sphere + thal_data
    
    x, y, z = np.where(data == 17)
    CL = np.zeros(data.shape, dtype=np.int16)
    CL[x,y,z] = 1 #just for dilation
    CL_square = ndimage.binary_dilation(CL, structure=kernal_square).astype(CL.dtype)
    #CL_sphere = ndimage.binary_dilation(CL_square, structure=kernal_diag).astype(CL.dtype)
    CL_dilate = CL_square + thal_data
    atlas_new[CL_dilate==2] = 17 #add only where in thalamus bounds
    
    for nuc in nuclei:
        nuc_num = int(nuc.split('-')[0])
        if nuc_num > 20:
            continue #skip VL conglomeration
        if nuc_num == 1:
            continue #skip Thalamus bounds
        if nuc_num == 11:
            continue #skip CM
        nuc_img = nib.load(os.getcwd()+r'/'+hemi+'/Resample/'+nuc)
        nuc_data = nuc_img.get_fdata()
        atlas_new[nuc_data==1] = nuc_num
    
    # Make special allowance for relevant nuclei
    CM = nib.load(os.getcwd()+r'/'+hemi+'/Resample/11-CM_resamp.nii.gz')
    CM_data = CM.get_fdata()
    atlas_new[VPM_new == 2] = 18 #prioritize CM over VPM
    atlas_new[CM_data == 1] = 11
    
    atlas_CL = nib.Nifti1Image(atlas_new, atlas_old.affine, atlas_old.header)
    nib.save(atlas_CL, 'atlas_CL_'+hemi+'.nii.gz')
    
    # Save out relevant nuclei
    for nuc in nuclei:
        nuc_num = int(nuc.split('-')[0])
        nuc_name = nuc.split('-')[1].split('_')[0]
        if nuc_num in [7,11,12]:
            x,y,z = np.where(atlas_new == nuc_num)
            nuc_out = np.zeros(atlas_new.shape, dtype=np.int16)
            nuc_out[x,y,z] = nuc_num
            nuc_out_img = nib.Nifti1Image(nuc_out,atlas_old.affine, atlas_old.header)
            nib.save(nuc_out_img, nuc_name+'_'+hemi+'.nii.gz')
    
    # Save out anything new
    x,y,z = np.where(atlas_new == 17)
    CL_new = np.zeros(atlas_new.shape, dtype=np.int16)
    CL_new[x,y,z] = 17
    CL_out = nib.Nifti1Image(CL_new,atlas_old.affine, atlas_old.header)
    nib.save(CL_out, 'CL_'+hemi+'.nii.gz')
    
    x,y,z = np.where(atlas_new == 18)
    VPM_new = np.zeros(atlas_new.shape, dtype=np.int16)
    VPM_new[x,y,z] = 18
    VPM_out = nib.Nifti1Image(VPM_new,atlas_old.affine, atlas_old.header)
    nib.save(VPM_out, 'VPM_'+hemi+'.nii.gz')
    
    
    
        
    