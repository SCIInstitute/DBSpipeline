import numpy as np
import pandas as pd
import argparse
import os
import sys
import nrrd
import json
import re
import scipy.io
import subprocess

def_net = os.path.join(os.environ["CODEDIR"], "SRNetworks", "Whole_brain_sim_script.srn5")

def build_parser():
  parser = argparse.ArgumentParser(
                prog = "RunSimulations",
                description = "runs the simulation parameters generated by the BravoToSimulation script",
                epilog="filenames are saved in the profile"
                )
  parser.add_argument("-p", "--profile", required=True,
                      help="profile filename",
                      dest="profile")
  parser.add_argument("-n", "--network", required=False,
                      help="scirun network", dest="SR_net", type=str,  default = def_net)
  parser.add_argument("-d", "--debug", required=False,
                      help="enable debug mode", action = "store_true", dest="debug_mode" )
  return parser
  
  
def main():

  parser = build_parser()
  args = parser.parse_args()
  
  with open(args.profile, 'r') as js_file:
    profile = json.load(js_file)
    
  p_dir = profile["stim_param_dir"]
  wh_sr = subprocess.run(["which", "scirun"], capture_output=True)
  print(wh_sr)

  
  # this is a fix for ImportMatricesFromMatlab scripting bug
  # The network is already modified for these files
  sr_dir = profile["SRFilesPath"]
  tan_fn = os.path.join(sr_dir,"Edge_data_tans.mat")
  end_fn = os.path.join(sr_dir,"Edge_data_ends.mat")

  if not os.path.exists(tan_fn):
    edgedata_fn = os.path.join(sr_dir,"Edge_data.mat")
    edgedata = scipy.io.loadmat(edgedata_fn)
    scipy.io.savemat(tan_fn, {"Tangents" : edgedata["Tangents"]})
  if not os.path.exists(end_fn):
    edgedata_fn = os.path.join(sr_dir,"Edge_data.mat")
    edgedata = scipy.io.loadmat(edgedata_fn)
    scipy.io.savemat(end_fn, {"Ends" : edgedata["Ends"]})
    
  
  #SCIRun_call is an environment variable set to the the SCIRun executable path
  SCIRun_call = os.environ["SCIRun_call"]
  
  os.environ["PATIENTID"] = profile["subject"]
  
  for p_fname in profile["stim_param_files"]:
    f_fname = os.path.join(p_dir, p_fname)
    print(f_fname)
    os.environ["PARAM_MATRIX"] = f_fname
    
#    print(os.environ["PARAM_MATRIX"])

    sr_call = [SCIRun_call, "-x", "-0", "-E", args.SR_net]
#    sr_call = [SCIRun_call, "-e", args.SR_net]
    if args.debug_mode:
      sr_call.append("--verbose")
      
    print(" ".join(sr_call))
    
    subprocess.run(sr_call)
    
if __name__ == "__main__":
   main()
    
    
    
  
