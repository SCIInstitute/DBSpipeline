#!/bin/bash

# preprocessing steps

#1) Ants rigid precise

# 2) parallel steps

Thomas
freesurfer (HCP) (fs_heatmap)
ANTs registrations (nonlin warp) moves things to MNI space
  contigency for atlases that are static
  
# 3) MRtrix tractography
  preproc_gpu.sh
  


# then Connectomics.  making this part of the experiments?
#calculate_connectome.py


