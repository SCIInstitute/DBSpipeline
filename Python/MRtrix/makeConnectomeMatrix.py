# -*- coding: utf-8 -*-
"""


usage:

python3 makeConnectomeMatrix.py --profile Allprofile.json --assigment "assignment_end_voxels"


"""



import pandas as pd
import os
import numpy as np
import argparse
import json
import subprocess

default_assignment="assignment_radial_search 3mm"
hcp_pattern="HCP_parc_all_"

def build_parser():
  parser = argparse.ArgumentParser(
                prog = "Connectome_maker",
                description = "compiles a connectome nifti from disparate nifti segmentations.",
                epilog="output saves nifti files as defined by profile or settings"
                )

  # This will be implemented as rollout broadens
  parser.add_argument("-p", "--profile", required=True,
                      help="profile filename",
                      dest="profile")

  parser.add_argument("-a", "--assignment", required=False,
                      help="Assignment method for MRtrix",
                      dest="assignment")
  return parser
  

def main():

  parser = build_parser()
  args = parser.parse_args()
#print(args.subject, args.ROI_list_left, args.ROI_list_right)

  with open(args.profile, 'r') as js_file:
    profile = json.load(js_file)
    
  subject= profile["subject"]
  experiment = profile["experiment"]
  lookup_table = profile["lookup_table"]
  connectomePath = profile["connectomePath"]
  fibertractPath = profile["fibertractPath"]
  cleantractPath = profile["cleantractPath"]
    
  file_dir = profile["tractographyPath"]
  
  if not args.assignment:
    assignment = default_assignment
  else:
    assignment = args.assignment
    
  filename = hcp_pattern+experiment+".nii.gz"
  filepath = os.path.join(connectomePath,filename)
  
#  if SYSNAME == "hipergator":
#    subprocess.run(["module", "load", "mrtrix"])
  
  cl_call1 = ["mrtransform",  "-linear", os.path.join(cleantractPath, "ACPC_to_b0.txt"), filepath, os.path.join(connectomePath, hcp_pattern+"b0space.nii.gz"),   "-force"]
  print(" ".join(cl_call1))
  subprocess.run(cl_call1)
  
  connectome_matrix=os.path.join(connectomePath, "connectome_matrix_" + experiment + ".csv")
  print(connectome_matrix)
  print(assignment)
  
  cl_call2 = ["tck2connectome", os.path.join(fibertractPath, "whole_brain_fibers.tck"), os.path.join(connectomePath, hcp_pattern+"b0space.nii.gz"), connectome_matrix,  "-tck_weights_in", os.path.join(fibertractPath, "sift2_weights.txt"),   "-keep_unassigned",  "-"+assignment,  "-out_assignments", os.path.join(cleantractPath, "assignments_" + experiment + ".txt"),  "-force"]
      #-scale_invlength \
      #-scale_invnodevol
  print(" ".join(cl_call2))
  subprocess.run(cl_call2)
      
 
  #setup output files for saving
  profile["makeConnectomeMatrix"] = { "Output_files":
        {"connectome_matrix" : connectome_matrix
        }
  }
  
  with open(args.profile, 'w') as fp:
    json.dump(profile, fp)
    
if __name__ == "__main__":
   main()
