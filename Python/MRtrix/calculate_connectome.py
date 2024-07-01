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
  return parser
  

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

  if not os.path.exists(c_matrix):
    c_matrix = os.path.join(profile["connectomePath"], "connectome_matrix.csv")
    
    
  connect_mat = np.loadtxt(c_matrix, delimiter=',')
  mu = np.loadtxt(os.path.join(profile["fibertractPath"], 'sift2_mu.txt'))
  
  lookup_main = pd.read_csv(profile["lookup_table"])
  lookup_key = pd.read_csv(profile["Connectome_maker"]["Output_files"]["matkey_outputname"])

  
  ROI_list_left = lookup_key.loc[lookup_key["Lookup Index"].isin(ROI_list_left_index),'MRtrix Index'].tolist()
  ROI_list_right = lookup_key.loc[lookup_key["Lookup Index"].isin(ROI_list_right_index),'MRtrix Index'].tolist()


  data = connect_mat[1:,1:] * mu #Remove unassigned tracts, multiply "Fudge Factor"
  if True in np.isnan(ROI_list_left):
      #raise Exception('Left region not given. Setting data to 0')
      print('Left region not given. Setting data to 0')
      data_left = np.zeros((1,len(data)))
      ROI_list_left = 0
  else:
      ROI_list_left = np.array([ROI_list_left]) - 1 #to deal with starting at 1
      data_left = data[:,ROI_list_left]
      
  if True in np.isnan(ROI_list_right):
      #raise Exception('Right region not given. Setting data to 0')
      print('Right region not given. Setting data to 0')
      data_right = np.zeros((1,len(data)))
      ROI_list_right = 0
  else:
      ROI_list_right = np.array([ROI_list_right]) - 1
      data_right = data[:,ROI_list_right]
      
      
      
  ROI_left = np.sum(data_left,axis=1).flatten() #collapse all regions
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
  right_region = region_connectivity.copy()
  right_region["Hemisphere"] = "Right"

  HCP_regions = [x for xs in connectome_regions.values() for x in xs] #List of all HCP regions

  for i in lookup_key["Lookup Index"].tolist():
    label = lookup_main["Labels"].loc[lookup_main["Index"] == i].tolist()[0].split('_')
    try:
        name = label[1]
    except:
        name = label[0] #to account for regions that do not have left/right split
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
        else:
            left_region[name] = ROI_left[matrix_index]
            right_region[name] = ROI_right[matrix_index]
        continue
    for key in connectome_regions.keys():
        if name in connectome_regions[key]:
            left_region[key] = left_region[key] + ROI_left[matrix_index]
            right_region[key] = right_region[key] + ROI_right[matrix_index]
                

#%%
  region_both = {'Region': left_region.keys(),'Left': left_region.values(), 'Right': right_region.values()}
  region_both = [left_region, right_region]
  df_regions = pd.DataFrame(data=region_both)
  
  df_outputfile = os.path.join(profile["connectomePath"],'Region_Connectivity_'+experiment+'.csv')

  df_regions.to_csv(df_outputfile, index=False)



  #setup output files for saving
  profile["connectome_connectome"] = { "Output_files":
        {"df_outputfile" : df_outputfile
        }
  }
  
  with open(args.profile, 'w') as fp:
    json.dump(profile, fp)
    
if __name__ == "__main__":
   main()
