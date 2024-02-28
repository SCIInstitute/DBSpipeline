subject=$1

module load freesurfer/6.0.0
SUBJECTS_DIR=/home/mphook/blue_butsonc/mphook/freesurfer/SimNIBS/FS_Subjects
cd $SUBJECTS_DIR/$subject/surf

mri_surf2vol --o thresh.nii.gz --subject $subject --so lh.pial lh.thresh.mgh --so rh.pial rh.thresh.mgh