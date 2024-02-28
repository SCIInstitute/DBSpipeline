"""
convert gmsh files to matlab for scirun

"""

import meshio
import scipy.io
import sys

pathname = "./"

filename = pathname + sys.argv[1]

#outname = pathname + sys.argv[1].split('.')[0] + '_mesh'
outname = pathname + 'headmesh'
mesh = meshio.read(filename)

#points = mesh.points
#tris = mesh.cells[0].data
#tets = mesh.cells[1].data
#
#tri_data = mesh.cell_data["gmsh:physical"][0]
#tet_data = mesh.cell_data["gmsh:physical"][1]

trisurf = {"node" : mesh.points,
            "face" : mesh.cells[0].data,
            "field" : mesh.cell_data["gmsh:physical"][0]
}

tetvol = {"node" : mesh.points,
            "cell" : mesh.cells[1].data,
            "field" : mesh.cell_data["gmsh:physical"][1]
}

scipy.io.savemat(outname+"_trisurf.mat", {"trisurf" : trisurf} )
scipy.io.savemat(outname+"_tetvol.mat", {"tetvol" : tetvol} )

