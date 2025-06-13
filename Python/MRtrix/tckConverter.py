#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert MRTRIX3 tck file to SCIRun Pts/Edges

@author: Jackson Cagle, 2022
"""

import argparse
from nibabel import streamlines
import numpy as np
import scipy.io

def convertPtsEdges(filename, tract_datafile=None):
    extractedTckFile = streamlines.load(filename)
    pts = np.zeros((extractedTckFile.streamlines.total_nb_rows, 3))
    edges = np.zeros((extractedTckFile.streamlines.total_nb_rows - len(extractedTckFile.streamlines),2), dtype=int)
    
    currentPts = 0
    currentEdges = 0

    if tract_datafile:
        try:
            original_data = np.loadtxt(tract_datafile, delimiter=",")
        except:
            original_data = [i for i in np.loadtxt(tract_datafile, delimiter=" ", dtype=str) if not i == ""]

        tract_data = np.zeros((extractedTckFile.streamlines.total_nb_rows))
        counter = 0

    for track in extractedTckFile.streamlines:
        trackNodes = track.copy()
        pts[currentPts:currentPts+trackNodes.shape[0],:] = trackNodes * [-1,-1,1]
        track_index[currentPts:currentPts+trackNodes.shape[0]] = k
        edges[currentEdges:currentEdges+trackNodes.shape[0]-1,0] = np.arange(currentPts,currentPts+trackNodes.shape[0]-1, dtype=int)
        edges[currentEdges:currentEdges+trackNodes.shape[0]-1,1] = np.arange(currentPts+1,currentPts+trackNodes.shape[0], dtype=int)

        if tract_datafile:
            tract_data[currentPts:currentPts+trackNodes.shape[0]] = original_data[counter]
#            tract_data[currentPts:currentPts+trackNodes.shape[0]] = counter
            counter += 1
        
        currentPts += trackNodes.shape[0]
        currentEdges += trackNodes.shape[0]-1

    if tract_datafile:
        return pts, edges, tract_data
    else:
        return pts, edges

parser = argparse.ArgumentParser(description='Convert MRTRIX3 tck file to SCIRun Pts/Edges')
parser.add_argument('input_tck', help='The input .tck File')
parser.add_argument('output_path', help='The output path (without extension). Two files will be generated')
parser.add_argument('--tract_data', help='The data to be written for each point.')

if __name__ == "__main__":
    args = parser.parse_args()
    if args.tract_data:
        pts, edges, tract_data = convertPtsEdges(args.input_tck, args.tract_data)
        wb = { "node" : pts.T,"edge" : edges.astype(dtype=np.uint32).T,"data" : tract_data}
        np.savetxt(args.output_path + ".edge", edges, fmt="%d", delimiter=" ")
        np.savetxt(args.output_path + ".pts", pts, fmt="%.8f", delimiter=" ")
        np.savetxt(args.output_path + ".tckdata", tract_data, fmt="%.8f", delimiter=" ")
        scipy.io.savemat(args.output_path + ".mat", {"scirunfield" : wb})
        
    else:
        pts, edges = convertPtsEdges(args.input_tck, args.tract_data)
        wb = { "node" : pts.T,"edge" : edges.astype(dtype=np.uint32).T}
        np.savetxt(args.output_path + ".edge", edges, fmt="%d", delimiter=" ")
        np.savetxt(args.output_path + ".pts", pts, fmt="%.8f", delimiter=" ")
        scipy.io.savemat(args.output_path + ".mat", {"scirunfield" : wb})
