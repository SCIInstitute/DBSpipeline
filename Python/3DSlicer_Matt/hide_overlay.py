# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:28:28 2023

@author: Matthew
"""

segmentationNode = getNodes('*SegmentationNode*')
[segmentationNode[seg].SetDisplayVisibility(False) for seg in segmentationNode.keys()]

maps = getNodes('*LabelMapVolumeNode*')
[maps[map].GetDisplayNode().SetVisibility(False) for map in maps.keys()]