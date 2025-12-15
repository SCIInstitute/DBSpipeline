import os
import sys
import argparse

import nrrd
import numpy as np
import nibabel as nib

from AxisCheckerDefaults import axisObjectTemplate, nrrdSpaceCodes, chiralityTable


def build_parser():
  parser = argparse.ArgumentParser(
                prog = "AxisChecker",
                description = "checking the Axes of nifti and nrrd files",
                epilog="currently doesn't do anything but check"
                )

  # This will be implemented as rollout broadens
  parser.add_argument('filenames', nargs='+',
            help = "list of image filenames to check axes (nrrd or nifti file types).  Minimum one filename. With multiple filenames, subsequent files will be checked against the first" )
  
  return parser
  
  
def nrrdDimCheck(header):

  """
  Designed for NRRD005 
  TODO: handling for vector, tensor data (need to find a good example)
  """
  
#  print(header["space directions"].shape)
  reported_dim = header["dimension"]
  if not len(header["sizes"]) == reported_dim:
    print(len(header["sizes"]))
    return False
  elif not header["space directions"].shape[0] == reported_dim:
    print(header["space directions"].shape)
    return False
  elif not len(header["kinds"]) == reported_dim:
    print(len(header["kinds"]))
    return False
  elif not len(header["space origin"]) == reported_dim:
    print(len(header["space origin"]))
    return False

  return reported_dim
  
  
  
  
  
def getNrrdAxes(filename, **kwargs):
  """
  Designed for NRRD005 and 3D data (space dim = 3, no time serieses)
  TODO: handling for vector, tensor data
  """
  
  dkwargs = {"verbose" : False, "axisObject" : {} }
  kwargs  = {**dkwargs, **kwargs}
  

  if type(kwargs["axisObject"]) is dict:
    axisObject = kwargs["axisObject"]
  else:
    print("keyword arg 'axisObject' is expected to be a dict")
    axisObject = {}
  
  if not axisObject:
    axisObject = axisObjectTemplate.copy()
  
  imgdata, header = nrrd.read(filename)
  
  dim = nrrdDimCheck(header)
  
  if not dim == 3:
    raise ValueError("This tools currently only works with 3D data")
    
  
#  print(header["space"])
#  print(nrrdSpaceCodes.items())
  
  axis_space = next(key for key, v_list in nrrdSpaceCodes.items() if  header["space"] in v_list )
#  print(axis_space)

  axisObject["axis_space"] = axis_space
  axisObject["affine"][0:3,0:3] = header["space directions"]
  axisObject["affine"][0:3,3] = header["space origin"]
  
  axisObject["source"] = "nrrd"
  
  axisObject["header"] = header
    
  if kwargs["verbose"]:
    print("axisObject = ", axisObject)
#    print("nrrd header = ", header)
    
  
  
  return axisObject
  

def checkNrrdAxes(filename, **kwargs):
  dkwargs = {"verbose" : False }
  kwargs  = {**dkwargs, ** kwargs}
  
  imgdata, header = nrrd.read(filename)
  
  if kwargs["verbose"]:
    print("nrrd header = ", header)
  
  return getNrrdAxes(filename, **kwargs)


def getNiftiAxes(filename, **kwargs):
  """
  assumes nifti1
  
    Additional Info
  # nifti header info: https://www.nitrc.org/docman/view.php/26/64/nifti1.h
  # nibabel nifti header docs: https://nipy.org/nibabel/nifti_images.html
  """
  
  dkwargs = {"verbose" : False, "axisObject" : {} }
  kwargs  = {**dkwargs, **kwargs}
  

  if type(kwargs["axisObject"]) is dict:
    axisObject = kwargs["axisObject"]
  else:
    print("keyword arg 'axisObject' is expected to be a dict")
    axisObject = {}
  
  if not axisObject:
    axisObject = axisObjectTemplate.copy()
  
  img = nib.load(filename)
  
  axisObject["affine"] = img.affine
  axis_space = "".join(nib.aff2axcodes(img.affine))
#  print(axis_space)
  axisObject["axis_space"] = axis_space
  axisObject["source"] = "nifti"
  
  axisObject["header"] = img.header
  

  if kwargs["verbose"]:
    print("Affine = ",  img.affine)
    print("ax codes = ", nib.aff2axcodes(img.affine))
    print("affine = ", img.header.get_sform())
    print("code = ", img.header["sform_code"])
    print("base affine = ", img.header.get_base_affine())
    print("base ax codes = ", nib.aff2axcodes(img.header.get_base_affine()))
  #  print("header = ", img.header)
    print("axisObject = ", axisObject)
    
  

  return axisObject

def checkNiftiAxes(filename, **kwargs):
  
  # TODO: check the pixdim and dim
  # nifti header info: https://www.nitrc.org/docman/view.php/26/64/nifti1.h
  # nibabel nifti header docs: https://nipy.org/nibabel/nifti_images.html
  

  return getNiftiAxes(filename, **kwargs)
  
def checkRotations(axes1, axes2, **kwargs):
  dkwargs = {"max_theta" : np.pi/6 }
  kwargs = {**dkwargs, **kwargs}
  
  #TODO: check for permutation differences?
  
  chir1 = next(key for key, v_list in chiralityTable.items() if  axes1["axis_space"] in v_list )
  chir2 = next(key for key, v_list in chiralityTable.items() if  axes2["axis_space"] in v_list )
  
  print(chir1, chir2)

  norm1 = np.sqrt(np.sum(axes1["affine"][0:3,0:3]*axes1["affine"][0:3,0:3], axis = 0))
  rot1 = axes1["affine"][0:3,0:3]/norm1
  
  print(axes1["affine"][0:3,0:3])
  print(rot1)
  print(norm1)
  
  norm2 = np.sqrt(np.sum(axes2["affine"][0:3,0:3]*axes2["affine"][0:3,0:3], axis = 0))
  rot2 = axes2["affine"][0:3,0:3]/norm2
  
  print(axes2["affine"][0:3,0:3])
  print(rot2)
  print(norm2)
  
  diff_mat = np.dot(rot1, rot2.T)
  print("different mat : ", diff_mat)
  
  cos_theta =  (np.trace(diff_mat)-1)/2
  print("cos_theta = ", cos_theta)
  
  theta = np.arccos(cos_theta)
  print("theta = ", theta)
  
  
  perm_mat = np.round(diff_mat)
  print("permutation mat : ", perm_mat)
  
  rot2_ = np.dot(perm_mat.T, rot2)
  print(rot2_)
  
  diff_mat_ = np.dot(rot1, rot2_)
  print("different mat perm : ", diff_mat_)
  
  cos_theta_ =  (np.trace(diff_mat_)-1)/2
  print("perm cos_theta = ", cos_theta_)
  
  theta_ = np.arccos(cos_theta_)
  print("perm theta = ", theta_)
  
  if theta>kwargs["max_theta"]:
    if theta_<kwargs["max_theta"]:
      print("potential match with permutations")
      # TODO: probably expand on this case set?
  
  return theta<kwargs["max_theta"]
  
  
def checkOrigin(axes1, axes2, **kwargs):
  dkwargs = {"precision" : 0.1 }
  kwargs = {**dkwargs, **kwargs}
  
  orig1 = axes1["affine"][0:3,3]
  norm1 = np.sqrt(np.sum(orig1*orig1))
  print(orig1)
  
  orig2 = axes1["affine"][0:3,3]
  norm2 = np.sqrt(np.sum(orig2*orig2))
  print(orig2)
  
  thresh = np.max([norm1, norm2]) * kwargs["precision"]
  print(thresh)
  
  diff = orig1-orig2
  norm_d = np.sqrt(np.sum(diff*diff))
  print(norm_d)
  
  return norm_d < thresh
  
  
def compareAxes(axes1, axes2, **kwargs):
  
  print(axes1["axis_space"], axes2["axis_space"])

  space_check = axes1["axis_space"] == axes2["axis_space"]
  
  rot_check = checkRotations(axes1, axes2, **kwargs)
  
  origin_check = checkOrigin(axes1, axes2, **kwargs)
  
  return space_check and rot_check and origin_check
  

def getAxes(filename, **kwargs):
  dkwargs = {"verbose" : False }
  kwargs = {**dkwargs, **kwargs}
  
  o_fname = os.path.realpath(filename)

  (data_path, name) = os.path.split(o_fname)

  #  outputpath = os.path.join(data_path, "transformed")
  #  outname =name[:-7]+"_transformed"
  #  out_fname = os.path.join(outputpath, outname+".nrrd")

  froot, ext = os.path.splitext(o_fname)
  if ext == ".gz":
    froot_, ext_ = os.path.splitext(froot)
    if ext_ == ".nii":
      froot = froot_
      ext = ext_ + ext
  if ext == ".nii.gz":
    axes = getNiftiAxes(o_fname, **kwargs)
  elif ext == ".nrrd":
    axes = getNrrdAxes(o_fname, **kwargs)
  else:
    raise ValueError("file type not regonized : "+o_fname)
  
  return axes

def compareAllAxes(filenames, **kwargs):

  first_axes = {}
  all_axes = []
  matching = []
  
  print(filenames)
  
  for fname in filenames:
    print(fname)
    axes = getAxes(fname, **kwargs)
    
    all_axes.append(axes.copy())
    if not first_axes:
      first_axes = axes.copy()
      first_filename = fname
      matching.append(True)
      continue
      
    axes_compare = compareAxes(first_axes, axes)
    matching.append(axes_compare)
    
    if not axes_compare:
      print(fname, " axes do not match ", first_filename)
  
  print(matching)
  if np.all(matching):
    print("all readable files appear to match axes")
      
  return matching
  


def main():
  parser = build_parser()
  args = parser.parse_args()

  if len(args.filenames)==1:
    axes = getAxes(args.filenames[0], verbose = True)
    return axes
  else:
    checkall = compareAllAxes(args.filenames)
    return checkall
    
  return

  


if __name__ == "__main__":
  main()



