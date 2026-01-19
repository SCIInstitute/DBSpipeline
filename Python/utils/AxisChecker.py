import os
import sys
import argparse
import copy

import nrrd
import numpy as np
import nibabel as nib

from AxisCheckerDefaults import axisObjectTemplate, nrrdSpaceCodes, chiralityTable, codeAxes, axisLookupTable


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
  
def checkAxesInput(passed_args):

  if not passed_args["axisObject"]:
    axisObject = copy.deepcopy(axisObjectTemplate)
  elif type(passed_args["axisObject"]) is dict:
    axisObject = passed_args["axisObject"] # reference
  else:
    print("keyword arg 'axisObject' is expected to be a dict")
    axisObject = copy.deepcopy(axisObjectTemplate)
    
  return axisObject
  
  
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
  
  dkwargs = {"verbose" : False, "axisObject" : None }
  kwargs  = {**dkwargs, **kwargs}
  
  axisObject = checkAxesInput(kwargs)
    
  imgdata, header = nrrd.read(filename)
  
  dim = nrrdDimCheck(header)
  
  if not dim == 3:
    raise ValueError("This tools currently only works with 3D data")
    
  
#  print(header["space"])
#  print(nrrdSpaceCodes.items())
  
  axis_space = next(key for key, v_list in nrrdSpaceCodes.items() if  header["space"] in v_list )
#  print(axis_space)

  axisObject["axis_space"] = axis_space
  axisObject["affine"][:3,:3] = header["space directions"].T
  axisObject["affine"][:3,3] = header["space origin"]
  
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
  
  dkwargs = {"verbose" : False, "axisObject" : None }
  kwargs  = {**dkwargs, **kwargs}
  
  axisObject = checkAxesInput(kwargs)
  
  img = nib.load(filename)
#  
#  axisObject["affine"] = img.affine
#  axis_space = "".join(nib.aff2axcodes(img.affine))
##  print(axis_space)
#  axisObject["axis_space"] = axis_space
#  axisObject["source"] = "nifti"
#  
#  axisObject["header"] = img.header
#  

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
  
def checkChiral(rot_mat, **kwargs):
# assumes normalized matrix

  precision_check = 0.1
  
  chir = None
  ax0 = rot_mat[:,0]
  ax1 = rot_mat[:,1]
  ax2 = rot_mat[:,2]
  
#  print("checking chirality of matrix = ")
#  print(rot_mat)
#  print("ax0 = ", ax0)
#  print("ax1 = ", ax1)
#  print("ax2 = ", ax2)
  
  ax2_check = np.cross(ax0, ax1)
  ax_check = np.dot(ax2, ax2_check)
  
#  print("ax2 check = ", ax2_check)
#  print("dot check = ", ax_check)
  
  if np.abs(np.abs(ax_check)-1) > precision_check:
    print("matrix might not be orthogonal")
    return
  
  if ax_check>0:
    chir = "right"
  else:
    chir = "left"
    
  return chir
  

def checkRotationAngle(rot1, rot2, **keargs):
# assumes normalized matrix
#  print(rot1)
#  print(rot2)

  diff_mat = np.dot(rot1, rot2.T)
#  print("different mat : ", diff_mat)
  
  cos_theta =  (np.trace(diff_mat)-1)/2
#  print("cos_theta = ", cos_theta)
  
  cos_theta_safe = np.max((np.min((cos_theta,1.0)), -1.0))
  
  theta = np.arccos(cos_theta_safe)
#  print("theta = ", theta)
  
  return theta, diff_mat
  
def matrix2Code(rot_mat, **kwargs):
# assumes a basis of RAS
  
  ind_arr = np.empty(3)
  neg_arr = np.zeros(3)
  for k in range(3):
    ax = rot_mat[:,k]
    mx_val = np.dot(ax, np.eye(3))
#    print(mx_val)
    ind = np.argmax(np.abs(mx_val))
    ind_arr[k] = ind
    if mx_val[ind]<0:
      neg_arr[k] = 1
      
  code_arr = [ axisLookupTable[ng][id] for id, ng in zip(ind_arr.astype(int), neg_arr.astype(int))]
  
#  print(code_arr)
      
 
  return "".join(code_arr)
  
def normalizeRotation(rot_mat, **kwargs):
  norm = np.sqrt(np.sum(rot_mat*rot_mat, axis = 0))
  rot = rot_mat/norm
  
  return rot

  
def checkRotations(axes1, axes2, **kwargs):
  dkwargs = {"max_theta" : np.pi/6 }
  kwargs = {**dkwargs, **kwargs}
  
  chir1 = next(key for key, v_list in chiralityTable.items() if  axes1["axis_space"] in v_list )
  chir2 = next(key for key, v_list in chiralityTable.items() if  axes2["axis_space"] in v_list )
  
  print(chir1, chir2)

  
  rot1 = normalizeRotation(axes1["affine"][:3,:3])
  
#  print("check axis 1")
#  print(axes1["affine"][:3,:3])
#  print(rot1)
  mat_code1 = matrix2Code(rot1)
#  print("estimated axes : ", mat_code1)

  rot2 = normalizeRotation(axes2["affine"][:3,:3])

#  print("check axis 2")
#  print(axes2["affine"][:3,:3])
#  print(rot2)
  mat_code2 = matrix2Code(rot2)
#  print("estimated axes : ", mat_code2)

  mat_chir1 = checkChiral(rot1)
  mat_chir2 = checkChiral(rot2)
  print("matrix chirality : ", mat_chir1, mat_chir2)
  
  if not mat_chir1 == mat_chir2:
    print("axes are not the same chirality")
    
  
  theta, diff_mat = checkRotationAngle(rot1, rot2)
  
#  print("different mat : ", diff_mat)
#  print("theta = ", theta)
  
#  rot2_check = np.dot(diff_mat, rot2)
#  
#  theta_check, diff_mat_check = checkRotationAngle(rot1, rot2_check)
  
#  print("different mat check: ", diff_mat_check)
#  print("theta check = ", theta_check)



  perm = False

  ax_mat1 = np.array([ codeAxes[ax] for ax in axes1["axis_space"]]).T
#  print(ax_mat1)
  ax_mat2 = np.array([ codeAxes[ax] for ax in axes2["axis_space"]]).T
#  print(ax_mat2)


# This checks if the Axis label is not RAS and if it matches the axes as if RAS were the basis.  This will check some of the ways that SCIRun may interpret the differently from other software.  Specifically, it checks to see if the axis code is the basis of the transform or a descriptor of the transform.  We check for differences with an RAS basis and can make suggestions if there is misalignment.

# There are other interpretations happening, and may need to be addressed.  

  if chir1 == mat_chir1 or chir1 == "RAS":
    rot1_ = rot1
  else:
    print("permuted matrix 1 = ")
    rot1_ = np.dot(ax_mat1,rot1)
    print(rot1_)
    perm = True
  
#  perm_mat = np.dot(ax_mat1, ax_mat2.T)
#  print(perm_mat)

  if chir2 == mat_chir2 or chir2 == "RAS":
    rot2_ = rot2
  else:
    print("permuted matrix 2 = ")
    rot2_ = np.dot(ax_mat2,rot2)
    print(rot2_)
    perm = True

  
  if perm:
    
    print("perm mat 1 = ")
    print(rot1_)
    mat_code1_ = matrix2Code(rot1_)
    print("estimated axes : ", mat_code1_)

    print("perm mat 2 = ")
    print(rot2_)
    mat_code2_ = matrix2Code(rot2_)
    print("estimated axes : ", mat_code2_)
    
    if not mat_code1_ == mat_code2_:
      print("trying another correction")
      ax_mat1_ = np.array([ codeAxes[ax] for ax in mat_code1]).T
      perm_mat1 = np.dot(ax_mat1, ax_mat1_.T)
      rot1_ = np.dot(perm_mat1, rot1)
      
      print(ax_mat1_)
      print(perm_mat1)
      print("perm mat 1 = ")
      print(rot1_)
      mat_code1_ = matrix2Code(rot1_)
      print("estimated axes : ", mat_code1_)
    
      ax_mat2_ = np.array([ codeAxes[ax] for ax in mat_code2]).T
      perm_mat2 = np.dot(ax_mat2, ax_mat2_.T)
      rot2_ = np.dot(perm_mat2, rot2)
      
      
      print(ax_mat2_)
      print(perm_mat2)
      print("perm mat 2 = ")
      print(rot2_)
      mat_code2_ = matrix2Code(rot2_)
      print("estimated axes : ", mat_code2_)
      
      
      
      
      
      
    
    theta_, diff_mat_ = checkRotationAngle(rot1_, rot2_)
    print("different mat perm : ", diff_mat_)
    print("perm theta = ", theta_)
    
    
#    rot2_check_ = np.dot(diff_mat_, rot2_)
#    
#    print("mat 2 perm check= ")
#    print(rot2_check_)
#    
#    theta_check_, diff_mat_check_ = checkRotationAngle(rot1_, rot2_check_)
#    
#    print("different mat perm check: ", diff_mat_check_)
#    print("perm theta check = ", theta_check_)
    
    if theta>kwargs["max_theta"]:
      if theta_<kwargs["max_theta"]:
        print("--- potential match with different axis interpretations ---")
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
#    print("axes : ", axes)
    
    all_axes.append(axes.copy())
    if not first_axes:
      first_axes = axes.copy()
      first_filename = fname
      matching.append(True)
#      print("first file")
      continue
    
#    print("Reference axes : ", first_axes)
#    print("axes : ", axes)
    
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

  print("number of files : ", len(args.filenames))
  if len(args.filenames)==1:
    print("running one")
    axes = getAxes(args.filenames[0], verbose = True)
    return axes
  else:
    print("running compareall")
    checkall = compareAllAxes(args.filenames)
    return checkall
    
  return

  


if __name__ == "__main__":
  main()



