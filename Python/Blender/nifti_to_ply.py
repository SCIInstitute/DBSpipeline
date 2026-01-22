# Convert Nifti file into a series of PLY slice models for blender, outputs three files: axial, sagittal, and coronal
# Usage: python nifti_to_ply.py --img WMn_ACPCspace.nii.gz --spacing 5 (optional input)

import pyvista as pv
import argparse
import numpy as np
import nibabel as nib
import scipy.linalg
import math

def scalar_to_gray(slice_mesh):
    # Scale data to 0-255 and creates grayscale RGB array
    scalars = slice_mesh.get_array('NIFTI')
    scaled = np.interp(scalars, (scalars.min(),scalars.max()),(0,255))
    grayscale = np.column_stack((scaled,scaled,scaled))
    return grayscale.astype(np.uint8)

def mesh_slicer_norm(mesh, axis, spacing=5): # Not in use, meant to slice along axes of object, but currently just slicing along absolute XYZ. Also does not work currently
    dim = mesh.GetDimensions()
    dim_xyz = {'x':dim[0],'y':dim[1],'z':dim[2]}
    vec_xyz = {'x':[1,0,0],'y':[0,1,0],'z':[0,0,1]}

    vec = np.array(vec_xyz[axis])
    norm_vec = vec / np.linalg.norm(vec)
    a = mesh.center + norm_vec * mesh.length / 3
    b = mesh.center - norm_vec * mesh.length / 3

    n_slices = math.floor(dim_xyz[axis]/float(spacing))
    line = pv.Line(a,b,n_slices)
    slices = pv.MultiBlock()
    for point in line.points:
        slices.append(mesh.slice(normal=norm_vec,origin=point))
    slices_merged = slices.combine()
    return slices_merged

parser = argparse.ArgumentParser(
    prog='Nifti to PLY',
    description='Convert Nifti image to PLY object slices'
)
parser.add_argument("--img", required=True, help="Path to file",dest="nifti")
parser.add_argument("--spacing", required=False, help="Slice Spacing (in mm), default 5mm",dest="spacing",default=5)
args = parser.parse_args()

print('Slice spacing (mm):',args.spacing)

#Image Transform Data
img = nib.load(args.nifti)
affine = img.affine

translate = np.eye(4)
translate[:3,3] = affine[:3,3]

affine[:3,3] = 0
transform, scale = scipy.linalg.polar(affine) #decompose rotation and scale, scale is not needed for model
transform[:3,3] = translate[:3,3]
print('Image Orientation:')
print(transform)

# Load mesh data
reader = pv.get_reader(args.nifti)
mesh = reader.read()
dim = mesh.GetDimensions()
dim_xyz = {'x':dim[0],'y':dim[1],'z':dim[2]}
plane_xyz = {'x':'sagittal','y':'coronal','z':'axial'}

flipXY = np.eye(4)
flipXY[0,0] = flipXY[0,0] * -1 #flip XY signs
flipXY[1,1] = flipXY[1,1] * -1
print('Flipping XY signs:')
print(flipXY)

for key, value in dim_xyz.items():
    mesh_transformed = mesh.transform(transform,inplace=False)
    mesh_flipped = mesh_transformed.transform(flipXY,inplace=False)
    slices = mesh_flipped.slice_along_axis(n=math.floor(value/float(args.spacing)), axis=key) #spits out a list of PolyData, number of slices determined by spacing and dimension
    slices_merged = slices.combine()
    slices_surface = slices_merged.extract_surface() #needed to save to PLY, no change to mesh or data, just format
    texture = scalar_to_gray(slices_surface)
    print('Saving:',plane_xyz[key])
    slices_surface.save('slices_'+plane_xyz[key]+'.ply',texture=texture)
