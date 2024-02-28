import nibabel as nib

dwi = ["DWI_up.nii.gz", "DWI_down.nii.gz"]

for file in dwi:
    img = nib.load(file)
    img_matrix = img.get_fdata()
    header_info = img.header

    # Check number of slices
    dims = header_info["dim"][1:5]
    print(file, 'slice count:', dims[2])
    if dims[2] % 2 != 0:
        print('Removing a slice')
        header_info["dim"][3] = dims[2] - 1
        affine = header_info.get_best_affine()
        if affine[2,2] < 0:
            img_matrix = img_matrix[:,:,:-1,:] #first slice is the head
        else:
            img_matrix = img_matrix[:,:,1:,:] #first slice is the neck

        new_nifti = nib.Nifti1Image(img_matrix, affine, header_info)
        nib.save(new_nifti, file)
    else:
        print('Leave as is')
