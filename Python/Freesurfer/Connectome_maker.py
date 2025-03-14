# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 16:07:45 2023

this script will run through the connectome lookup table to generate
a compilation of atlases or subsets into a single volume.
It can be used to swap out different atlases.

with new parcelation segmentation


@author: Matthew
"""

#For use in the working directory
import nibabel
import json
import nibabel.processing
import numpy as np
import pandas as pd
import argparse
import os
import sys
import nrrd
#print(os.path.join(os.path.dirname(__file__), "..", "MRtrix" ))
#sys.path.append(os.path.join(os.path.dirname(__file__), "..", "MRtrix" ))
print(os.path.join(os.environ["CODEDIR"], "Python/MRtrix" ))
sys.path.append(os.path.join(os.environ["CODEDIR"], "Python/MRtrix" ))
 
from NRRDConverter import readNRRD

def build_parser():
  parser = argparse.ArgumentParser(
                prog = "Connectome_maker",
                description = "compiles a connectome nifti from disparate nifti segmentations.",
                epilog="output saves nifti files as defined by profile or settings"
                )

  # This will be implemented as rollout broadens
  parser.add_argument("-p", "--profile", required=True,
                      help="profile filename",
                      dest="profile")
  parser.add_argument("-s", "--stim", required=False,
                      help="include stimulations",
                      action = "store_true", dest="stim")
  parser.add_argument("-f", "--force", required=False,
                      help="force a rewrite of files",
                      action = "store_true", dest="rerun")
  return parser


#Load lookup table
default_lookup = os.path.join(os.environ["CODEDIR"], 'Bash/Freesurfer/connectome_lookup_v1.csv')
default_experiment=""

def append_lookup_file(profile, **kwargs):
  # stim regions will start with 3000s?
  # always want the stim regions to go last because of overwriting
  default_kwargs = { "begin_idx" : 3000 }
  kwargs = { **default_kwargs, **kwargs }
 
  begin_idx = kwargs["begin_idx"]

  experiment = profile["experiment"]
  stim_table = pd.read_csv(profile["stim_table"],index_col=False)
  stim_out = profile["stimoutpath"]
  
  lookup = pd.read_csv(profile["lookup_table"],index_col=False)
  
  if not os.path.exists(stim_out):
    os.makedirs(stim_out)
  
  stim_output_files = {"lookup_tables" : [], "nifti_lookup_outputfiles" : [], "nifti_outputfiles" : [], "matkey_outputnames" : [], "ROIs" : {}}
  
  ROI_table = {}
  for idx, col in enumerate(stim_table.columns):
    stim_output_files["ROIs"][col] = []
    ROI_table[col] = begin_idx + idx
  
  stim_tags =  []
  for row in stim_table.iterrows():
    stim_string = "stim_"
    stim_fnames = []
    stim_labels = []
    #
    ROIs = []
    cnt = begin_idx
    for stim_key, stim_fname in row[1].items():
    #      print(stim_key, stim_fname)
      if isinstance(stim_fname, float) and np.isnan(stim_fname):
        stim_output_files["ROIs"][stim_key].append(np.nan)
        continue
      stim_fnames.append(stim_fname)
      sfroot, ext = os.path.splitext(stim_fname)
      stript_sfroot = "_".join([ t for t in sfroot.split("_") if not ("stim".casefold() in t.casefold() or  stim_key.casefold() in t.casefold()) ])
      stim_labels.append(stim_key[0] + "_" + stript_sfroot)
      stim_string+=stim_key + "_" + stript_sfroot + "-"
      stim_output_files["ROIs"][stim_key].append(cnt)
      ROIs.append(cnt)
      cnt += 1
      
    stim_lookup_fname = os.path.join(stim_out, "connectome_lookup_"+stim_string+".csv")
    stim_output_files["lookup_tables"].append(stim_lookup_fname)
    stim_tags.append(stim_string)

    stim_output_files["nifti_lookup_outputfiles"].append( os.path.join(stim_out, "HCP_parc_all_"+experiment+"_"+stim_string+"_lookup.nii.gz"))
    stim_output_files["nifti_outputfiles"].append( os.path.join(stim_out, "HCP_parc_all_"+experiment+"_"+stim_string+".nii.gz"))
    stim_output_files["matkey_outputnames"].append( os.path.join(stim_out, "MRtrix_index_key_"+experiment+"_"+stim_string+".csv"))
    
    stim_dict = {
              "Index" : ROIs,
              "Labels" : stim_labels,
              "Filename" : stim_fnames,
              "File Index" : [1]*len(stim_fnames),
              "Path" : "Stim",
    }
    
    pd.concat((lookup, pd.DataFrame(stim_dict)), ignore_index=True).to_csv(stim_lookup_fname)
  
  stim_output_files["stim_tags"] = stim_tags
    
  return stim_output_files
  
def check_lookup_files(anat_lookup_file, lookup_file):
# TODO: not sure if needed, but will need to be implemented
  anat_lookup = pd.read_csv(anat_lookup_file,index_col=False)
  stim_lookup = pd.read_csv(lookup_file,index_col=False)
  
  return
  
  
def table_2_atlas_stim(st_lookup_file, profile, output_files, **kwargs ):
  default_kwargs = {"rerun" : False}
  kwargs = { **default_kwargs, **kwargs}

  print("==========")
  print("Appending Atlas file from for stim lookup table: ")
  print(st_lookup_file)
  
  anat_output_files =  profile["Connectome_maker"]["Output_files"]

  anat_out_check = [os.path.exists(f_name ) for f_var, f_name in anat_output_files.items() ]
  
  if not all(anat_out_check):
    raise ValueError("some how base files do not exist, yet they are needed for the stimulation pipelines")
  
#  anat_lookup_file = profile["lookup_table"]
  
#  check_lookup_files(anat_lookup_file, st_lookup_file)

# add stim from last entry of the anatomical lookup table
  stim_lookup = pd.read_csv(st_lookup_file,index_col=False)
  anat_lookup = pd.read_csv(profile["lookup_table"],index_col=False)
  
  HCP = nibabel.load(anat_output_files["nifti_lookup_outputfile"])
  All_data = HCP.get_fdata()
  
  st_index = np.array(stim_lookup['Index'])
  anat_index = np.array(anat_lookup['Index'])
  
  l_anat_idx = np.nonzero(st_index == anat_index[-1])[0][0]
  
  seg_files = stim_lookup['Filename'][l_anat_idx+1:].unique()
  
  return add_files_2_atlas(All_data, HCP, stim_lookup, seg_files, profile, output_files)
  
    
  

def add_files_2_atlas(All_data, HCP, lookup, seg_files, profile, output_files, **kwargs):

  

  for file in seg_files:
    seg_dirs = lookup['Path'][lookup['Filename'] == file].unique()[0]
    main_index = np.array(lookup['Index'][lookup['Filename'] == file])
    local_index = np.array(lookup['File Index'][lookup['Filename'] == file])
    #
    fullfile = os.path.join(profile["segPath"], seg_dirs, file)
    #
  #    # saving resampled images to save time
  #    froot, ext = os.path.splitext(file)
  #    if ext == ".gz":
  #      froot_, ext_ = os.path.splitext(froot)
  #      if ext_ == ".nii":
  #        froot = froot_
  #        ext = ext_ + ext
  #
  #    resamp_file = froot + "_resample" + ".nii.gz"
  #    resamp_fullfile = os.path.join(profile["segPath"], seg_dirs, resamp_file)
  #
  #    if kwargs["rerun"] or not os.path.exists(resamp_fullfile):
  #
    if os.path.splitext(file)[1] == ".nrrd":
      img = readNRRD(fullfile)
    else:
      img = nibabel.load(fullfile)
    #
    img_resamp = nibabel.processing.resample_from_to(img, HCP,order=0)
#    print(img_resamp)
    img_data = img_resamp.get_fdata()
    data_add = img_data.copy()
    for j in range(0,len(local_index)):
      data_add[img_data == local_index[j]] = int(main_index[j])
    #
    All_data[data_add != 0] = data_add[data_add != 0]
    
  All_data = All_data.astype(int)
  All_to_nii = nibabel.Nifti1Image(All_data, HCP.affine, HCP.header)
  
  nibabel.save(All_to_nii, output_files["nifti_lookup_outputfile"])

  #Create Key for MRtrix image
  mrtrix_key = {  'Lookup Index' : np.unique(All_data)[1:].tolist(),
                  'MRtrix Index' : list(range(1,len(np.unique(All_data)[1:].tolist())+1))
  }
  
  mrtrix_data = All_data.copy()
  for i in range(0,len(mrtrix_key['Lookup Index'])):
      mrtrix_data[All_data == mrtrix_key['Lookup Index'][i]] = mrtrix_key['MRtrix Index'][i]
      
  mrtrix_to_nii = nibabel.Nifti1Image(mrtrix_data, HCP.affine, HCP.header)
  nibabel.save(mrtrix_to_nii, output_files["nifti_outputfile"] )
  mrtrix_save = pd.DataFrame(data=mrtrix_key)
  
  mrtrix_save.to_csv(output_files["matkey_outputname"])
  
  print("files generated:")
  print(output_files)
  
  return mrtrix_save
  
  
  
def table_2_atlas(lookup_file, profile, output_files, **kwargs ):
  default_kwargs = {"rerun" : False}
  kwargs = { **default_kwargs, **kwargs}

  print("==========")
  print("Making Atlas file from lookup table: ")
  print(lookup_file)
  
  lookup = pd.read_csv(lookup_file,index_col=False)
  seg_files = lookup['Filename'].unique()
  #seg_dirs = lookup['Path'].unique()
  seg_dirs = lookup['Path'][lookup['Filename'] == seg_files[0]].unique()[0]

  #Load HCP first always. This will be the reference
#  print(seg_files)
  HCP = nibabel.load(os.path.join(profile["segPath"], seg_dirs, seg_files[0]))
  
  HCP_data = HCP.get_fdata()
  main_index = np.array(lookup['Index'][lookup['Filename'] == seg_files[0]])
  local_index = np.array(lookup['File Index'][lookup['Filename'] == seg_files[0]])

  All_data = HCP_data.copy()
  for i in range(0,len(local_index)):
    All_data[HCP_data == local_index[i]] = int(main_index[i])


  return add_files_2_atlas(All_data, HCP, lookup, seg_files, profile, output_files)
  
  

def main():

  parser = build_parser()
  args = parser.parse_args()
  
  
  with open(args.profile, 'r') as js_file:
    profile = json.load(js_file)
    
  subject= profile["subject"]
  experiment = profile["experiment"]
  lookup_file = profile["lookup_table"]

  if not subject:
    print("need subject string")
    quit()
  #%%

  print(lookup_file)
  
  print(experiment)

  #Get patient
  #filepath = args.filepath + '/' + subject + '/'
  print('Python Input',subject)
  filepath = profile["rootpath"]
  
  nifti_lookup_outputfile = os.path.join(profile["connectomePath"], 'HCP_parc_all_'+experiment+'_lookup.nii.gz')
  nifti_outputfile = os.path.join(profile["connectomePath"], 'HCP_parc_all_'+experiment+'.nii.gz')
  matkey_outputname=os.path.join(profile["connectomePath"], 'MRtrix_index_key_'+experiment+'.csv')

  output_files =  {"nifti_outputfile": nifti_outputfile,
          "nifti_lookup_outputfile" : nifti_lookup_outputfile,
          "matkey_outputname" : matkey_outputname}

  out_check = [os.path.exists(f_name ) for f_var, f_name in output_files.items() ]
  
#  print(out_check)
  
  if all(out_check):
    print("files all exist")
    print(args.rerun)
    if args.rerun:
      print("overwriting output files")
      table_2_atlas(lookup_file, profile, output_files, rerun = args.rerun  )
      profile["Connectome_maker"] = { "Output_files": output_files}
      
      with open(args.profile, 'w') as fp:
        json.dump(profile, fp, sort_keys=True, indent=2)
    else:
      print("output files exist.  Use '-f' to force overwrite")
  else:
    # make sure to run the anatomy data
    # TODO: restructure to avoid all the repeat calls and profiles saves
    table_2_atlas(lookup_file, profile, output_files, rerun = args.rerun  )
    profile["Connectome_maker"] = { "Output_files": output_files}
    
    with open(args.profile, 'w') as fp:
      json.dump(profile, fp, sort_keys=True, indent=2)
  
  
  
  if args.stim:
    print("running stimulation data")
    if "stim_table" in profile.keys():
      if not os.path.exists(profile["stim_table"]):
        raise ValueError("cannot find stimulation table: "+profile["stim_table"])
    else:
      raise ValueError("Cannot run --stim (-s) option without stimulation table filepath (profile['stim_table'])")

    stim_output_files = append_lookup_file(profile)
#    print("--- checking files ---")
#    print(stim_output_files)
    
    stim_out_check = [  os.path.exists(f_name )  for f_var, fn_list in stim_output_files.items() if not (f_var=="ROIs" or f_var=="stim_tags") for f_name in fn_list  ]
    
#    print(stim_out_check)
#    print(np.all(stim_out_check))
    
    if np.all(stim_out_check):
      print("stim files all exist")
      print(args.rerun)
      if args.rerun:
        print("overwriting stim output files")
      else:
        print("stim output files exist.  Use '-f' to force overwrite")
        return
    
    for idx in range(len(stim_output_files["lookup_tables"])):
      
      st_lookup_file = stim_output_files["lookup_tables"][idx]
#      st_lookup = pd.read_csv(stim_output_files["lookup_tables"][idx], index_col=False)
      st_output_fs = {"nifti_outputfile": stim_output_files["nifti_outputfiles"][idx],
          "nifti_lookup_outputfile" : stim_output_files["nifti_lookup_outputfiles"][idx],
          "matkey_outputname" : stim_output_files["matkey_outputnames"][idx]
      }
      
#      print("should make these files :")
#      print(st_output_fs)
      
      table_2_atlas_stim(st_lookup_file, profile, st_output_fs, rerun = args.rerun )
    
    ROIs = stim_output_files["ROIs"]
    stim_tags = stim_output_files["stim_tags"]
    stim_output_files.pop("ROIs")
    stim_output_files.pop("stim_tags")
    
    if "stim" in profile.keys():
      profile["stim"]["Connectome_maker"] = {
                             "Output_files" : stim_output_files,
                             "ROIs" : ROIs,
                             "stim_tags" : stim_tags
      }
    else:
      profile["stim"] = { "Connectome_maker" :
                            { "Output_files" : stim_output_files,
                              "ROIs" : ROIs,
                              "stim_tags" : stim_tags
                            }
                        }
                      
        
    with open(args.profile, 'w') as fp:
      json.dump(profile, fp, sort_keys=True, indent=2)
    

if __name__ == "__main__":
   main()

#%%
'''
#Load HCP and grab all other nifti volumes to add
HCP = nibabel.load(glob.glob(r'./*HCP.nii.gz')[0])
files = glob.glob(r'./*[!HCP].nii.gz')

#Re-label each volume to match with HCP data
HCP_data = HCP.get_fdata()
count = int(np.max(HCP_data)) #highest value in labelmap
All_data = HCP_data.copy()
for file in files:
    count = count + 1
    filename = file.split('/')[1].split('.nii')[0]
    img = nibabel.load(file)
    img_resamp = nibabel.processing.resample_from_to(img, HCP,order=1)
    
    img_data = img_resamp.get_fdata()
    All_data[img_data != 0] = count
    #All_data = np.add(All_data,img_data)
    img_to_nii =  nibabel.Nifti1Image(img_data, img_resamp.affine, img_resamp.header)
    nibabel.save(img_to_nii, filename+'_resamp.nii.gz')
    
#Save as new nifti
All_to_nii = nibabel.Nifti1Image(All_data, HCP.affine, HCP.header)
nibabel.save(All_to_nii, 'HCP_parc_all.nii.gz')
'''
