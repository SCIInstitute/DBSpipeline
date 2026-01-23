import os
import sys

import numpy as np



axisObjectTemplate = {
        "axis_space" : None,
        "affine" : np.identity(4),
        "source": None,
        "header" : None
}

# space dims of 3 only.
# The assumption is that RAS is the base system,
#   and is therefore the same as scanner-xyz
nrrdSpaceCodes = {
    "RAS" : ["right-anterior-superior",  "RAS"],
    "LAS" : ["left-anterior-superior", "LAS"],
    "LPS" : ["left-posterior-superior", "LPS"],
    "RAS" : ["scanner-xyz"],
    "RAS"  : ["3D-right-handed"],
    "LAS"  : ["3D-left-handed"]
#    "XYZ" : ["scanner-xyz"],
#    "RH"  : ["3D-right-handed"],
#    "LH"  : ["3D-left-handed"]
}



#compared to RAS = XYZ = RH
#codeAxes = {
#    "RAS" : np.eye(3),
#    "LAS" : np.array([[-1, 0, 0], [ 0, 1, 0], [0, 0, 1]]),
#    "LPS" : np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]]),
#    "LIA" : np.array([[-1, 0, 0], [0, 0, 1], [0, -1, 0]]),
#    "ALS" : np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
#    "PRS" : np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]),
#    "RIP" : np.array([[1, 0, 0], [0, 0, -1], [0, -1, 0]]),
#    "XYZ" : np.eye(3),
#    "RH"  : np.eye(3),
#    "LH"  : np.array([[-1, 0, 0], [ 0, 1, 0], [0, 0, 1]])
#}

codeAxes = {
    "R" : np.array([1,0,0]),
    "A" : np.array([0,1,0]),
    "S" : np.array([0,0,1]),
    "L" : np.array([-1,0,0]),
    "P" : np.array([0,-1,0]),
    "I" : np.array([0,0,-1])
}

axisLookupTable = [["R", "A", "S"], ["L", "P", "I"]] 




# do I need to make these exhaustive?
chiralityTable = {
    "right" : ["RH", "LPS", "RAS", "XYZ", "PIR" ],
    "left"  : [ "LH", "LAS", "RPS", "LIA"]
}

