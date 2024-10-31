"""
convert gmsh files to matlab for scirun

"""
import sys
sys.path.append(r'/blue/butsonc/Github/DBSpipeline/Python/utils')
# print(sys.path)
from meshfiles import gmsh2Mat

pathname = "./"

filename = pathname + sys.argv[1]

gmsh2Mat(filename)