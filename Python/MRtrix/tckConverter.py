#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert MRTRIX3 tck file to SCIRun Pts/Edges

@author: Jackson Cagle, 2022
"""

import argparse
from nibabel import streamlines
import numpy as np

def convertPtsEdges(filename):
    extractedTckFile = streamlines.load(filename)

    pts = np.zeros((extractedTckFile.streamlines.total_nb_rows, 3))
    edges = np.zeros((extractedTckFile.streamlines.total_nb_rows - len(extractedTckFile.streamlines),2), dtype=int)

    currentPts = 0
    currentEdges = 0
    for track in extractedTckFile.streamlines:
        trackNodes = track.copy()
        pts[currentPts:currentPts+trackNodes.shape[0],:] = trackNodes * [-1,-1,1]
        edges[currentEdges:currentEdges+trackNodes.shape[0]-1,0] = np.arange(currentPts,currentPts+trackNodes.shape[0]-1, dtype=int)
        edges[currentEdges:currentEdges+trackNodes.shape[0]-1,1] = np.arange(currentPts+1,currentPts+trackNodes.shape[0], dtype=int)

        currentPts += trackNodes.shape[0]
        currentEdges += trackNodes.shape[0]-1

    return pts, edges

parser = argparse.ArgumentParser(description='Convert MRTRIX3 tck file to SCIRun Pts/Edges')
parser.add_argument('input_tck', help='The input .tck File')
parser.add_argument('output_path', help='The output path (without extension). Two files will be generated')

if __name__ == "__main__":
    args = parser.parse_args()
    pts, edges = convertPtsEdges(args.input_tck)
    np.savetxt(args.output_path + ".edge", edges, fmt="%d", delimiter=" ")
    np.savetxt(args.output_path + ".pts", pts, fmt="%.8f", delimiter=" ")
