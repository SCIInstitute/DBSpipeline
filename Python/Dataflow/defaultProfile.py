# default values for makeProfile.py

from defaultImplantation import def_implantation


experiment_required_fields = [
  "experiment_name",
  "subjects",
  "lookup_table",
  "left_ROI",
  "right_ROI"
]
                    
def_Makeprofile = {
  "experiment" : "default"
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
  "rootPath",
  "segPath",
  "SRFilesPath",
  "connectomePath",
  "tractographyPath",
  "cleantractPath",
  "fibertractPath",
  "implantation"
]

def_baseProfile = {
  "lookup_table" : "connectome_lookup.csv",
  "left_ROI" : [ 1001 ],
  "right_ROI" : [ 1016 ],
  "implantation" : def_implantation
}

# maybe I'll need to add these too?
#  "stim_table",
#  "stimoutpath",
#  "stimsegpath",
#  "stim_param_dir"

