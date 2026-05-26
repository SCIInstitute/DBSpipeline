# prototype profile for connectomics from the CL
import json
import numpy as np
import argparse
import pathlib
import copy

import os

from defaultProfile import experiment_required_fields, files_ignore, def_print_contents, def_Makeprofile,  base_profile_keys, profile_keys, def_baseProfile, def_implantation



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


Notes from Matt (2026/04/14):
patient name redundancy - make sure that it doesn't have to be read/written twice
two patient IDs - freesurfer and connectomics 

"""

def build_parser():
  parser = argparse.ArgumentParser(
                prog = "makeProfile",
                description = "makes a profile file for a set of experimental parameters",
                epilog="saves a profile subject path inferred from the DATADIR environment variable or as supplied to %(prog)s")
  parser.add_argument("-s", "--subjects", required=True,
                      help="Lists of subjects to make a profile. Subjects should have their own folder in DATADIR",
                      dest="subjects", nargs="*")
  parser.add_argument("-d", "--datapath", required=False,
                      help="path to were the data are located. If not provided, the script will try to use the enviroment variable DATADIR",
                      dest="datapath", type=pathlib.Path)
  parser.add_argument("-p", "--profile", required=False,
                      help="path to profile file to use as a template.  Only provided values will be used.", nargs="*", default = [""],
                      dest="profilepath", type=pathlib.Path)
  parser.add_argument("-f", "--force", required=False,
                      help="Force overwrite profile files",
                      action = "store_true", dest="rewrite")
#  parser.add_argument("-e", "--experiment", required=False,
#                      help="Name for the experiment.  this string will be used in several filenames, and should not include spaces.  Unicode characters and many symboles may also cause problems. (default: %(default)s)",
#                      dest="experiment_name", default = "default")
#  parser.add_argument("--lookup_table", required=False,
#                      help="path to lookuptable to use for atlas generation. (default: %(default)s)",
#                      dest="lookup_table", type=pathlib.Path, default = pathlib.Path("connectome_lookup.csv") )
  for key, value in profile_keys["base"].items():
    p_args = [ "--"+key ]
    if "short_flag" in profile_keys["base"][key].keys():
      p_args.insert(0, "-"+profile_keys["base"][key]["short_flag"])
      del profile_keys["base"][key]["short_flag"]
    p_kwargs = { **{"required" : False }, **profile_keys["base"][key] }
    parser.add_argument(*p_args, **p_kwargs)
#    print(p_args)
  return parser

def check_datapath(datapath):
    
  use_environ = True
  if datapath:
    if not isinstance(datapath, pathlib.Path):
      datapath = pathlib.Path(datapath)
    if datapath.is_dir():
      use_environ = False
      datapath = os.fspath(datapath)
    else:
      print("the provided path, "+os.fspath(datapath)+" does not exist.  Trying environment variable")
  
  if use_environ:
    if os.environ["DATADIR"]:
      datapath = os.environ["DATADIR"]
    else:
      raise ValueError("environment variable DATADIR not set.  use -d flag to provide path or set DATADIR")
      
  return datapath
  
  
def check_profilepath(profilepath):

  if profilepath:
    if not isinstance(profilepath, pathlib.Path):
      profilepath = pathlib.Path(profilepath)
    if profilepath.exists():
      profilepath = os.fspath(profilepath)
    else:
      print("the supplied profile, "+os.fspath(profilepath)+", does not exist. Ignoring")
      profilepath=""

  
  return profilepath
  
def check_lookup_table(lookup_table):
#  print(os.fspath(args.lookup_table))
  
  if lookup_table:
    if not isinstance(lookup_table, pathlib.Path):
      lookup_table = pathlib.Path(lookup_table)
    if lookup_table.exists():
      os.fspath(lookup_table)
    else:
#      def_lookup = os.path.join(args.datapath, def_baseProfile["lookup_table"] )
      print("the supplied lookup table, "+os.fspath(lookup_table)+", does not exist. Using default value: "+ os.fspath(def_baseProfile["lookup_table"]) )
      lookup_table = os.fspath(def_baseProfile["lookup_table"])
  else:
    lookup_table = os.fspath(def_baseProfile["lookup_table"])
  
  return lookup_table
  
def check_subject(datapath, subject):
  sub_dir = os.path.join(datapath, subject)
  sub_check = False
  if os.path.isdir(sub_dir):
    sub_check = True
  else:
    print(sub_dir+" not found ")
  return sub_check
  
  
  
  
def check_parser(args):

  args.datapath = check_datapath(args.datapath)
  
  args.lookup_table = check_lookup_table(args.lookup_table)
  
  print(args.profilepath)
  profilepaths = []
  for profpath in args.profilepath:
    profilepaths.append(check_profilepath(profpath))
  
  
  
  missing_subs=[]
  for subject in args.subjects:
    
    if not check_subject(args.datapath, subject):
      missing_subs.append(subject)
    
  if len(missing_subs)>0:
    raise ValueError("Subjects:"+" ".join(missing_subs)+", are missing folders in "+args.datapath)
  
  if len(profilepaths)==1 or len(profilepaths)==len(args.subjects):
    args.profilepath = profilepaths
  else:
    print(profilepaths)
    raise ValueError("profilepath inputs (-p, --profile) needs to be a single file, or the lenght as the subjects list (-s, --subjects)")
      
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



def getRootPath(profile, **kwargs):
  return os.path.join(kwargs["datapath"], profile["subject"] )

def getSegPath(profile, **kwargs):
  return os.path.join(profile["rootPath"], "Segmentations")
  
def getSRFilesPath(profile, **kwargs):
  return os.path.join(profile["rootPath"], "SCIRun_files")
  
def getConnectomePath(profile, **kwargs):
  return os.path.join(profile["rootPath"], "Connectome")
  
def getTractographyPath(profile, **kwargs):
  return os.path.join(profile["rootPath"], "Tractography")

def getCleanTractPath(profile, **kwargs):
  return os.path.join(profile["tractographyPath"], "Cleaned")
  
def getFiberTractPath(profile, **kwargs):
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

def copyFromProfile(subject, profilepath):
  # copy what makes sense from another profile
  with open(profilepath, 'r') as json_file:
    profile_old = json.load(json_file)
  
  subject_old = profile_old["subject"]
  
  profile = copy.deepcopy(profile_old)
  
  if not subject == subject_old:
  
    with open(profilepath, 'r+') as st_file:
      content_old = st_file.read()
      
    content = content_old.replace(subject_old, subject)
    profile = json.loads(content)
    
    # TODO: it would probably be good to have a check to see if the files exist, especially when changing the subject name
    # TODO: another thing to do could be to make an option to have a list of profiles for the list of subjects?
    
  return profile
  

def makeProfile(subject,  **kwargs):
  kwargs = {**def_Makeprofile, **def_baseProfile, **kwargs}
  
  
  kwargs["datapath"] = check_datapath(kwargs["datapath"])
  if not check_subject(kwargs["datapath"], subject):
    raise ValueError(subject+" not found in "+kwargs["datapath"])
  # there may be an edge case where a user may want to set the datapath from this input, but I'm not going to deal with that until someone asks for it.
  profilepath = check_profilepath(kwargs["profilepath"])
  
  profile_filename = subject+"_"+kwargs["experiment"]+"_profile.json"
  profile_file = os.path.join(kwargs["datapath"], subject, profile_filename)
  
  print(kwargs["datapath"])
  print(profile_file)
  
  if kwargs["profilepath"]:
    print(" copying from "+kwargs["profilepath"])
    profile_cp = copyFromProfile(subject, profilepath)
  
  write_q = True
  if os.path.exists(profile_file):
    print("previous version of this profile file exists (" + profile_file + ").  Pulling existing fields from existing file, and Kwarg input fields will override previous values.  Note the profile file will not be overwritten without the appropriate flag ('-f' or '--force')")
    write_q = False
    with open(profile_file, 'r') as json_file:
      profile = json.load(json_file)
  else:
    profile = {}
  
  if kwargs["profilepath"]:
    profile_cp = copyFromProfile(subject, profilepath)
    profile = { **profile, **profile_cp}
    
    
  
  profile["subject"]=subject
  profile["profile_file"] = profile_file
  
  
  for key, value in kwargs.items():
    if key == "subject":
      print("subject added as arg and kwarg.  kwarg value will be ignored")
      continue
    elif key == "profile_file":
      print("'profile_file' kwarg will be ignored")
      continue
    elif key in profile_keys["base"].keys() and value:
      profile[key] = value #do I need to deep copy?
  
  for key in profile_keys["base"].keys():
    if not key in profile.keys():
      if key in def_baseProfile.keys():
        profile[key] = def_baseProfile[key] #do I need to deep copy?
      else:
        # very order dependent right now
        profile[key] = paths_table[key](profile,**kwargs)
  
  print(profile)
  if not write_q:
    if kwargs["rewrite"]:
      write_q = True
      print(" overwriting previous profile file "+ profile_file)
    else:
      print("profile already exists :" + profile_file + ". To overwrite, use '-f' or '--force'.")
      profile_file = ""
      
      
  if write_q:
    with open(profile_file, 'w') as fp:
      json.dump(profile, fp, sort_keys=True, indent=2)
  return profile_file


def main():

  parser = build_parser()
  args = parser.parse_args()
  args = check_parser(args)
  
#  experiment = readExperimentFile(args)
  subjects=args.subjects
  profilepaths = args.profilepath
  args_dict = vars(args)
  del args_dict["subjects"]
#  print(pathlib.Path)
  for key, val in args_dict.items():
#    print(key, type(val), isinstance(val, pathlib.Path) )
    if isinstance(val, pathlib.Path):
      args_dict[key] = os.fspath(val)

#  print(args_dict)
  for k, sub in enumerate(subjects):
    if len(profilepaths)==1:
      args_dict["profilepath"] = profilepaths[0]
    else:
      args_dict["profilepath"] = profilepaths[k]
    makeProfile(sub, **args_dict)
  
    
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



