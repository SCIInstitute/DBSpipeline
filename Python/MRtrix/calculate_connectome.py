# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 10:04:09 2024

usage:

python3 calculate_connectome.py --matrix <connectome_matrix> --subject <subject> --left_ROI <index> --right_ROI <index>

python3 calculate_connectome.py --matrix "/Users/jess/Dropbox/CT DBS Human/CENTURY S Patients/p102 (44)/MRtrix/Tractography/Cleaned/connectome_matrix_1.csv --subject "p102 (44)" --left_ROI 371 --right_ROI 372

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
                      
                      
  parser.add_argument("-s", "--subject", required=False,
                      help="subject to run.  cannot be used with --profile",
                      dest="subject")
  parser.add_argument("--left_ROI", type=int, required=False,
                      help="indexes for left ROIs.  cannot be used with --profile",
                      default=np.NaN, dest="ROI_list_left")
  parser.add_argument("--right_ROI", type=int, required=False,
                      help="indexes for right ROIs.  cannot be used with --profile",
                      default=np.NaN, dest="ROI_list_right")
  parser.add_argument("-e", "--experiment", required=False,
                      help="experiment lable.  cannot be used with --profile",
                      dest="experiment")
  parser.add_argument("-m", "--matrix", required=True,
                      help="connectome matrix.  ouput of calculate_connectome.sh",
                      dest="c_matrix")
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
    
    ROI_list_right = profile["right_ROI"]
    ROI_list_left = profile["left_ROI"]
    
  else:
    if np.isnan(args.ROI_list_left) or np.isnan(args.ROI_list_right):
        raise Exception('Not Valid Region')

    home = os.environ["DATADIR"]
    if os.environ["SYSNAME"]=="hipergator":
      rel_path1 = "Connectome"
      rel_path2 = "Tractography"
      rel_path3 = "Tractography"
      rel_path4 = "Segmentations"
    else:
      rel_path1 = "MRtrix/Connectome"
      rel_path2 = "MRtrix/Tractography/Cleaned"
      rel_path3 = "MRtrix/Tractography/Fibers/"
      rel_path4 = "MRtrix/Segmentations"
      
    ROI_list_right = args.ROI_list_right
    ROI_list_left = args.ROI_list_left

#home = os.getcwd()
# to match calculate_connectom.sh
    file_dir = os.path.join(home,  args.subject, rel_path2)
    
#Note: this notebook generates figures the rely on the data being from one region to everywhere else.
# ROI lists should be related as they will be combined into one region
# ${DATADIR}/${subject}/Connectome/connectome_matrix.csv in calculate_connectome.sh
#added to input
  c_matrix =args.c_matrix

  if not os.path.exists(c_matrix):
    c_matrix = os.path.join(profile["connectomePath"], "connectome_matrix.csv")
  connect_mat = np.loadtxt(c_matrix, delimiter=',')
  mu = np.loadtxt(os.path.join(profile["fibertractPath"], 'sift2_mu.txt'))


  # Lookup table
  LT_file = os.path.join(os.environ["CODEDIR"], 'Bash/Freesurfer/hcpmmp1_subcortex.txt')
  print(LT_file)
  label_table = pd.read_fwf(LT_file, header=None)
  labels = label_table[1].tolist()


  data = connect_mat[1:,1:] * mu #Remove unassigned tracts, multiply "Fudge Factor"
  if np.isnan(ROI_list_left):
      #raise Exception('Left region not given. Setting data to 0')
      print('Left region not given. Setting data to 0')
      data_left = np.zeros((1,len(data)))
      ROI_list_left = 0
  else:
      ROI_list_left = np.array([ROI_list_left]) - 1 #to deal with starting at 1
      data_left = data[:,ROI_list_left]
      
  if np.isnan(ROI_list_right):
      #raise Exception('Right region not given. Setting data to 0')
      print('Right region not given. Setting data to 0')
      data_right = np.zeros((1,len(data)))
      ROI_list_right = 0
  else:
      ROI_list_right = np.array([ROI_list_right]) - 1
      data_right = data[:,ROI_list_right]
      
      
      
  ROI_left = np.sum(data_left,axis=1) #collapse all regions
  ROI_right = np.sum(data_right,axis=1)
  ROI_left[ROI_list_left] = np.NAN #Remove regions from connectivity output
  ROI_right[ROI_list_right] = np.NAN



  percent = 100 #top k percentage of connections, not implemented at the moment
  top = percent/100
  Index_left = np.argsort(ROI_left) #Sort indicies and remove nan values
  Index_left = Index_left[np.argwhere(~np.isnan(ROI_left[Index_left]))].squeeze()[::-1]
  Index_right = np.argsort(ROI_right)
  Index_right = Index_right[np.argwhere(~np.isnan(ROI_right[Index_right]))].squeeze()[::-1]

  #ROI_left_top = ROI_left[Index_left[Index_left < 360]]
  ROI_left_top = ROI_left[Index_left]
  ROI_right_top = ROI_right[Index_right]
  labels_left = np.array(labels)[Index_left[Index_left < len(labels)]]
  labels_right = np.array(labels)[Index_right[Index_right < len(labels)]]

  with open(os.path.join(file_dir, 'labels_left.txt'),'w') as f:
      count = 0
      for label in labels_left:
          print(label,Index_left[count]+1,ROI_left_top[count],file=f)
          count += 1
  with open(os.path.join(file_dir, 'labels_right.txt'),'w') as f:
      count = 0
      for label in labels_right:
          print(label,Index_right[count]+1,ROI_right_top[count],file=f)
          count += 1
          
          
  file_path_1 = os.path.join(file_dir, 'labels_left.txt')
  file_path_2 = os.path.join(file_dir, 'labels_right.txt')

  f = open(file_path_1,'r')
  connectome_1 = f.readlines()
  f.close()

  f = open(file_path_2,'r')
  connectome_2 = f.readlines()
  f.close()

  shared = []
  conn_1 = []
  conn_2 = []
  count = 0
  for region in connectome_1:
      if region in connectome_2:
          shared.append(region.split()[0])
      else:
          conn_1.append(region.split()[0])

  for region in connectome_2:
      if region in connectome_1:
          continue
      else:
          conn_2.append(region.split()[0])

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
      
  #region_connectivity = {
  #    'Patient ID': PatientID,
  #    'Hemisphere': "",
  #    'Primary Visual Cortex': 0,
  #    'Early Visual Cortex': 0,
  #    'Dorsal Stream Visual Cortex': 0,
  #    'Ventral Stream Visual Cortex': 0,
  #    'MT+ Complex and Neighboring Visual Areas': 0,
  #    'Somatosensory and Motor Cortex': 0,
  #    'Paracentral Lobular and Mid Cingulate Cortex': 0,
  #    'Premotor Cortex': 0,
  #    'Posterior Opercular Cortex': 0,
  #    'Early Auditory Cortex': 0,
  #    'Auditory Association Cortex': 0,
  #    'Insular and Frontal Opercular Cortex': 0,
  #    'Medial Temporal Cortex': 0,
  #    'Lateral Temporal Cortex': 0,
  #    'Temporo-Parieto-Occipital Junction': 0,
  #    'Superior Parietal Cortex': 0,
  #    'Inferior Parietal Cortex': 0,
  #    'Posterior Cingulate Cortex': 0,
  #    'Anterior Cingulate and Medial Prefrontal Cortex': 0,
  #    'Orbital and Polar Frontal Cortex': 0,
  #    'Inferior Frontal Cortex': 0,
  #    'DorsoLateral Prefrontal Cortex': 0,
  #}

  left_region = region_connectivity.copy()
  left_region["Hemisphere"] = "Left"
  right_region = region_connectivity.copy()
  right_region["Hemisphere"] = "Right"
  left_leftover = connectome_1.copy()
  right_leftover = connectome_2.copy()

  for key in connectome_regions.keys():
      region_connectivity[key] = 0
      for region in connectome_1:
          if region.split()[0].split('_')[-1] in connectome_regions[key]:
              region_connectivity[key] = region_connectivity[key] + float(region.split()[-1].split('\n')[0])
              left_region[key] = left_region[key] + float(region.split()[-1].split('\n')[0])
              try:
                  left_leftover.remove(region)
              except:
                  continue
                  
  for region in left_leftover:
      keyname = region.split()[0].split('_')[-1]
      try:
          left_region[keyname] = left_region[keyname] + float(region.split()[-1].split('\n')[0])
      except:
          left_region[keyname] = float(region.split()[-1].split('\n')[0])
                  
  for key in connectome_regions.keys():
      region_connectivity[key] = 0
      for region in connectome_2:
          if region.split()[0].split('_')[-1] in connectome_regions[key]:
              region_connectivity[key] = region_connectivity[key] + float(region.split()[-1].split('\n')[0])
              right_region[key] = right_region[key] + float(region.split()[-1].split('\n')[0])
              try:
                  right_leftover.remove(region)
              except:
                  continue
                  
  for region in right_leftover:
      keyname = region.split()[0].split('_')[-1]
      try:
          right_region[keyname] = right_region[keyname] + float(region.split()[-1].split('\n')[0])
      except:
          right_region[keyname] = float(region.split()[-1].split('\n')[0])
          
  all_data = region_connectivity


  padding = ' ' * 35
  filepath = file_path_1.split('labels')[0]
  region_outputfile = os.path.join(filepath, 'Region_connectivity_'+experiment+'.txt')
  with open(region_outputfile, 'w') as f:
      for k,v in all_data.items():
          print('{:.50s} {}'.format(k + padding,v), file=f)
          
  region_both = {'Region': left_region.keys(),'Left': left_region.values(), 'Right': right_region.values()}
  region_both = [left_region, right_region]
  df_regions = pd.DataFrame(data=region_both)
  df_outputfile = os.path.join(filepath,'Region_Connectivity_'+experiment+'.csv')
  df_regions.to_csv( df_outputfile, index=False)
  
  profile["connectome_connectome"] = { "Output_files":
        {"df_outputfile" : df_outputfile,
          "region_outputfile" : region_outputfile
        }
  }
  
  with open(args.profile, 'w') as fp:
    json.dump(profile, fp)
    
if __name__ == "__main__":
   main()
