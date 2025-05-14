import numpy as np
import pandas as pd
import argparse
import os
import sys
import nrrd
import json
import re
import scipy.io


def build_parser():
  parser = argparse.ArgumentParser(
                prog = "BravoToSimulation",
                description = "Converts Bravo clinical data into data that SCIRun can use for simulations",
                epilog="outputs a simulation table, matrix of contact amplitudes, and other data needed for SCIRun"
                )
  parser.add_argument("-p", "--profile", required=True,
                      help="profile filename",
                      dest="profile")
#  parser.add_argument("-o", "--output", required=False,
#                      help="output directory", dest="output_dir", type=str, default="")
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
  
def settingsToMatrix(settings_df, contact_list=[],  **kwargs):
  # TODO: move to hardware parameter file
  def_contact_list = [ "E0", "E1A", "E1B", "E1C", "E2A", "E2B", "E2C", "E7"]
  # from Matthew
  #  Electrode 1: Left GPi
  #  Electrode 2: Left CM
  #  Electrode 3: Right GPi
  #  Electrode 4: Right CM
  device_list = [ "Left GPi", "Left CM", "Right GPi", "Right CM" ]
  
  if not contact_list:
    contact_list = def_contact_list
  #
  n_settings = len(settings_df)
  l_devices = settings_df["Left Device"]
  r_devices = settings_df["Right Device"]
  #
#  devices_sett = [ (l_devices[k], r_devices[k]) for k in range(n_settings) ]
#  uniq_devices = list(set(devices_sett))
#  
#  # this assumes no mixing of devices (GPI and CM). Also, this may cause problems if there are blanks in the device fields
#  num_leads = sum([len(t) for t in uniq_devices])
  #
  # assumes in-name labeling (left/right)
  devices_sett = list(l_devices) + list(r_devices)
  in_dev = []
  out_dev = []
  for dev in devices_sett:
    if dev in device_list:
      in_dev.append(dev)
    else:
      out_dev.append(dev)
  
  uniq_known_devices = list(set(in_dev))
  uniq_unknown_devices = list(set(out_dev))
  num_leads = len(uniq_known_devices)
  if (not num_leads == len(device_list)) or len(uniq_unknown_devices)>0:
    raise ValueError("unknown device or device set detected.  Need to implement more stuff")
  #
  num_contacts = len(contact_list)
  num_contacts_tot = num_contacts*num_leads
  #
  all_filestrings =[]
  all_mats = []
  stim_files={"Left" : [], "Right" : []}
  file_set = set()
#
  for row in settings_df.iterrows():
  #
    file_str, amp_mat = extractSettings(row, device_list, contact_list, **kwargs )
#    print("row iter")
#    print(file_str)
  #  print(amp_mat)
    #
    for k in range(len(file_str)):
      s_ky = list(stim_files.keys())[k]
#      print("amplitude value")
#      print(amp_mat[k])
      amp_check = np.max(np.abs(amp_mat[k][np.isfinite(amp_mat[k])]))
#      print(amp_check)
      if not file_str[k]:
        stim_files[s_ky] = ""
        continue
      if amp_check==0:
        continue
        #
      if not file_str[k] in file_set:
        all_filestrings.append(file_str[k])
        all_mats.append(amp_mat[k])
        #
      stim_files[s_ky].append("Stimulation_"+file_str[k]+".nrrd")
      file_set.add(file_str[k])
  #
  return stim_files, all_mats, all_filestrings
      
      
      
    
#    print(row[0])
#    print(len(row[1]))
#    print(row[1].keys())
#    print(parseSettingString(row[1]["Left Therapy Description"]))
    
def extractSettings(df_row, device_list, contact_list, **kwargs ):
  #
  num_contacts = len(contact_list)
  #
  r_amp_dict = {}
  l_amp_dict = {}
  for dev in device_list:
    r_amp_dict[dev] = np.empty(num_contacts)
    r_amp_dict[dev][:] = np.nan
    l_amp_dict[dev] = np.empty(num_contacts)
    l_amp_dict[dev][:] = np.nan
  #
  l_dev = df_row[1]["Left Device"]
  r_dev = df_row[1]["Right Device"]
  r_maxAmp = df_row[1]["Right Max Amplitude"]
  l_maxAmp = df_row[1]["Left Max Amplitude"]
  l_sett = parseSettingString(df_row[1]["Left Therapy Description"])
  r_sett = parseSettingString(df_row[1]["Right Therapy Description"])
  amp_unit = "mA"
  #
  l_mat = np.empty(num_contacts)
  l_mat[:] = np.nan
  #
  r_mat = np.empty(num_contacts)
  r_mat[:] = np.nan
  #
  l_cath_ind = [contact_list.index(l_s) for l_s in l_sett["cathodes"]]
  l_mat[l_cath_ind] = l_maxAmp/len(l_cath_ind)
  #
  l_ann_ind = [contact_list.index(l_s) for l_s in l_sett["annodes"] if not l_s=="CAN" ]
  l_mat[l_ann_ind] = 0
  #
  r_cath_ind = [contact_list.index(r_s) for r_s in r_sett["cathodes"]]
  r_mat[r_cath_ind] = r_maxAmp/len(r_cath_ind)
  #
  r_ann_ind = [contact_list.index(r_s) for r_s in r_sett["annodes"] if not r_s=="CAN" ]
  r_mat[r_ann_ind] = 0
  #
  l_amp_dict[l_dev] = l_mat
  r_amp_dict[r_dev] = r_mat
  #
  l_fstring = re.sub(r"\s+", "", l_dev) + "_+" + "+".join(l_sett["cathodes"]) + "-" + "-".join(l_sett["annodes"]) + "_maxAmp_"+ str(l_maxAmp) + amp_unit
  r_fstring = re.sub(r"\s+", "", r_dev) + "_+" + "+".join(r_sett["cathodes"]) + "-" + "-".join(r_sett["annodes"]) + "_maxAmp_"+ str(r_maxAmp) + amp_unit
  #
  l_amp_mat = np.concatenate(list(l_amp_dict.values()))
  r_amp_mat = np.concatenate(list(r_amp_dict.values()))
  #
  return (l_fstring, r_fstring), [l_amp_mat, r_amp_mat]
    
  # TODO: move to another script that would generate parameters from the input. The inputs will vary by study, so we'd want to find a general enough format to help make that work.
    

def main():

  parser = build_parser()
  args = parser.parse_args()
  
  with open(args.profile, 'r') as js_file:
    profile = json.load(js_file)

  settings_df = pd.read_csv(args.settings_fname, delimiter=',')
  
  print(settings_df)
  
  stim_files, all_mats, all_filestrings = settingsToMatrix(settings_df)
  
  stim_param_flist = []
  stim_param_dir = os.path.join(profile["SRFilesPath"],"stim_params")
  profile["stim_param_dir"] = stim_param_dir
  if not os.path.exists(stim_param_dir):
    os.makedirs(stim_param_dir)
  for fstr, mat in zip(all_filestrings, all_mats):
    fname = fstr+".mat"
    stim_param_flist.append(fname)
    full_fn = os.path.join(stim_param_dir, fname)
    scipy.io.savemat(full_fn, {"params" : mat, "param_str" : fstr})
  
  profile["stim_param_files"] = stim_param_flist
  
  full_mat = np.vstack(all_mats).T
  scipy.io.savemat(os.path.join(stim_param_dir, "all_params.mat"), {"allparams" : full_mat, "allparam_str" : all_filestrings})
    
  
  tab_fname = profile["experiment"]+".csv"
  if not os.path.exists(profile["stimsegpath"]):
    os.makedirs(profile["stimsegpath"])
  stim_table = os.path.join(profile["stimsegpath"],tab_fname)
  pd.DataFrame(data = stim_files ).to_csv(stim_table, index=False)
  profile["stim_table"] = stim_table
  
  
  with open(args.profile, 'w') as fp:
    json.dump(profile, fp, sort_keys=True, indent=2)
  
#  for row in settings_df.iterrows():
#    print(row[0])
#    print(len(row[1]))
#    print(row[1].keys())
#    print(parseSettingString(row[1]["Left Therapy Description"]))
  
  


if __name__ == "__main__":
   main()
