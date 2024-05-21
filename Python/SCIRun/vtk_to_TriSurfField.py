
#TODO
#only works when properly packaged
#from ..utils.meshfiles import vtk_to_TriSurfField
# here is the current workaround
import sys,os
sys.path.insert(1, os.path.realpath(os.path.pardir))
from utils.meshfiles import vtk_to_TriSurfField

subject = sys.argv[1]
vtk_to_TriSurfField(subject)
