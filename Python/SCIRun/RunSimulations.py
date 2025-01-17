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

def_net = os.path.join(os.environ["CODEDIR"], "SRNetworks", "Whole_brain_sim.srn5")

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

  return parser
  
  
def main():

  parser = build_parser()
  args = parser.parse_args()
  
  with open(args.profile, 'r') as js_file:
    profile = json.load(js_file)
    
  p_dir = profile["stim_param_dir"]
  for p_fname in profile["stim_param_files"]:
    f_fname = os.path.join(p_dir, p_fname)
    print(f_fname)
    os.environ["PARAM_MATRIX"] = f_fname
    
    wh_sr = subprocess.run(["which", "scirun"], capture_output=True)
    print(wh_sr)
    
    #SCIRun_call is an environment variable set to the the SCIRun executable path
    SCIRun_call = os.environ["SCIRun_call"]
    sr_call = [SCIRun_call, "-x", "-0", "-E", args.SR_net]
    print(" ".join(sr_call))
    
    subprocess.run(sr_call)
    
if __name__ == "__main__":
   main()
    
    
    
  
