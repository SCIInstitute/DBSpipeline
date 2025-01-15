import numpy as np
import pandas as pd
import argparse
import os
import sys
import nrrd
import json
import re


def build_parser():
  parser = argparse.ArgumentParser(
                prog = "BravoToSimulation",
                description = "Converts Bravo clinical data into data that SCIRun can use for simulations",
                epilog="outputs a simulation table, matrix of contact amplitudes, and other data needed for SCIRun"
                )
#  parser.add_argument("-p", "--profile", required=True,
#                      help="profile filename",
#                      dest="profile")
#  parser.add_argument("-s", "--stim", required=False,
#                      help="include stimulations",
#                      action = "store_true", dest="stim")
  parser.add_argument("-s", "--settings", required=True,
                      help="settings filename, usually from Bravo",
                      dest="settings_fname")
  return parser
  

def parseSettingString(setting_str, **kwargs):
  values = {
      "pulse_freq" :  re.findall(r"^(\d+\.?\d+?)([a-z]?Hz)",setting_str)[0],
      "pulse_dur" :  re.findall(r"(\d+\.?\d+?)([a-z]?S)",setting_str)[0],
      "sensing_freq" : re.findall(r"\s+\@\s+(\d+\.?\d+?)([a-z]?Hz)",setting_str)[0],
      "cathodes" : re.findall(r"\+(\w+)",setting_str),
      "annodes" : re.findall(r"\-(\w+)",setting_str)
  }
  return values
  
def stringToMatrix(settings_df, contact_list=[], **kwargs):
  # settingstr_tup = (left settings, right settings)
  # one can be empty
  # TODO: move to hardware parameter file
  def_contact_list = [ "E0", "A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", "E7"]
  if not contact_list:
    contact_list = def_contact_list
   
  n_settings = len(settings_df)
  l_devices = settings_df["Left Device"]
  r_devices = settings_df["Right Device"]
  
  devices_sett = [ (l_devices[k], r_devices[k]) for k in range(n_settings) ]
  uniq_devices = list(set(devices_sett))
  
  num_contacts = sum([len(t) for t in uniq_devices])
  
  
  
  
    
  
  
  

def main():

  parser = build_parser()
  args = parser.parse_args()
  
  settings_df = pd.read_csv(args.settings_fname, delimiter=',')
  
  print(settings_df)
  
  for row in settings_df.iterrows():
    print(row[0])
    print(len(row[1]))
    print(row[1].keys())
    print(parseSettingString(row[1]["Left Therapy Description"]))
  
  


if __name__ == "__main__":
   main()
