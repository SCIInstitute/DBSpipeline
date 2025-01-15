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
