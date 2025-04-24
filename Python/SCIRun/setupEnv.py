import os
import sys


def build_parser():
  parser = argparse.ArgumentParser(
                prog = "setupEnv",
                description = "sets up the environment variables for running SCIRun networks",
                epilog="filenames are saved in the profile"
                )
  parser.add_argument("-p", "--profile", required=True,
                      help="profile filename",
                      dest="profile")
  return parser

core_profile_fields = ("subject", "experiment", "profile_file", "rootpath", "SRFilesPath")

def profileToEnv(profile, *args,  **kwargs):

  # convert profile values to environment variables.
  # inputs:
  #  filename - filename for the profile (json format) (required)
  #  additional inputs args - field names (from the profile) to save to environment (string).  The variable name will be the same as the field name.
  #  kwargs - fields from the profile to save to environment (string).  the kwarg name will be the name of the  envrionment var
  #    ex: spath = "segmentation_path" with save the field profile["segmentation_path"] to the environment variable spath. values must be a string
  #
  # The os.environ will be updated when the function is run.
  #
  # This funciton is designed to run with SCIRun networks that use environment vars to pass values, such as bash scripting
  
  # pass profile instead
#  with open(filename, 'r') as js_file:
#    profile = json.load(js_file)
  
  c_fields = (*core_profile_fields, *args)
  print(c_fields)
  for field in c_fields:
    if isinstance(profile[field], str):
      os.environ[field] = profile[field]
    else:
      raise ValueError("cannot assign %d to %d environment variable", type(profile[field]), field)
    
    
  for key, value in kwargs.items():
    if isinstance(profile[value], str):
      os.environ[key] = profile[value]
    else:
      raise ValueError("cannot assign ", type(profile[value]), " to ", key, " environment variable" )
  return
  

def main():

  parser = build_parser()
  args = parser.parse_args()
  
  with open(args.profile, 'r') as js_file:
    profile = json.load(js_file)
    
  profileToEnv(profile)
  
  return


