# prototype profile for connectomics from the CL
import json
import numpy as np

import os

scriptpath = os.path.dirname(os.path.abspath(__file__))
#print(scriptpath)
#profile_file = os.path.join(scriptpath, "Allprofile.json")

# TODO: Preprocessing placeholder
# TODO: save location
#   experiment : github? probably with the data
#   subjects : centralized or in subject folder

"""
Some notes:
luigi handles data workflows in python:
https://github.com/spotify/luigi?tab=readme-ov-file

still not sure that luigi would be work implementing for these pipelines, since I'm not sure what the overhead is, or what it actually supports
There are some similarities to SCIRun.  Maybe we can include somekind of SCIrun pipeline manager into the mix in the proposal
other packages for other frameworks exists, but luigi is python and open source. Others mentioned in sources: Apache Beam, Airflow, Dask, Prefect

https://github.com/PrefectHQ/prefect
https://github.com/apache/beam
https://github.com/apache/airflow
https://github.com/dask/dask

"""

def build_parser():
  parser = argparse.ArgumentParser(
                prog = "makeProfile",
                description = "makes a profile file for a set of experimental parameters",
                epilog="saves a profile to the provide profile path")

  # This will be implemented as rollout broadens
  parser.add_argument("-d", "--datapath", required=False,
                      help="path to were the data are located. If not provided, the script will try to use the enviroment variable DATADIR", default
                      dest="datapath")
  parser.add_argument("-p", "--profilepath", required=False,
                      help="path to profile directory. default location is <datapath>/profiles",
                      dest="profilepath")
  parser.add_argument("-e", "--experiment", required=False,
                      help="path (relative to profilepath or absolute) to experiment profile file. default file found default_experiment_profile.json.",
                      dest="experimentfile", default = os.path.join(scriptpath, "default_experiment_profile.json" ))
  return parser
  
def check_parser(args):

  use_environ = True
  if args.datapath:
    if os.path.exists(args.datapath):
      use_environ = False
    else:
      print("the provided path, "+args.datapath+"does not exist.  Trying environment variable")
    
      
  if use_environ:
    if os.environ["DATADIR"]
      args.datapath = os.environ["DATADIR"]
    else:
      raise ValueError("environment variable DATADIR not set.  use -d flag to provide path or set DATADIR")
  
  use_defaultpath = True
  profilepath =
  if args.profilepath:
    if os.path.exists(args.profilepath):
      use_defaultpath = False
    else:
      print("the provided path, "+args.profilepath+"does not exist.  Using default path")
  
  if use_defaultpath:
    args.profilepath = os.path.join(datapath, "profiles")
    if os.path.exists(args.profilepath):
      os.makedirs(args.profilepath)
  
  experimentfile = args.experimentfile
  if not os.path.exists(args.experimentfile):
    args.experimentfile = os.path.abspath(args.experimentfile)
    if not os.path.exists(args.experimentfile):
      args.experimentfile = os.path.join(args.profilepath, args.experimentfile)
    else:
      raise ValueError("cannot file experiment file "+experimentfile+" or "+ args.experimentfile)
      
  return args
  
def readExperimentFile(args):
  with open(experimentfile, 'r') as json_file:
    experiment = json.load(json_file)
    
  check_experiment(experiment, args)
  
  return experiment
  
def check_experiment(experiment, args):
  
  required_fields = ["experiment_name", "subjects", "lookup_table", "left_ROI", "right_ROI"]
  
  for key in required_fields:
    if not key in experiment:
      raise ValueError("Required experiment inputs:", ", ".join(required_fields))
  
  print(print_folder(args.datapath))
      
  for sub in subjects:
    sub_dir = os.path.join(args.datapath, sub)
    missing = []
    if not os.path.exists(sub_dir):
      missing.append(sub)
    else:
      #TODO: check file structure
      subfolders = get_contents(sub_dir)
      
   if len(missing)>0:
      raise ValueError("One or more subjects provided in experiment profile are missing")
    
    
  return True
  
def fast_scandir(dirname):
  subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
  for dirname in list(subfolders):
    subfolders.extend(fast_scandir(dirname))
  return subfolders

def get_contents(directory):
  #test_content = get_contents(sub_dir)
  parent, folder = os.path.split(directory)
  children = os.listdir(directory)
  files={}
  directories = {}
  for child in children:
    if child[0]==".":
      continue
    child_path = os.path.join(directory, child)
    if os.path.isdir(child_path):
      directories[child] = get_contents(child_path)
    else:
#      files.append((child, os.path.getsize(child_path)))
      files[child] = {
          "size" : os.path.getsize(child_path),
          "time" : os.path.getmtime(child_path)
      }
    contents = {"files" : files, "directories" :  directories}
#  output = {"path" : parent, folder : contents}
  return contents
  
def print_folder(directory):
  parent, folder = os.path.split(directory)
  
  contents = get_contents(directory)
  
  return string

def print_contents(contents, indent = 2):
  
  output_string = ""
  for
  

def main():

  parser = build_parser()
  args = parser.parse_args()
  args = check_parser(args)
  
  experiment = readExperimentFile(arg.experimentfile)
  
  
    
if __name__ == "__main__":
    main()
    


#if os.path.exists(profile_file):
#  with open(profile_file, 'r') as json_file:
#    profile = json.load(json_file)
#else:
#  profile = {}
#
#profile["subject"] = "S1"
#profile["experiment"]  ="All"
#profile["profile_file"]= profile_file
#
#profile["lookup_table"] = os.path.join(os.environ["DATADIR"], "connectome_lookup_all.csv")
#profile["rootpath"] = os.path.join(os.environ["DATADIR"],"S1")
#profile["segPath"] = os.path.join(profile["rootpath"], "Segmentations")
#profile["connectomePath"] = os.path.join(profile["rootpath"], "Connectome")
#profile["tractographyPath"] = os.path.join(profile["rootpath"], "Tractography")
#profile["cleantractPath"] = os.path.join(profile["tractographyPath"], "Cleaned")
#profile["fibertractPath"] = os.path.join(profile["tractographyPath"], "Cleaned", "Fibers")
#
## need to find a way to make this more consistent
## for calculate_connectome.py
## from matrix key
#profile["left_ROI"] =  [ 1001 ]
#profile["right_ROI"] = [ 1016 ]
#
#
#
#
#
#with open(profile_file, 'w') as fp:
#    json.dump(profile, fp)



