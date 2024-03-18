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
import argparse

parser = argparse.ArgumentParser(description='Inputs')
parser.add_argument('--subject',action='store',dest='subject',default=0)
parser.add_argument('--lookup',action='store',dest='lookup_dir',default=0)
#parser.add_argument('--filepath',action='store',dest='filepath',default=0)
args = parser.parse_args()
subject = args.subject

#Load lookup table
lookup = pd.read_csv(args.lookup_dir,index_col=False)

#%%

#Get patient
#filepath = args.filepath + '/' + subject + '/'
filepath = subject + '/'

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
        
#Rest of the data
for file in seg_files: 
    seg_dirs = lookup['Path'][lookup['Filename'] == file].unique()[0]
    main_index = np.array(lookup['Index'][lookup['Filename'] == file])
    local_index = np.array(lookup['File Index'][lookup['Filename'] == file])
    
    img = nibabel.load(filepath + 'Segmentations/' + seg_dirs + '/' + file)
    img_resamp = nibabel.processing.resample_from_to(img, HCP,order=0)
    img_data = img_resamp.get_fdata()
    data_add = img_data.copy()
    for j in range(0,len(local_index)):
        data_add[img_data == local_index[j]] = int(main_index[j])

    All_data[data_add != 0] = data_add[data_add != 0]

All_data = All_data.astype(int)
All_to_nii = nibabel.Nifti1Image(All_data, HCP.affine, HCP.header)
nibabel.save(All_to_nii, filepath + 'Connectome/HCP_parc_all_lookup.nii.gz')

#Create Key for MRtrix image
mrtrix_key = {}
mrtrix_key['Lookup Index'] = np.unique(All_data)[1:].tolist()
mrtrix_key['MRtrix Index'] = list(range(1,len(np.unique(All_data)[1:].tolist())+1))

mrtrix_data = All_data.copy()
for i in range(0,len(mrtrix_key['Lookup Index'])):
    mrtrix_data[All_data == mrtrix_key['Lookup Index'][i]] = mrtrix_key['MRtrix Index'][i]
    
mrtrix_to_nii = nibabel.Nifti1Image(mrtrix_data, HCP.affine, HCP.header)
nibabel.save(All_to_nii, filepath + 'Connectome/HCP_parc_all.nii.gz')
mrtrix_save = pd.DataFrame(data=mrtrix_data)
mrtrix_save.to_csv(filepath + 'Connectome/MRtrix_index_key.csv')
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