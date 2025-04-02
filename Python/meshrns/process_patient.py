# Strip meshing pipeline
# Chantel Charlebois
# 8/22/2022

import os
import meshrns

# set up directories
# CHANGE TO YOUR DIRECTORIES
sci_run_bin = os.path.normpath(r'"C:\Program Files\SCIRun_ZZZ\SCIRun_5.0\bin\SCIRun.exe"') # scirun binary directory
# sci_run_bin = os.path.join("C:","Program Files","SCIRun_5.0","bin") + "\SCIRun.exe"
subject_dir = os.path.normpath("Z:\meshrns_integrated\subject_directory") # subject directory where centroids.txt file and smooth_gm.stl file exist
scirun_net_dir = os.path.normpath("Z:\meshrns_integrated\scirun_nets") # directory with scirun networks
# matlab script directory
os.environ["ECOG_matlab_dir"] = os.path.normpath("Z:\meshrns_integrated\matlab_scripts") # directory with matlab scripts

# Mesh the grid
# If final mesh of grid has holes or does not mesh with tetgen, change the triangulation radius
for electrode in ["L_centroids.mat","R_centroids.mat"]:
    meshrns.grid_mesh(subject_dir, scirun_net_dir, sci_run_bin, 10, electrode)
    if "L" in electrode.split('_'):
        os.rename(os.path.join(subject_dir,'FINAL_GRID.bdl'),os.path.join(subject_dir,'Left_strip.bdl'))
    else:
        os.rename(os.path.join(subject_dir,'FINAL_GRID.bdl'),os.path.join(subject_dir,'Right_strip.bdl'))


