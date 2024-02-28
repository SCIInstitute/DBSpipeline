# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:20:03 2023

@author: Matthew
"""

import nibabel as nib

dwi = ["DWI_up.nii.gz", "DWI_down.nii.gz"]


slice_count = {}
for file in dwi:
    img = nib.load(file)
    header_info = img.header
    dims = header_info["dim"][1:5]
    slice_count[file] = dims[2]
dwi_min = min(slice_count.values())


for file in dwi:
    n = 0 #number of slices to remove
    img = nib.load(file)
    img_matrix = img.get_fdata()
    header_info = img.header

    # Check number of slices
    dims = header_info["dim"][1:5]
    print(file, 'slice count:', dims[2])
    if dims[2] > dwi_min:
        n = dims[2] - dwi_min
    if (dims[2] - n) % 2 != 0:
        n = n + 1
    if n != 0:
        print('Removing',n,'slice(s)')
        header_info["dim"][3] = dims[2] - n
        affine = header_info.get_best_affine()
        if affine[2,2] < 0:
            img_matrix = img_matrix[:,:,:-n,:] #first slice is the head
        else:
            img_matrix = img_matrix[:,:,n:,:] #first slice is the neck

        new_nifti = nib.Nifti1Image(img_matrix, affine, header_info)
        nib.save(new_nifti, file)
    else:
        print('Leave as is')