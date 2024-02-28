# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 10:35:45 2023

@author: Matthew
"""

import numpy as np
from scipy.spatial.transform import Rotation as R

sci_quat = R.from_quat([float(x) for x in input("SCIRun Quaternion: ").split(',')])
ax_rot = R.from_euler(input("Axis of Roation: "), float(input("Angle (Deg): ")), degrees=True)

sci_rotated = ax_rot.apply(sci_quat.as_matrix())
sci_quat_rotated = R.from_matrix(sci_rotated)
sci_array = np.asarray(sci_quat_rotated.as_quat())
print(sci_array.tolist())