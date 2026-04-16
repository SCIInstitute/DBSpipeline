# prototype profile for connectomics from the CL
import json
import numpy as np
import argparse

import os

from defaultProfile import experiment_required_fields, def_Makeprofile, files_ignore, def_print_contents, base_profile_keys, def_baseProfile, def_implantation



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


Current design is based on an "experiment" with a set of parameters and subjects that would be relatively consistent. This could still be a useful concept yet I think I would like to rethink the interface a little bit. 

"""

def build_parser():
  parser = argparse.ArgumentParser(
                prog = "makeProfile",
                description = "makes a profile file for a set of experimental parameters",
                epilog="saves a profile to the provide profile path")

  # This will be implemented as rollout broadens
  parser.add_argument("-d", "--datapath", required=False,
                      help="path to were the data are located. If not provided, the script will try to use the enviroment variable DATADIR",
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
    if os.environ["DATADIR"]:
      args.datapath = os.environ["DATADIR"]
    else:
      raise ValueError("environment variable DATADIR not set.  use -d flag to provide path or set DATADIR")
  
  use_defaultpath = True
  profilepath = ""
  if args.profilepath:
    if os.path.exists(args.profilepath):
      use_defaultpath = False
    else:
      print("the provided path, "+args.profilepath+"does not exist.  Using default path")
  
  if use_defaultpath:
    args.profilepath = os.path.join(args.datapath, "profiles")
    if not os.path.exists(args.profilepath):
      os.makedirs(args.profilepath)
  
  experimentfile = args.experimentfile
  if not os.path.exists(args.experimentfile):
    args.experimentfile = os.path.abspath(args.experimentfile)
    if not os.path.exists(args.experimentfile):
      args.experimentfile = os.path.join(args.profilepath, args.experimentfile)
    else:
      raise ValueError("cannot find experiment file "+experimentfile+" or "+ args.experimentfile)
      
  return args
  
def readExperimentFile(args):
  print(args.experimentfile)
  with open(args.experimentfile, 'r') as json_file:
    experiment = json.load(json_file)
  
#  print(experiment)
  
  check_experiment(experiment, args)
  
  return experiment
  
def check_experiment(experiment, args):
  
  for key in experiment_required_fields:
    if not key in experiment.keys():
      raise ValueError("Required experiment inputs:", ", ".join(experiment_required_fields))
  
#  print(print_folder(args.datapath))
      
  for sub in experiment["subjects"]:
    sub_dir = os.path.join(args.datapath, sub)
    missing = []
    if not os.path.exists(sub_dir):
      missing.append(sub)
    else:
      #TODO: check file structure
      subfolders = get_contents(sub_dir)
#      print(print_contents(subfolders))
#      print(print_folder(sub_dir))
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
    if child[0]=="." or child in files_ignore:
#      print("skip ", child)
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
#  print(contents)
#  output = {"path" : parent, folder : contents}
  return contents
  
def print_folder(directory, **kwargs):
  parent, folder = os.path.split(directory)
  
  contents = get_contents(directory)
#  print(print_contents(contents, 1, 2, True))
  return folder+"\n"+print_contents(contents, **kwargs)

def print_contents(contents, **kwargs):
  kwargs = {**def_print_contents, **kwargs}
  indent = (" "*kwargs["indent_spaces"]+"| ")*kwargs["indent_level"]
#  output_string = " "*(indent-1)+"|_ "
  output_string = ""
  if not kwargs["dirs_only"]:
    for file in contents["files"]:
      output_string+=indent+file+"\n"
  for dir_name, dir_content in contents["directories"].items():
    output_string+=indent[:-1]+"-"+dir_name+"\n"
    output_string+=print_contents(dir_content, **{**kwargs, "indent_level" : kwargs["indent_level"]+1} )
    
  return output_string
#  print(output_string)
#  for



def getRootPath(profile, args):
  return os.path.join(args.datapath, profile["subject"] )

def getSegPath(profile, args):
  return os.path.join(profile["rootPath"], "Segmentations")
  
def getSRFilesPath(profile, args):
  return os.path.join(profile["rootPath"], "SCIRun_files")
  
def getConnectomePath(profile, args):
  return os.path.join(profile["rootPath"], "Connectome")
  
def getTractographyPath(profile, args):
  return os.path.join(profile["rootPath"], "Tractography")

def getCleanTractPath(profile, args):
  return os.path.join(profile["tractographyPath"], "Cleaned")
  
def getFiberTractPath(profile, args):
  return os.path.join(profile["cleantractPath"], "Fibers")
  
paths_table = {
  "rootPath" : getRootPath,
  "segPath" : getSegPath,
  "SRFilesPath" : getSRFilesPath,
  "connectomePath" : getConnectomePath,
  "tractographyPath" : getTractographyPath,
  "cleantractPath" : getCleanTractPath,
  "fibertractPath" : getFiberTractPath,
}


def makeProfile(subject, args, **kwargs):
  kwargs = {**def_Makeprofile, **kwargs}
  
  profile_filename = subject+"_"+kwargs["experiment"]+"_profile.json"
  profile_file = os.path.join(args.profilepath, profile_filename)
  
  if os.path.exists(profile_file):
    with open(profile_file, 'r') as json_file:
      profile = json.load(json_file)
  else:
    profile = {}
    
  profile["subject"]=subject
  profile["profile_file"] = profile_file
  
  for key, value in kwargs.items():
    if key in base_profile_keys and value:
      profile[key] = value #do I need to deep copy?
  
  for key in base_profile_keys:
    if not key in profile.keys():
      if key in def_baseProfile.keys():
        profile[key] = def_baseProfile[key] #do I need to deep copy?
      else:
        # very order dependent right now
        profile[key] = paths_table[key](profile,args)
  
  print(profile)
  with open(profile_file, 'w') as fp:
    json.dump(profile, fp, sort_keys=True, indent=2)
  return profile_file


def main():

  parser = build_parser()
  args = parser.parse_args()
  args = check_parser(args)
  
  experiment = readExperimentFile(args)
  
  for sub in experiment["subjects"]:
    makeProfile(sub, args,
          experiment = experiment["experiment_name"],
          lookup_table = experiment["lookup_table"],
          left_ROI = experiment["left_ROI"],
          right_ROI = experiment["right_ROI"]
          )
  
    
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



