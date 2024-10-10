# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 10:04:09 2024

usage:

python3 calculate_connectome.py --matrix <connectome_matrix> --subject <subject> --left_ROI <index> --right_ROI <index>

python3 calculate_connectome.py --matrix "/Users/jess/Dropbox/CT DBS Human/CENTURY S Patients/p102 (44)/MRtrix/Tractography/Cleaned/connectome_matrix_1.csv --subject "p102 (44)" --left_ROI 371 --right_ROI 372

revised to match lookup table

l - 1001
r - 1016


@author: Matthew
"""



import pandas as pd
import os
import numpy as np
import argparse
import json


def build_parser():
  parser = argparse.ArgumentParser(
                prog = "Connectome_maker",
                description = "compiles a connectome nifti from disparate nifti segmentations.",
                epilog="output saves nifti files as defined by profile or settings"
                )

  # This will be implemented as rollout broadens
  parser.add_argument("-p", "--profile", required=False,
                      help="profile filename",
                      dest="profile")
  parser.add_argument("-s", "--stim", required=False,
                      help="include stimulations",
                      action = "store_true", dest="stim")
  parser.add_argument("-f", "--force", required=False,
                      help="force a rewrite of files",
                      action = "store_true", dest="rerun")
  return parser

def run_calc_connectome(df_outputfile, df_outputfile_ips, df_outputfile_con, c_matrix, experiment, ROI_list_right_index, ROI_list_left_index, lookup_table, matkey_outputname,  profile):

  subject= profile["subject"]
  experiment = profile["experiment"]

  connect_mat = np.loadtxt(c_matrix, delimiter=',')
  mu = np.loadtxt(os.path.join(profile["fibertractPath"], 'sift2_mu.txt'))
  
  lookup_main = pd.read_csv(lookup_table)
  lookup_key = pd.read_csv(matkey_outputname)

  
  ROI_list_left = lookup_key.loc[lookup_key["Lookup Index"].isin(ROI_list_left_index),'MRtrix Index'].tolist()
  ROI_list_right = lookup_key.loc[lookup_key["Lookup Index"].isin(ROI_list_right_index),'MRtrix Index'].tolist()


  data = connect_mat[1:,1:] * mu #Remove unassigned tracts, multiply "Fudge Factor"
  if True in np.isnan(ROI_list_left):
      #raise Exception('Left region not given. Setting data to 0')
      print('Left region not given. Setting data to 0')
      data_left = np.zeros((1,len(data)))
      ROI_list_left = 0
  else:
      ROI_list_left = np.array(ROI_list_left) - 1 #to deal with starting at 1
      data_left = data[:,ROI_list_left]
      print(data_left.shape)
      
  if True in np.isnan(ROI_list_right):
      #raise Exception('Right region not given. Setting data to 0')
      print('Right region not given. Setting data to 0')
      data_right = np.zeros((1,len(data)))
      ROI_list_right = 0
  else:
      ROI_list_right = np.array(ROI_list_right) - 1
      data_right = data[:,ROI_list_right]
      
      
  file_dir = profile["tractographyPath"]
  
  ROI_left = np.sum(data_left,axis=1).flatten() #collapse all regions
  print(ROI_left.shape)
  ROI_right = np.sum(data_right,axis=1).flatten()
  np.savetxt(os.path.join(file_dir, 'ROI_left.txt'), ROI_left,delimiter=',')
  np.savetxt(os.path.join(file_dir, 'ROI_right.txt'), ROI_right,delimiter=',')

  #HCP Macro-regions
  connectome_file = os.path.join(os.environ["CODEDIR"], "Python/connectomics/connectome_maps/HCP_MacroRegions.json")

  with open(connectome_file, 'r') as fp:
      connectome_regions = json.load(fp)

  subject_id = subject
  PatientID = subject_id.split('/')[0]
  #Add up regions to get macro-connectivity, any that are not part of HCP are put in on their own

  region_connectivity = {
      'Patient ID': PatientID,
      'Hemisphere': ""}
      
  region_connectivity = {
      'Patient ID': PatientID,
      'Hemisphere': "",
      'Primary Visual Cortex': 0,
      'Early Visual Cortex': 0,
      'Dorsal Stream Visual Cortex': 0,
      'Ventral Stream Visual Cortex': 0,
      'MT+ Complex and Neighboring Visual Areas': 0,
      'Somatosensory and Motor Cortex': 0,
      'Paracentral Lobular and Mid Cingulate Cortex': 0,
      'Premotor Cortex': 0,
      'Posterior Opercular Cortex': 0,
      'Early Auditory Cortex': 0,
      'Auditory Association Cortex': 0,
      'Insular and Frontal Opercular Cortex': 0,
      'Medial Temporal Cortex': 0,
      'Lateral Temporal Cortex': 0,
      'Temporo-Parieto-Occipital Junction': 0,
      'Superior Parietal Cortex': 0,
      'Inferior Parietal Cortex': 0,
      'Posterior Cingulate Cortex': 0,
      'Anterior Cingulate and Medial Prefrontal Cortex': 0,
      'Orbital and Polar Frontal Cortex': 0,
      'Inferior Frontal Cortex': 0,
      'DorsoLateral Prefrontal Cortex': 0,
  }

  left_region = region_connectivity.copy()
  left_region["Hemisphere"] = "Left"
  left_ips = left_region.copy()
  left_con = left_region.copy()
  right_region = region_connectivity.copy()
  right_region["Hemisphere"] = "Right"
  right_ips = right_region.copy()
  right_con = right_region.copy()

  HCP_regions = [x for xs in connectome_regions.values() for x in xs] #List of all HCP regions

  for i in lookup_key["Lookup Index"].tolist():
    label = lookup_main["Labels"].loc[lookup_main["Index"] == i].tolist()[0].split('_')
    try:
        name = label[1]
        hemi = label[0]
    except:
        name = label[0] #to account for regions that do not have left/right split
        hemi = ''
    matrix_index = lookup_key["MRtrix Index"].loc[lookup_key['Lookup Index'] == i].tolist()[0] - 1
    if matrix_index in ROI_list_left or matrix_index in ROI_list_right: #Remove connections to itself
        continue
    #### Add new changes here ####
    # Keep the loop, but add based on name only
    # if not in df, include it. If in df, add to existing
    # same for HCP regions
    # should keep everything fine unless problem added to lookup table
    if name not in HCP_regions: #Any non HCP regions
        if name in left_region.keys():
            left_region[name] = left_region[name] + ROI_left[matrix_index]
            right_region[name] = right_region[name] + ROI_right[matrix_index]
            if 'L' == hemi or not hemi:
               left_ips[name] = left_ips[name] + ROI_left[matrix_index]
               right_con[name] = right_con[name] + ROI_right[matrix_index]
            if 'R' == hemi or not hemi:
               right_ips[name] = right_ips[name] + ROI_right[matrix_index]
               left_con[name] = left_con[name] + ROI_left[matrix_index] 
        else:
            left_region[name] = ROI_left[matrix_index]
            right_region[name] = ROI_right[matrix_index]
            if 'L' == hemi or not hemi:
               left_ips[name] = ROI_left[matrix_index]
               right_con[name] = ROI_right[matrix_index]
               right_ips[name] = 0
               left_con[name] = 0
            if 'R' == hemi or not hemi:
               right_ips[name] = ROI_right[matrix_index]
               left_con[name] = ROI_left[matrix_index]
               left_ips[name] = 0
               right_con[name] = 0
        continue
    for key in connectome_regions.keys():
        if name in connectome_regions[key]:
            left_region[key] = left_region[key] + ROI_left[matrix_index]
            right_region[key] = right_region[key] + ROI_right[matrix_index]
            if 'L' == hemi or not hemi:
               left_ips[key] = left_ips[key] + ROI_left[matrix_index]
               right_con[key] = right_con[key] + ROI_right[matrix_index]
            if 'R' == hemi or not hemi:
               right_ips[key] = right_ips[key] + ROI_right[matrix_index]
               left_con[key] = left_con[key] + ROI_left[matrix_index]
                

#%%
  region_ips = [left_ips, right_ips]
  df_ips = pd.DataFrame(data=region_ips)
  
  df_ips.to_csv(df_outputfile_ips, index=False)

  region_con = [left_con, right_con]
  df_con = pd.DataFrame(data=region_con)
  df_con.to_csv(df_outputfile_con, index=False)
  
  
  region_both = {'Region': left_region.keys(),'Left': left_region.values(), 'Right': right_region.values()}
  region_both = [left_region, right_region]
  df_regions = pd.DataFrame(data=region_both)

  df_regions.to_csv(df_outputfile, index=False)
  
  return


def main():

  parser = build_parser()
  args = parser.parse_args()
#print(args.subject, args.ROI_list_left, args.ROI_list_right)

  if args.profile:
    with open(args.profile, 'r') as js_file:
      profile = json.load(js_file)
      
    subject= profile["subject"]
    experiment = profile["experiment"]
    
    file_dir = profile["tractographyPath"]
    
    ROI_list_right_index = profile["right_ROI"]
    ROI_list_left_index = profile["left_ROI"]
    
    
#Note: this notebook generates figures the rely on the data being from one region to everywhere else.
# ROI lists should be related as they will be combined into one region

# ${DATADIR}/${subject}/Connectome/connectome_matrix.csv in calculate_connectome.sh
#added to input
  c_matrix = profile["makeConnectomeMatrix"]["Output_files"]["connectome_matrix"]
  matkey_outputname = profile["Connectome_maker"]["Output_files"]["matkey_outputname"]

  if not os.path.exists(c_matrix):
    c_matrix = os.path.join(profile["connectomePath"], "connectome_matrix.csv")
    
  df_outputfile = os.path.join(profile["connectomePath"],'Region_Connectivity_'+experiment+'.csv')
  df_outputfile_isp = os.path.join(profile["connectomePath"],'Region_Connectivity_'+experiment+'_ipsilateral.csv')
  df_outputfile_con = os.path.join(profile["connectomePath"],'Region_Connectivity_'+experiment+'_contralateral.csv')
    
  run_calc_connectome(df_outputfile, df_outputfile_isp, df_outputfile_con, c_matrix,  experiment, ROI_list_right_index, ROI_list_left_index, profile["lookup_table"], matkey_outputname,  profile)


  #setup output files for saving
  profile["calculate_connectome"] = { "Output_files":
        { "df_outputfile" : df_outputfile,
          "df_outputfile_ips" : df_outputfile_isp,
          "df_outputfile_con" : df_outputfile_con
        }
  }
  
  
  if args.stim:
    if not "stim" in profile.keys():
      raise valueError("--stim flag (-s) used, but previous outputs are missing.  Please run Connectome_maker.py and makeConnectomeMatrix.py")
      
    stim_tags = profile["stim"]["Connectome_maker"]["stim_tags"]
    stim_ROIs = profile["stim"]["Connectome_maker"]["ROIs"]
    
    stim_df_outputfiles=[]
    stim_df_outputfiles_ips=[]
    stim_df_outputfiles_con=[]
    
    for idx in range(len(stim_tags)):
      stim_experiment = experiment+"_"+stim_tags[idx]
      stim_df_outputfile = os.path.join(profile["stimoutpath"], "Region_Connectivity_"+stim_experiment+".csv")
      stim_df_outputfiles.append(stim_df_outputfile)
      
      stim_df_outputfile_ips = os.path.join(profile["stimoutpath"], "Region_Connectivity_"+stim_experiment+"ipsolateral.csv")
      stim_df_outputfiles_ips.append(stim_df_outputfile_ips)
      
      stim_df_outputfile_con = os.path.join(profile["stimoutpath"], "Region_Connectivity_"+stim_experiment+"contralateral.csv")
      stim_df_outputfiles_con.append(stim_df_outputfile_con)
      
      c_matrix = profile["stim"]["makeConnectomeMatrix"]["Output_files"]["connectome_matrix"][idx]
      matkey_outputname = profile["stim"]["Connectome_maker"]["Output_files"]["matkey_outputnames"][idx]
      lookup_table = profile["stim"]["Connectome_maker"]["Output_files"]["lookup_tables"][idx]
      
      run_calc_connectome(stim_df_outputfile, stim_df_outputfile_ips, stim_df_outputfile_con, c_matrix, stim_experiment, [stim_ROIs[0]], [stim_ROIs[1]], lookup_table, matkey_outputname,  profile)
      
    profile["stim"]["calculate_connectome"] = { "Output_files":
        {"df_outputfile" : stim_df_outputfiles }
    }
    
  with open(args.profile, 'w') as fp:
    json.dump(profile, fp, sort_keys=True, indent=2)
    
if __name__ == "__main__":
   main()
