# Run recon-all
echo $'\nRunning recon-all***************************************************************************************************\n'
recon-all -s $1 -i $2 -FLAIR $3 -FLAIRpial -3T -all -parallel -openmp 8

subject_id=$1
home=${PWD}

#Transform heat maps into patient space
echo $'\nTransforming Cortial Heat Maps to Patient Space**********************************************************************\n'
for hemi in lh rh
do
	mri_surf2surf --srcsubject fsaverage --trgsubject ${subject_id} --trgsurfreg sphere.reg --hemi ${hemi} --sval /mnt/d/Linux/Freesurfer/Surface_transform/${hemi}.fsaverage.gm.PET_EEGFMRI_DWI_ZSCORE_4D_INTERSECTIONONLY_MEAN.proj-mid.sm10.5pcnt.min1cmsq.caudalmiddlefrontal.mgh --tval ${SUBJECTS_DIR}/${subject_id}/surf/${hemi}.thresh.mgh
	mri_surf2surf --srcsubject fsaverage --trgsubject ${subject_id} --trgsurfreg sphere.reg --hemi ${hemi} --sval /mnt/d/Linux/Freesurfer/Surface_transform/${hemi}.fsaverage.gm.PET_EEGFMRI_DWI_ZSCORE_4D_INTERSECTIONONLY_MEAN.proj-mid.sm10.posthresh.frontal.mgh --tval ${SUBJECTS_DIR}/${subject_id}/surf/${hemi}.heatmap.mgh
done

# Convert heat maps to vtk
echo $'\nConvert Heat Maps to vtk**********************************************************************************************\n'
cd ${SUBJECTS_DIR}/${subject_id}/surf

for hemi in lh rh
do
	mris_convert -c ${hemi}.thresh.mgh ${hemi}.pial ${hemi}.thresh.vtk
	mris_convert -c ${hemi}.heatmap.mgh ${hemi}.pial ${hemi}.heatmap.vtk
done

#Convert vtk to TriSurfField
echo $'\nConvert Heat Maps to .pts, .fac, and data*****************************************************************************\n'
python3 /mnt/c/Users/Matthew/Dropbox\ \(UFL\)/DataProcessing/Pipeline\ Code/Python/SCIRun/vtk_to_TriSurfField.py

mkdir SCIRun
mv *.pts ${PWD}/SCIRun
mv *.fac ${PWD}/SCIRun
mv *_data.txt ${PWD}/SCIRun

echo $'\n\n******************Done!****************\n\n'
cd ${home}

