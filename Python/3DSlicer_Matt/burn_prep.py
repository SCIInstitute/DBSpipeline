# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 09:37:52 2023

@author: Matthew
"""

#For setting up burned images

#Load Imaging and models to burn in first
#To Run: exec(open(r'D://Dropbox (UFL)//DataProcessing//Pipeline Code//Python//3D Slicer//burn_prep.py').read())

#Convert models to segmentations
modelNode = getNodes('*ModelNode*')
[slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modelNode[model],slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSegmentationNode',modelNode[model].GetName())) for model in modelNode.keys() if 'Slice' not in modelNode[model].GetName()]

visibleSegmentIds = vtk.vtkStringArray()
sourceVolumeNode = slicer.vtkMRMLScalarVolumeNode()
slicer.mrmlScene.AddNode(sourceVolumeNode)

#Convert segmentations to label maps (no direct path from model to label map)
segmentationNode = getNodes('*SegmentationNode*')
[slicer.vtkSlicerSegmentationsModuleLogic.ExportSegmentsToLabelmapNode(segmentationNode[seg], visibleSegmentIds, slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode', segmentationNode[seg].GetName()), sourceVolumeNode) for seg in segmentationNode.keys()]
slicer.mrmlScene.RemoveNode(getNode('Volume'))

#Find max and mean intensity values and set those as label map values
T1 = getNode('*ScalarVolumeNode*')
T1_array = arrayFromVolume(T1)
array_max = T1_array.max() #round(T1_array.max() / 1.5)
array_mean = round(T1_array.max() / 4)
maps = getNodes('*LabelMapVolumeNode*')
[updateVolumeFromArray(maps[map], arrayFromVolume(maps[map])*array_max) if 'shaft' not in maps[map].GetName().lower() else updateVolumeFromArray(maps[map], arrayFromVolume(maps[map])*array_mean) for map in maps.keys()]
