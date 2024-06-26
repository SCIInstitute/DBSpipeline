"""
convert gmsh files to matlab for scirun

"""

from ../utils/meshfiles import gmsh2Mat

pathname = "./"

filename = pathname + sys.argv[1]

gmsh2Mat(filename)
