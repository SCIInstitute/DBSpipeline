# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:11:15 2023

@author: Matthew
"""

mods=slicer.util.getNodes('*SliceNode*')
mods['Red'].SetOrientationToAxial()
mods['Green'].SetOrientationToCoronal()
mods['Yellow'].SetOrientationToSagittal()