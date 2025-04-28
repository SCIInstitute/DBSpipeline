import numpy as np
import pandas as pd
import argparse
import os
import sys
import nrrd
import json
import re
import scipy.io


def build_parser():
  parser = argparse.ArgumentParser(
                prog = "SimulationParams",
                description = "Adds generated simulated data to the profile.  similar to BravoToSimluation",
                epilog="simulation table and other outputs from the clinical processing (already generated) will be added to the profile"
                )
  parser.add_argument("-p", "--profile", required=True,
                      help="profile filename",
                      dest="profile")
#  parser.add_argument("-o", "--output", required=False,
#                      help="output directory", dest="output_dir", type=str, default="")
  parser.add_argument("-d", "--param_dir", required=False,
                      help="location of the simulation data that will be used in simulation",
                      dest="param_dir")
  return parser
  
def findStimFiles(param_dir, profile):
  tab_fn = profile["experiment"]+".csv"
  
  tab_filename = os.path.join(param_dir, tab_fn)
  df = pd.read_csv(tab_filename)
  
  profile["stim_table"] = tab_filename
  
  filenames = []
  for col in list(df):
    filenames += list(df[col])
  
  nrrd_fn = list(set(filenames))
  
  file_str = []
  stim_param_flist = []
  file_exists = []
  for fn in nrrd_fn:
  #based on : "Stimulation_"+file_str[k]+".nrrd"
    fstr = nrrd_fn[0][12:-5]
    file_str.append(fstr)
    fname = fstr+".mat"
    stim_param_flist.append(fname)
    full_fn = os.path.join(param_dir, fname)
    file_exists.append(os.path.exists(full_fn))
    
  if not np.array(file_exists).all():
    raise ValueError("some files missing")
    
  all_params = scipy.io.loadmat(os.path.join(param_dir, "all_params.mat"))
  
  if not ( all_params["allparams"].shape[0] == len(file_str) and all_params["allparams_stim"].shape[0] == len(file_str)):
    raise ValueError("all_params.mat file does not match ", tab_fn)
  
    
  profile["stim_param_files"] = stim_param_flist
  
  return profile


def main():

  parser = build_parser()
  args = parser.parse_args()
  
  with open(args.profile, 'r') as js_file:
    profile = json.load(js_file)
    
  if args.param_dir:
    param_dir = args.param_dir
  elif "stim_param_dir" in profile.keys():
    param_dir = profile["stim_param_dir"]
  else:
    raise ValueError("need an input param dir in profile or passed in a flag (-d)")
  
  profile = findStimFiles(param_dir, profile)
  
  
  profile["stim_param_dir"] = param_dir


#  print(profile)
  
  with open(args.profile, 'w') as fp:
    json.dump(profile, fp, sort_keys=True, indent=2)


if __name__ == "__main__":
   main()

