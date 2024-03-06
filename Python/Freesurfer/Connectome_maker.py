# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 16:07:45 2023

@author: Matthew
"""
#For use in the working directory
import nibabel
import nibabel.processing
import numpy as np
import pandas as pd

#Load lookup table
lookup = pd.read_csv(r'Z:\Dropbox (UFL)\CT DBS Human\CENTURY S Patients\connectome_lookup.csv',index_col=False)
#%%
#Get patient ***TODO: Replace this with reading a file with a list of subjects***
filepath = r'Z:/Dropbox (UFL)/CT DBS Human/CENTURY S Patients/pDummy_conectome/pDummy/'

seg_files = lookup['Filename'].unique()
#seg_dirs = lookup['Path'].unique()
seg_dirs = lookup['Path'][lookup['Filename'] == seg_files[0]].unique()[0]

#Load HCP first always. This will be the reference
HCP = nibabel.load(filepath + 'Segmentations/' +seg_dirs + '/' + seg_files[0])
HCP_data = HCP.get_fdata()
main_index = np.array(lookup['Index'][lookup['Filename'] == seg_files[0]])
local_index = np.array(lookup['File Index'][lookup['Filename'] == seg_files[0]])

All_data = HCP_data.copy()

for i in range(0,len(local_index)):
   All_data[HCP_data == local_index[i]] = int(main_index[i])
#%%
#Rest of the data
for file in seg_files: 
    seg_dirs = lookup['Path'][lookup['Filename'] == file].unique()[0]
    main_index = np.array(lookup['Index'][lookup['Filename'] == file])
    local_index = np.array(lookup['File Index'][lookup['Filename'] == file])
    
    img = nibabel.load(filepath + 'Segmentations/' + seg_dirs + '/' + file)
    img_resamp = nibabel.processing.resample_from_to(img, HCP,order=0)
    img_data = img_resamp.get_fdata()
    for j in range(0,len(local_index)):
        img_data[img_data == local_index[j]] = int(main_index[j])

    All_data[img_data != 0] = img_data[img_data != 0]

#%%
All_to_nii = nibabel.Nifti1Image(All_data, HCP.affine, HCP.header)
nibabel.save(All_to_nii, filepath + 'HCP_parc_all.nii.gz')
#%%
'''
#Load HCP and grab all other nifti volumes to add
HCP = nibabel.load(glob.glob(r'./*HCP.nii.gz')[0])
files = glob.glob(r'./*[!HCP].nii.gz')

#Re-label each volume to match with HCP data
HCP_data = HCP.get_fdata()
count = int(np.max(HCP_data)) #highest value in labelmap
All_data = HCP_data.copy()
for file in files:
    count = count + 1
    filename = file.split('/')[1].split('.nii')[0]
    img = nibabel.load(file)
    img_resamp = nibabel.processing.resample_from_to(img, HCP,order=1)
    
    img_data = img_resamp.get_fdata()
    All_data[img_data != 0] = count
    #All_data = np.add(All_data,img_data)
    img_to_nii =  nibabel.Nifti1Image(img_data, img_resamp.affine, img_resamp.header)
    nibabel.save(img_to_nii, filename+'_resamp.nii.gz')
    
#Save as new nifti
All_to_nii = nibabel.Nifti1Image(All_data, HCP.affine, HCP.header)
nibabel.save(All_to_nii, 'HCP_parc_all.nii.gz')
'''