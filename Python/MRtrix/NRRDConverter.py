import nrrd
import nibabel as nib
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Inputs')
parser.add_argument('--NRRD',action='store',dest='inputFile',default=0)
args = parser.parse_args()

inputFile = args.inputFile
outputFile = inputFile.replace("nrrd", "nii.gz")
#inputFile = "T1_pre_ACPCspace.nrrd"
#outputFile = "T1_pre_ACPCspace_converted.nii.gz"

#bestNii = nib.load("T1_pre_ACPCspace.nii.gz")

readdata, header = nrrd.read(inputFile)
if header["space"] == "left-posterior-superior":
  tform = np.eye(4)
  tform[:3,:3] = 0
  tform[:3,:3] += (header["space directions"].T)
  tform[:3,-1] += (header["space origin"])
  tform[:2,:] *= -1

  niiHeader = nib.Nifti1Header()
  niiHeader.set_qform(tform)
  niiHeader.set_sform(tform)
  niiHeader.set_data_shape(readdata.shape)
  niiHeader.set_xyzt_units(2)
  nii = nib.Nifti1Image(readdata, niiHeader.get_best_affine(), niiHeader)
  nib.save(nii, outputFile)
  
elif header["space"] == "3D-right-handed":
  tform = np.eye(4)
  tform[:3,:3] = 0
  tform[:3,:3] += (header["space directions"].T)
  tform[:3,-1] += (header["space origin"])
#  tform[:2,:] *= -1
  
#  print(tform[:2,:])
#  print(header["space directions"])
#  print(tform)

  niiHeader = nib.Nifti1Header()
  niiHeader.set_qform(tform)
  niiHeader.set_sform(tform)
  niiHeader.set_data_shape(readdata.shape)
  niiHeader.set_xyzt_units(2)
  
  nii = nib.Nifti1Image(readdata, niiHeader.get_best_affine(), niiHeader)
  nib.save(nii, outputFile)

else:
  raise Exception("I am too lazy to implement other space, so please contact Jackson to add more support for this NRRD file.")

