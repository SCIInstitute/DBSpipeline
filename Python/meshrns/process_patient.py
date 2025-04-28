# Strip meshing pipeline
# Chantel Charlebois
# 8/22/2022

import os
import meshrns
import argparse
import glob

parser = argparse.ArgumentParser(description='Create Meshed RNS Strip Electrodes for a Specific Subject')
parser.add_argument('--subject', help='Subject ID')
args = parser.parse_args()
subject_path = os.path.join("Z:\meshrns\Subjects",args.subject)

print('Creating Cortical Strips for',args.subject)

# set up directories
# CHANGE TO YOUR DIRECTORIES
sci_run_bin = os.path.normpath(r'"C:\Program Files\SCIRun_ZZZ\SCIRun_5.0\bin\SCIRun.exe"') # scirun binary directory
# sci_run_bin = os.path.join("C:","Program Files","SCIRun_5.0","bin") + "\SCIRun.exe"
subject_dir = os.path.normpath(subject_path) # subject directory where side_centroids.mat file, smooth_gm.stl, and strip orientation files exist
scirun_net_dir = os.path.normpath("Z:\Github\DBSpipeline\SRNetworks\meshrns") # directory with scirun networks
# matlab script directory
os.environ["ECOG_matlab_dir"] = os.path.normpath("Z:\Github\DBSpipeline\Matlab\meshrns") # directory with matlab scripts

# Mesh the grid
# If final mesh of grid has holes or does not mesh with tetgen, change the triangulation radius
for electrode in ["L_centroids.mat","R_centroids.mat"]:
    meshrns.grid_mesh(subject_dir, scirun_net_dir, sci_run_bin, 10, electrode)
    if "L" in electrode.split('_'):
        os.rename(os.path.join(subject_dir,'FINAL_GRID.bdl'),os.path.join(subject_dir,'Left_strip.bdl'))
    else:
        os.rename(os.path.join(subject_dir,'FINAL_GRID.bdl'),os.path.join(subject_dir,'Right_strip.bdl'))
    # if "L" in electrode.split('_'):
    #     side = "Left"
    # else:
    #     side = "Right"

    # os.mkdirs(os.path.join(subject_dir,side), exist_ok=True)
    # move_files = glob.glob('*.vtk') + glob.glob('*.fld') + glob.glob('*.pts') + glob.glob('*.mat')


