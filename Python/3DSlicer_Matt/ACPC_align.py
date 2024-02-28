# -*- coding: utf-8 -*-
"""
Created on Tue May  9 13:35:29 2023

@author: Matthew
"""
#Run after ACPC Module hardening the transform
ACPC = slicer.util.getNode('ACPC') #ACPC line markers
AC = ACPC.GetNthControlPointPositionVector(0) #Coords of AC and PC
PC = ACPC.GetNthControlPointPositionVector(1)

ACPC_move = [-(AC[0]+PC[0])/2,-(AC[1]+PC[1])/2,-(AC[2]+PC[2])/2] #Vector to move volume to origin

transformNode = slicer.vtkMRMLTransformNode()
slicer.mrmlScene.AddNode(transformNode)
mat = vtk.vtkMatrix4x4()
mat.SetElement(0,3,ACPC_move[0])
mat.SetElement(1,3,ACPC_move[1])
mat.SetElement(2,3,ACPC_move[2])
transformNode.SetMatrixTransformToParent(mat)
transformNode.SetName('ACPC_translation')