import sys, getopt

import numpy as np
import pyvista
import bpy

"""
to run in blender console:
import sys
sys.path.append(r'D:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\Blender')
import loadStreamLinesVTK

loadStreamLinesVTK.main([vtk_file, data_field_name])

"""


vtk_file = r'D:\Dropbox (UFL)\Projects\NeuroPaceUH3\NeuroPaceLGS_Data_Analysis\Emory\S303-001\Snippets\Rendering\Data\CL_left_data.vtk'
data_field = "curv"

colors= [ [0.044, 0.072, 0.527], [0.456, 0.001, 0.019] ]


def vtk2BlenderCurves(infile, field_name):

  reader = pyvista.get_reader(infile)
  polydata = reader.read()

  n_streamlines = polydata.n_cells

  obj_name_root = "Fibers"
  obj_name0 = obj_name_root+"_0"
  obj_name1 = obj_name_root+"_1"

  c_name_root = "Streamlines"
  cname_0 = c_name_root+"_0"
  cname_1 = c_name_root+"_1"

  pt_data = polydata.point_data[field_name]

  curve_0 = bpy.data.curves.new(name=cname_0, type='CURVE')
  curve_1 = bpy.data.curves.new(name=cname_1, type='CURVE')
  curve_0.dimensions = '3D'
  curve_1.dimensions = '3D'

  for k in range(n_streamlines):
    cell = polydata.get_cell(k)
    cell_points = cell.points
    n_cpts = cell.n_points
    p_id =  cell.point_ids
    vals = pt_data[p_id]
    med = np.median(vals)
    
    if med<0.5:
        spline = curve_0.splines.new('NURBS')
    else:
        spline = curve_1.splines.new('NURBS')
    spline.points.add(n_cpts - 1)
    for l, pt in enumerate(cell_points):
        spline.points[l].co = np.append(pt,1)
        
        
  obj0 = bpy.data.objects.new(obj_name0, curve_0)
  obj1 = bpy.data.objects.new(obj_name1, curve_1)

  bpy.context.collection.objects.link( obj0 )
  bpy.context.collection.objects.link( obj1 )

  return

def main(argv):

  infile = vtk_file
  field_name = data_field
  
  opts, args = getopt.getopt(argv,"hi:o:",["ifile=","field="])
  for opt, arg in opts:
    if opt == "-h":
      print ("loadStreamLinesVTK.py -i <inputfile> -f <field_name>")
      sys.exit()
    elif opt in ("-i", "--ifile"):
      infile = arg
    elif opt in ("-f", "--field"):
      field_name = arg
  
  vtk2BlenderCurves(infile, field_name)
  


if __name__ == "__main__":
   main(sys.argv[1:])
