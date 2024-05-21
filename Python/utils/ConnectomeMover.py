# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:09:29 2024

@author: Matthew
"""

import os
import subprocess
import shutil
import pandas as pd

parser = argparse.ArgumentParser(description='Inputs')
parser.add_argument('--subject',action='store',dest='subject',default=0)

#parser.add_argument('--left_ROI',action='store',dest='ROI_list_left',type=int,default=np.NaN)
#parser.add_argument('--right_ROI',action='store',dest='ROI_list_right',type=int,default=np.NaN)
#parser.add_argument('--matrix',action='store',dest='c_matrix',default=0)
args = parser.parse_args()

rel_path1 = "Connectome"
rel_path2 = "Tractography"

connectomeMakerDir = os.path.join(os.environ["DATADIR"],  args.subject, rel_path1)
stimVolumeDir = os.path.join(os.environ["DATADIR"],  args.subject, "SCIRun_MRtrix/Stim_volumes")
#connectomeMakerDir = r"Z:\Dropbox (UFL)\CT DBS Human\CENTURY S Patients\p102 (44)\MRtrix\Connectome\Stim"
#stimVolumeDir = r"Z:\Dropbox (UFL)\CT DBS Human\CENTURY S Patients\p102 (44)\MRtrix\SCIRun\Stim_volumes"

allStimVolume = os.listdir(stimVolumeDir)

BilateralStim = pd.read_csv(os.path.join(stimVolumeDir, "BilateralStim.csv"), delimiter=",")
print(BilateralStim.keys())
for i in BilateralStim.index:
    os.chdir(stimVolumeDir)

    for side in ["Left", "Right"]:
        # Convert NRRD first here.
        #print("python3 /mnt/d/Github/DBSpipeline/Python/MRtrix/NRRDConverter.py --NRRD " + stimVolumeDir + os.path.sep + BilateralStim[side][i])
        subprocess.call('python3 ' + os.path.join(os.environ["CODEDIR"], "Python/MRtrix/NRRDConverter.py") + ' --NRRD "' + stimVolumeDir + os.path.sep + BilateralStim[side][i] + '"', shell=True)
        shutil.copy(os.path.join(stimVolumeDir, BilateralStim[side][i].replace(".nrrd",".nii.gz")), os.path.join(connectomeMakerDir, "temp_" + side + ".nii.gz"))
    
    # run HCP_to_subject
    
    os.chdir(connectomeMakerDir)
    subprocess.call('python3 "' + os.path.join(os.environ["CODEDIR"], "Python/Freesurfer/Connectome_maker.py") + ' --subject '+arg.subject+'"', shell=True)
    
    shutil.copy(connectomeMakerDir + os.path.sep + "HCP_parc_all.nii.gz", connectomeMakerDir + os.path.sep + "HCP_parc_all" + "_" + str(i) + ".nii.gz")

    
