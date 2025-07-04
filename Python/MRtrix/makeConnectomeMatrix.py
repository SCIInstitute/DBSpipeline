# -*- coding: utf-8 -*-
"""


usage:

python3 makeConnectomeMatrix.py --profile Allprofile.json --assigment assignment_end_voxels


"""



import pandas as pd
import os
import numpy as np
import argparse
import json
import subprocess

default_assignment="assignment_radial_search"
default_radius=3
default_distance=0
hcp_pattern="HCP_parc_all_"

def build_parser():
  parser = argparse.ArgumentParser(
                prog = "makeConnectomeMatrix",
                description = "makes connectome matrix from compiled nifti",
                epilog="output: connectome matrix"
                )

  # This will be implemented as rollout broadens
  parser.add_argument("-p", "--profile", required=True,
                      help="profile filename",
                      dest="profile")

  parser.add_argument("-a", "--assignment", required=False,
                      help="Assignment method for MRtrix.  found in: https://mrtrix.readthedocs.io/en/dev/reference/commands/tck2connectome.html#options",
                      dest="assignment")
                      
  parser.add_argument("-r", "--radius", required=False,
                      help="Assignment radius for MRtrix.  works only with assignment_radial_search",
                      dest="radius", default=default_radius, type=int)
                      
  parser.add_argument("-d", "--distance", required=False,
                      help="Assignment max distance for MRtrix.  works only with assignment_reverse_search and assignment_forward_search",
                      dest="distance", default=default_distance, type=int)
                      
  parser.add_argument("-s", "--stim", required=False,
                      help="include stimulations",
                      action = "store_true", dest="stim")
  parser.add_argument("-f", "--force", required=False,
                      help="force rerun/rewrite of the pipeline",
                      action = "store_true", dest="rerun")
  return parser

def run_connectome_matrix(connectome_matrix, input_file, lookup_table,  experiment, profile, assignment, radius, distance):

  rerun = True
  
  subject= profile["subject"]
  connectomePath = profile["connectomePath"]
  fibertractPath = profile["fibertractPath"]
  cleantractPath = profile["cleantractPath"]
   
  file_dir = profile["tractographyPath"]
  
  
  apppath=""
  if os.environ["SYSNAME"] == "hipergator":
  # hard coded for now. There should be a better way to do this. ugh
    apppath="/apps/mrtrix/3.0.3/bin/"
  
  cl_call1 = [apppath+"mrtransform",  "-linear", os.path.join(cleantractPath, "ACPC_to_b0.txt"), input_file, os.path.join(connectomePath, hcp_pattern+"b0space.nii.gz")]
  if rerun:
    cl_call1.append("-force")
  print(" ".join(cl_call1))
  subprocess.run(cl_call1)
  
  
  print(connectome_matrix)
  print(assignment)
  cl_call2 = [apppath+"tck2connectome", os.path.join(fibertractPath, "whole_brain_fibers.tck"), os.path.join(connectomePath, hcp_pattern+"b0space.nii.gz"), connectome_matrix,  "-tck_weights_in", os.path.join(fibertractPath, "sift2_weights.txt"),   "-keep_unassigned",  "-out_assignments", os.path.join(cleantractPath, "assignments_" + experiment + ".txt"), "-symmetric" ]
  if rerun:
    cl_call2.append("-force")
  
  cl_call2.append("-"+assignment)
  if assignment == "assignment_radial_search":
    cl_call2.append(str(radius))
  elif assignment == "assignment_forward_search" or assignment == "assignment_reverse_search":
    cl_call2.append(str(distance))
    
      #-scale_invlength \
      #-scale_invnodevol
  print(" ".join(cl_call2))
  subprocess.run(cl_call2)
  
  return


def main():

  parser = build_parser()
  args = parser.parse_args()
#print(args.subject, args.ROI_list_left, args.ROI_list_right)

  with open(args.profile, 'r') as js_file:
    profile = json.load(js_file)
    
  experiment = profile["experiment"]
  connectomePath = profile["connectomePath"]
  connectome_matrix=os.path.join(connectomePath, "connectome_matrix_" + experiment + ".csv")
  lookup_table = profile["lookup_table"]
  
  if "Connectome_maker" in profile.keys():
    filepath = profile["Connectome_maker"]["Output_files"]["nifti_outputfile"]
  else:
    filename = hcp_pattern+experiment+".nii.gz"
    filepath = os.path.join(connectomePath,filename)
  
  run_connectome_matrix(connectome_matrix, filepath, lookup_table,  experiment, profile, args.assignment, args.radius, args.distance)
  
  #setup output files for saving
  profile["makeConnectomeMatrix"] = { "Output_files":
        {"connectome_matrix" : connectome_matrix }
  }
  
  if args.stim:
    if not "stim" in profile.keys():
      raise valueError("--stim flag (-s) used, but previous outputs are missing.  Please run Connectome_maker.py")
    elif not "Connectome_maker" in profile["stim"].keys():
      raise valueError("--stim flag (-s) used, but previous outputs are missing.  Please run Connectome_maker.py")
      
    stim_tags = profile["stim"]["Connectome_maker"]["stim_tags"]
    
    stim_inputs = profile["stim"]["Connectome_maker"]["Output_files"]["nifti_outputfiles"]
    stim_lookup_tables = profile["stim"]["Connectome_maker"]["Output_files"]["lookup_tables"]
    stim_connectome_matrices = []
    for idx in range(len(stim_tags)):
      stim_experiment = experiment+"_"+stim_tags[idx]
      stim_conn_mat=os.path.join(profile["stimoutpath"], "connectome_matrix_" + stim_experiment + ".csv")
      
      run_connectome_matrix(stim_conn_mat, stim_inputs[idx], stim_lookup_tables[idx],  stim_experiment, profile, args.assignment, args.radius, args.distance)
      
      stim_connectome_matrices.append(stim_conn_mat)
      
    profile["stim"]["makeConnectomeMatrix"] = { "Output_files":
        {"connectome_matrix" : stim_connectome_matrices }
    }
    
    
  
  with open(args.profile, 'w') as fp:
    json.dump(profile, fp, sort_keys=True, indent=2)
    
if __name__ == "__main__":
   main()
