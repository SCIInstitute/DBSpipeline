
#TODO
#only works when properly packaged
#from ..utils.meshfiles import vtk_to_TriSurfField

# currently copied from meshfiles
import sys,os

#import meshio
import scipy.io

import numpy as np



def vtk_converter(vtk_filename):
  vtk = open(vtk_filename,'r') #read the vtk file
  filename = vtk_filename.split('.')
  filename = filename[0] + '_' + filename[1]
  lines = vtk.readlines()
  vtk.close()
  pts_range = []
  fac_range = []
  data_range = []
  count = 0
  for line in lines: #separate the data
    if 'POINTS' in line:
      pts_range.append(count)
    if 'POLYGONS' in line:
      pts_range.append(count)
      fac_range.append(count)
    if 'POINT_DATA' in line:
      fac_range.append(count)
    if 'curv' in line:
      data_range.append(count)
    count += 1

  pts = lines[pts_range[0]+1:pts_range[1]]
  fac = lines[fac_range[0]+1:fac_range[1]]
  data = lines[data_range[0]+1:]

  #print(len(data))

  pts_file = open(filename+'.pts','w') #save data out to separate files
  pts_file.writelines(pts)
  pts_file.close()

  fac_file = open(filename+'_threes.fac','w')
  fac_file.writelines(fac)
  fac_file.close()
  faces = np.loadtxt(filename+'_threes.fac') #remove the 3's column
  faces_new = faces[:,1:]
  np.savetxt(filename+'.fac',faces_new, fmt='%d')

  data_file = open(filename+'_data.txt','w')
  data_file.writelines(data)
  data_file.close()
  
  return

def vtk_to_TriSurfField(subject):

  SUBJECTS_DIR=os.environ["SUBJECTS_DIR"]
  rel_path = "surf"
  vtk_files = ['lh.thresh.vtk', 'rh.thresh.vtk', 'lh.heatmap.vtk', 'rh.heatmap.vtk']

  for file in vtk_files:
    vtk_converter(os.path.join(SUBJECTS_DIR, subject, rel_path, file))

  return

def main(argv):
  subject = argv[1]
  vtk_to_TriSurfField(subject)
  
if __name__=="__main__":
  main(sys.argv)
