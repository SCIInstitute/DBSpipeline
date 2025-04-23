import os
import json
from bs4 import BeautifulSoup
import xml

core_profile_fields = ("subject", "experiment", "profile_file", "rootpath", "SRFilesPath")

def profileToEnv(filename, *args,  **kwargs):

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
  
  
  with open(filename, 'r') as js_file:
    profile = json.load(js_file)
  
  print(args)
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
  
  
def loadSRNetwork(filename):
  with open(filename, 'r') as f:
    file = f.read()
    
  srnet = BeautifulSoup(file, features="xml")
  
  return srnet

def main():

#  filename = "/Users/jess/UF_brainstim/HiperGator_Connectome/S1/ClinicalSimprofile.json"
#  profileToEnv(filename, "stim", "segPath", "connectomePath", test = "stim", sp = "segPath", cp = "connectomePath")

  def_net = os.path.join(os.environ["CODEDIR"], "SRNetworks", "Whole_brain_sim_script.srn5")

  srnet  = loadSRNetwork(def_net)
  
#  print(srnet)
  

if __name__ == "__main__":
 main()
  
    

  
  
