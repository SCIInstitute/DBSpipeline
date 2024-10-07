## edge_finder

# Counts the ends of all streamlines. Outputs an array of end-fiber locations and an array of edge tangents

import numpy as np
import argparse
import os
from scipy.io import savemat

# Insert your Python code here. The SCIRun API package is automatically imported.

# field = fieldInput1
# m = np.array(field['edge'])
def edge_calc(edge_data,node_data,node_depth):
    m = edge_data
    # print(m[0])
    m0 = m[1:,0]
    m0 = np.append(m0,0)
    m1 = m[:,1]

    EndCount = np.where(np.not_equal(m0,m1))[0] #Mismatch Indicates end of fiber
    EndCount = np.insert(EndCount,0,0,axis=0)
    indexer = np.arange(len(EndCount))
    EndCount = np.add(EndCount,indexer)
    #EndCount[-1] = EndCount[-1] + 1

    matrixOutput1 = EndCount.tolist()

    # edges = m - 1
    edges = m.copy()
    nodes = node_data
    print(np.min(edges))
    print(np.max(edges))

    edge_tangs = np.zeros((edges.shape[0],3))

    for ind, edge in enumerate(edges):
    #     print(nodes[edge[1],:] - nodes[edge[0],:])
        edge_tangs[ind, :] = nodes[edge[1],:] - nodes[edge[0],:]

    # new_field = {"edge" : edges.tolist(),  "node" : nodes.tolist(),  "field" : edge_tangs.tolist() }

    # fieldOutput1 = new_field

    fieldMask = np.zeros(EndCount[-1]+1)
    print('End Data Removal:',node_depth)
    n = node_depth
    Ends_end = EndCount[1:] #Removes the 0 at the beginning
    Ends_start = EndCount[:-1] #Removes the last value
    for i in range(-n+1,n+1):
        if i < 0:
            fieldMask[Ends_end + i] = 1
        if i == 0:
            fieldMask[EndCount] = 1
        if i > 0:
            fieldMask[Ends_start + i] = 1


    return fieldMask, edge_tangs

parser = argparse.ArgumentParser(description='Find edges and edge tangents of tracts')
parser.add_argument('edge', help='input edge file')
parser.add_argument('pts', help='input pts file')
parser.add_argument('end_depth',help='number of nodes to set to zero at the ends of fibers')

if __name__ == "__main__":
    args = parser.parse_args()
    edge = np.loadtxt(args.edge,dtype=int)
    pts = np.loadtxt(args.pts)
    depth = int(args.end_depth)
    ends, edge_tangent = edge_calc(edge,pts,depth)
    out_path = os.path.dirname(args.edge)
    # np.savetxt(os.path.join(out_path,"EndCount.txt"),ends,fmt="%d", delimiter=" ")
    # np.savetxt(os.path.join(out_path, "EdgeTangents.txt"),edge_tangent,fmt="%.8f", delimiter=" ")
    # savemat(os.path.join(out_path,"EndCount.mat"),{"Ends":ends},do_compression=True)
    # savemat(os.path.join(out_path,"EdgeTangents.mat"),{"Tangents":edge_tangent},do_compression=True)
    savemat(os.path.join(out_path,"Edge_data.mat"),{"Tangents":edge_tangent,"Ends":ends},do_compression=True)