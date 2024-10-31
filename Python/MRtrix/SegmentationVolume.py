import nibabel as nib
import numpy as np
import pandas as pd
import argparse
import os
import sys
import nrrd
from scipy import io

def build_parser():
  parser = argparse.ArgumentParser(description='Inputs')
  parser.add_argument("-i", "--input", action="store", dest="inputFile", required=True, help="input file name.  nii or nrrd")
  parser.add_argument("-o", "--output", action="store", dest="outputFile", required=True, help="output file name, saved as matlab file")
  return parser
  
  
def getNiftiVoxelSize(header):
  # don't know if this will break for other data. as far as I can tell, this will be the 3D dims for the voxels
  
  voxSize = np.prod(header["pixdim"].astype(np.int32)[1:4])

  return voxSize


def getNRRDVoxelSize(header):
  
  if "spacing" in header.keys():
    voxSize = np.prod(header["spacing"])
  elif "thicknesses" in header.keys:
    voxSize = np.prod(header["thicknesses"])
  elif "space directions" in header.keys:
    sdir = header["space directions"]
    spacings = np.sqrt(np.sum(sdir*sdir, axis = 0))
    voxSize = np.prod(spacings)
  else:
    raise ValueError("cannot get voxel spacing from nrrd header")
    
  return voxSize
  
def segmentationVolumes(imgdata, volSize=1):
  checked = np.zeros(imgdata.shape)
  N_vox = np.prod(imgdata.shape)
  seg_vols = []
  seg_ind = []
  idx = (0,0,0)
  cntr = 0
  #
  while np.sum(checked) < N_vox:
#    print(idx)
#    print(N_vox - np.sum(checked))
#    print(cntr)
    if checked[idx] == 0:
      s_val = imgdata[idx]
      n_pval = np.sum(imgdata == s_val)
      checked[imgdata == s_val] = 1
      seg_ind.append(s_val)
      seg_vols.append(n_pval/volSize)
      cntr += 1
    #
    n_ck = np.where(checked == 0)
    if len(n_ck[0])>0:
      idx = (n_ck[0][0], n_ck[1][0], n_ck[2][0])
  #
  ord_ind = np.argsort(seg_ind)
  print(seg_vols)
  seg_vols_tab=[]
  for k in ord_ind:
    seg_vols_tab.append((seg_ind[k], seg_vols[k]))
  return seg_vols_tab
  
def segVolumesFile(inputFile):
  filename, extension = os.path.splitext(inputFile)
  print(inputFile)
  print(extension)
  if extension == ".nrrd":
    imgdata, header = nrrd.read(inputFile)
    voxSize = getNRRDVoxelSize(header)
  elif extension == ".nii":
    img = nib.load(inputFile)
    imgdata = img.get_fdata().astype(np.int32)
    voxSize = getNiftiVoxelSize(img.header)
  elif inputFile[-7:] == ".nii.gz":
    filename = inputFile[:-7]
    extension = ".nii.gz"
    img = nib.load(inputFile)
    imgdata = img.get_fdata().astype(np.int32)
    voxSize = getNiftiVoxelSize(img.header)
  else:
    raise ValueError("cannot read file: ", inputFile)
    
  segVols = segmentationVolumes(imgdata, voxSize)
  
  return segVols
  
  
def main():

  parser = build_parser()
  args = parser.parse_args()

  inputFile = args.inputFile
  if not os.path.exists(inputFile):
    raise ValueError("input file not found:", inputFile)
  
  segVols = segVolumesFile(inputFile)
    
  outputFile = filename+".mat"
  print(outputFile)
  
  io.savemat(outputFile, {"segmentationVolumes" : np.array(segVols)})
  print("volume measurements saved to file")
  
  
  

if __name__ == "__main__":
   main()
