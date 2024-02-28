# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 08:43:25 2023

@author: Matthew
"""

import nibabel as nib
import numpy as np
import nrrd

dti = "dti.nii.gz"
img = nib.load(dti)
matrix = img.get_fdata()
#matrix = np.nan_to_num(matrix)
#matrix[matrix > 1] = 0

nrrd.write("tensor.nrrd", matrix)

#FA
fa_img = nib.load("fa.nii.gz")
fa = fa_img.get_fdata()
nrrd.write("fa.nrrd",fa)
#dti_dim = np.asarray(matrix.shape) + 1
#np.savetxt(r"C:\Users\Matthew\Dropbox (UFL)\Projects\NeuroPaceUH3\NeuroPaceLGS_Data_Analysis\UAB\S300-002\Tractography\Cleaned\dti_dim.txt", dti_dim[0:3], delimiter=',',fmt='%d')
'''
#MRtrix dti format
D11 = matrix[:,:,:,0]
D11 = D11.reshape(D11.size,1)
D22 = matrix[:,:,:,1]
D22 = D22.reshape(D22.size,1)
D33 = matrix[:,:,:,2]
D33 = D33.reshape(D33.size,1)
D12 = matrix[:,:,:,3]
D12 = D12.reshape(D12.size,1)
D13 = matrix[:,:,:,4]
D13 = D13.reshape(D13.size,1)
D23 = matrix[:,:,:,5]
D23 = D23.reshape(D23.size,1)

#SCIRun Format
tensor = np.array([D11, D12, D13, D22, D23, D33])
#tensor[tensor < 0] = 0
tensor = np.nan_to_num(tensor)
tensor = np.squeeze(tensor)
tensor = np.transpose(tensor)
print(tensor.shape)
print(np.min(tensor), np.max(tensor))
'''
#np.savetxt(r"C:\Users\Matthew\Dropbox (UFL)\Projects\NeuroPaceUH3\NeuroPaceLGS_Data_Analysis\UAB\S300-002\Tractography\Cleaned\tensor.txt", tensor, delimiter=',',fmt='%1.4e')
