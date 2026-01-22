# Convert Nifti files into nrrd. Can be used on scalar, vector, and tensor datatypes
# Currently scalar only works on 3D images, not 4D

import nibabel as nib
import numpy as np
import nrrd
import argparse

def nrrd_head_make(file):
      if 'tensor' in file:
            kind = ("space", "space", "space", '3D-symmetric-matrix')
            center = ("node", "node", "node", "node")
            dim = 4
      if 'vector' in file:
            kind = ("space", "space", "space", '3-vector')
            center = ("node", "node", "node", "node")
            dim = 4
      if 'scalar' in file:
            kind = ("domain", "domain", "domain")
            center = ("node", "node", "node")
            dim = 3
      header = {
      "dimension" : dim,
      "space dimensions" : 3,
      "space" : "3D-right-handed",
      "sizes": (1, 1, 1, 1),
      "space directions": ((0,0,0), (2,0,0), (0,2,0), (0,0,0)),
      "centerings": center,
      "kinds" : kind,
      "endian": "little",
      "encoding": "gzip",
      "space origin": (0,0,0),
      "measurement frame": ((1,0,0), (0,1,0), (0,0,1))
      }
      return header

parser = argparse.ArgumentParser(
    prog='Nifti to NRRD',
    description='Convert Nifti image to a NRRD'
)
parser.add_argument("--img", required=True, help="Path to file",dest="nifti")
parser.add_argument("--datatype", required=False, help="Type of image data. Options: tensor, vector, scalar. Default: scalar",dest="datatype",default='scalar')
args = parser.parse_args()
nifti = args.nifti
print('datatype:',args.datatype)

img = nib.load(nifti)  
data = img.get_fdata()
affine = img.affine

nrrd_header = nrrd_head_make(args.datatype)
if 'scalar' in args.datatype:
      nrrd_header["space directions"] = np.vstack(affine[:3,:3].T).tolist()
else:
      nrrd_header["space directions"] = np.vstack((affine[:3,:3].T, np.zeros(3))).tolist()
nrrd_header["sizes"] = data.shape
nrrd_header["space origin"] = affine[:3,3].tolist()

filename = nifti.replace('.nii.gz','.nrrd')
nrrd.write(filename,data,nrrd_header)