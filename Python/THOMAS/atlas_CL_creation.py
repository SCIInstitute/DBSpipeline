import nibabel as nib
import numpy as np
import os

for hemi in ['left', 'right']:
    nuclei_data = []
    atlas_old = nib.load('atlas_'+hemi+'_resamp.nii.gz')
    data = atlas_old.get_fdata() #get matrix

    atlas_new = np.zeros(data.shape, dtype=np.int16) #New atlas

    x, y, z = np.where(data == 18) #threshold out VPM
    VPM = np.zeros(data.shape, dtype=np.int16)
    VPM[x, y, z] = 18 #no further modification
    atlas_new[x, y, z] = 18 #add VPM to atlas_CL
    x, y, z = np.where(data == 17) #threshold out CL
    CL = np.zeros(data.shape, dtype=np.int16)
    for i in range(len(x)): #dilate CL
        CL[x[i]-2:x[i]+2, y[i]-2:y[i]+2, z[i]-2:z[i]+2] = 17
        atlas_new[x[i]-2:x[i]+2, y[i]-2:y[i]+2, z[i]-2:z[i]+2] = 17 #add dilated CL to atlas

    path = os.getcwd()
    nuclei_files = os.listdir(path+'/'+hemi+'/Resample')

    for nuc_num in range(20):
        print(nuc_num)
        for nuc in nuclei_files:
            print(nuc)
            if nuc.startswith(str(nuc_num)+"-"):
                nuc_load = nib.load(path+'/'+hemi+'/Resample/'+nuc)
                nucleus_data = nuc_load.get_fdata()

                nuclei = np.zeros(nucleus_data.shape, dtype=np.int16)
                if nuc_num == 1: #invert thalamus
                    x, y, z = np.where(nucleus_data == 0)
                    for i in range(len(x)):
                        if CL[x[i],y[i],z[i]] != 0:
                            CL[x[i],y[i],z[i]] = 0
                            atlas_new[x[i],y[i],z[i]] = 0
                    x, y, z = np.where(nucleus_data == 1)
                    for i in range(len(x)):#add thalamus to full atlas
                        if atlas_new[x[i],y[i],z[i]] == 0:
                            nuclei[x[i],y[i],z[i]] = 1
                            atlas_new[x[i],y[i],z[i]] = 1

                else:
                    x, y, z = np.where(nucleus_data == 1) #Boolean remove
                    for i in range(len(x)):
                        if atlas_new[x[i],y[i],z[i]] != 0:
                            CL[x[i],y[i],z[i]] = 0
                            nuclei[x[i],y[i],z[i]] = nuc_num
                            atlas_new[x[i],y[i],z[i]] = nuc_num

                nuclei_data.append(nuclei)

    """
    for nuc in nuclei:
        nuc_load = nib.load(path+'/'+hemi+'/Resample/'+nuc)
        nuc_num = nuc.split('-')
        nuc_num = int(nuc_num[0])
        nucleus_data = nuc_load.get_fdata()

        nuclei = np.zeros(nucleus_data.shape, dtype=np.int16)
        if nuc_num == 1: #invert thalamus
            x, y, z = np.where(nucleus_data == 0)
            for i in range(len(x)):
                if CL[x[i],y[i],z[i]] != 0:
                    CL[x[i],y[i],z[i]] = 0
                    atlas_new[x[i],y[i],z[i]] = 0
            x, y, z = np.where(nucleus_data == 1)
            for i in range(len(x)):#add thalamus to full atlas
                if atlas_new[x[i],y[i],z[i]] == 0:
                    nuclei[x[i],y[i],z[i]] = 1
                    atlas_new[x[i],y[i],z[i]] = 1
        else:
            x, y, z = np.where(nucleus_data == 1) #Boolean remove
            for i in range(len(x)):
                if atlas_new[x[i],y[i],z[i]] != 0:
                    CL[x[i],y[i],z[i]] = 0
                    nuclei[x[i],y[i],z[i]] = nuc_num
                    atlas_new[x[i],y[i],z[i]] = nuc_num

        if nuc_num != 4567:
            nuclei_data.append(nuclei)
            print(nuc)
    """
    nuclei_data.append(VPM)
    nuclei_data.append(CL)

    atlas_new = np.zeros(atlas_new.shape, dtype=np.int16)
    for i in range(len(nuclei_data)):
        nuclei = nuclei_data[len(nuclei_data)-1-i]
        selected_data = np.bitwise_and(atlas_new == 0, nuclei > 0)
        atlas_new[selected_data] = nuclei[selected_data]

    New_CL = nib.Nifti1Image(CL, atlas_old.affine, atlas_old.header)
    New_VPM = nib.Nifti1Image(VPM, atlas_old.affine, atlas_old.header)
    atlas_CL = nib.Nifti1Image(atlas_new, atlas_old.affine, atlas_old.header)
    nib.save(New_CL, 'CL_'+hemi+'.nii.gz')
    nib.save(New_VPM, 'VPM_'+hemi+'.nii.gz')
    nib.save(atlas_CL, 'atlas_CL_'+hemi+'.nii.gz')
