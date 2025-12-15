import os
import sys

import numpy as np



axisObjectTemplate = {
        "axis_space" : None,
        "affine" : np.identity(4),
        "source": None,
        "header" : None
}

# space dims of 3 only
nrrdSpaceCodes = {
    "RAS" : ["right-anterior-superior",  "RAS"],
    "LAS" : ["left-anterior-superior", "LAS"],
    "LPS" : ["left-posterior-superior", "LPS"],
    "XYZ" : ["scanner-xyz"],
    "RH"  : ["3D-right-handed"],
    "LH"  : ["3D-left-handed"]
}

# do I need to make these exhaustive?
chiralityTable = {
    "right" : ["RH", "LPS", "RAS", "XYZ" ],
    "left"  : [ "LH", "LAS", "RPS", "LIA"]
}

