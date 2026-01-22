import os
import json
from bs4 import BeautifulSoup
import xml

  
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
  
    

  
  
