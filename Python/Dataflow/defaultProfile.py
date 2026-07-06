# default values for makeProfile.py

import pathlib
from defaultImplantation import def_implantation


experiment_required_fields = [
  "experiment_name",
  "subjects",
  "lookup_table",
  "left_ROI",
  "right_ROI"
]
                    
def_Makeprofile = {
  "profilepath" : "",
  "rewrite" : False,
  "datapath" : "",
  
}

files_ignore = [
  "__pycache__"
]

def_print_contents = {
  "indent_level" : 1,
  "indent_spaces" : 2,
  "dirs_only" : True
}

base_profile_keys = [
  "experiment",
  "lookup_table",
  "left_ROI",
  "right_ROI",
  "rootpath",
  "segPath",
  "SRFilesPath",
  "connectomePath",
  "tractographyPath",
  "cleantractPath",
  "fibertractPath"
]

optional_profile_keys = [
  "implantation",
  "stim_table",
  "stimoutpath",
  "stimsegpath",
  "stim_param_dir"
]




profile_keys = {}
profile_keys["base"] = {
  "experiment" : {
              "short_flag" : "e",
              "help" : "Name for the experiment.  this string will be used in several filenames, and should not include spaces.  Unicode characters and many symboles may also cause problems. (default: %(default)s)",
              "default" : "default"
              },
  "lookup_table" : {
              "help" : "path to lookuptable to use for atlas generation. (default: %(default)s)",
              "type" : pathlib.Path,
              "default" : pathlib.Path("connectome_lookup.csv")
              },
  "left_ROI" : {
              "help" : "index for the region of intrest, left side. (default: %(default)s)",
              "nargs" : "*",
              "type" : int,
              "default" : [ 1001 ]
              },
  "right_ROI" :  {
              "help" : "index for the region of intrest, right side. (default: %(default)s)",
              "nargs" : "*",
              "type" : int,
              "default" : [ 1016 ]
              },
  "rootpath" :  {
              "help" : "subject data directory. (default: <datapath>/subject)",
              "type" : pathlib.Path
              },
  "segPath" :  {
              "help" : "subject segmentation directory. (default: <rootPath>/Segmentations)",
              "type" : pathlib.Path
              },
  "SRFilesPath" :  {
              "help" : "subject directory for SCIRun files. (default: <rootPath>/SCIRun_files)",
              "type" : pathlib.Path
              },
  "connectomePath" :  {
              "help" : "subject directory for connectome data. (default: <rootPath>/Connectome)",
              "type" : pathlib.Path
              },
  "tractographyPath" :  {
              "help" : "subject directory for tractography data. (default: <rootPath>/Tractography)",
              "type" : pathlib.Path
              },
  "cleantractPath" :  {
              "help" : "subject directory for cleanded tractography data. (default: <tractographyPath>/Cleaned)",
              "type" : pathlib.Path
              },
  "fibertractPath" :  {
              "help" : "subject directory for fiber tractography data. (default: <cleantractPath>/Fibers)",
              "type" : pathlib.Path
              }
}


profile_keys["optional"] = {
  "implantation" : {
              "help" : "implantantion profile for the patient",
              "default" : def_implantation
              },
  "stim_param_dir" : {
              "help" : "Path to the directory with clinical stimulation parameters to use in SCIRun simulations",
              "type" : pathlib.Path
              },
  "stim_table" : {
              "help" : "Path to the lookuptable for stimulated regions",
              "type" : pathlib.Path
              },
  "stimoutpath" : {
              "help" : "Path to directory for Connectome data using stimulation regions",
              "type" : pathlib.Path
              },
  "stimsegpath" : {
              "help" : "Path to the directory containing the segmented stimulation regions. An output of the SCIRun simulation pipelines.",
              "type" : pathlib.Path
              }
}

def_baseProfile = {}
for key, v_dict in profile_keys["base"].items():
  if "default" in v_dict.keys():
    def_baseProfile[key]=v_dict["default"]

def_optProfile = {}
for key, v_dict in profile_keys["optional"].items():
  if "default" in v_dict.keys():
    def_optProfile[key]=v_dict["default"]


# maybe I'll need to add these too?
#  "implantation" : def_implantation
#  "stim_table",
#  "stimoutpath",
#  "stimsegpath",
#  "stim_param_dir"

