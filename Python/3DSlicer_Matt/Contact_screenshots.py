# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:36:06 2023

@author: Matthew
"""
import ScreenCapture
cap = ScreenCapture.ScreenCaptureLogic()

contacts = getNodes('*MarkupsFiducialNode*') #get different scene nodes
crosshair = getNode('*CrosshairNode*')
atlas = getNodes('*SegmentationNode*')
view_ax = cap.viewFromNode(getNode('*SliceNodeRed*'))
view_cor = cap.viewFromNode(getNode('*SliceNodeGreen*'))
view_sag = cap.viewFromNode(getNode('*SliceNodeYellow*'))

for side in atlas.keys(): #split everything into left and right, trying to not rely on naming (except for THOMAS atlas)
    if 'left' in side.lower():
        left_atlas = atlas[side]
    if 'right' in side.lower():
        right_atlas = atlas[side]

for markup in contacts.keys():
    sign_test = contacts[markup].GetNthControlPointPosition(0)[0]
    if sign_test < 0:
        left_contacts = contacts[markup]
        left_contacts.SetDisplayVisibility(0)
    if sign_test >= 0:
        right_contacts = contacts[markup]
        right_contacts.SetDisplayVisibility(0)
        
        
# Left side
for contact in range(0,4):
    contact_name = left_contacts.GetNthControlPointLabel(contact) #set up locations
    coords = left_contacts.GetNthControlPointPosition(contact)
    slicer.modules.markups.logic().JumpSlicesToLocation(coords[0],coords[1],coords[2], True)
    crosshair.SetCrosshairRAS(coords)
    
    left_atlas.SetDisplayVisibility(0)
    cap.captureImageFromView(view_ax, r'Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\3D Slicer\Captures\Left_ax_'+contact_name+'.png')
    cap.captureImageFromView(view_sag, r'Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\3D Slicer\Captures\Left_sag_'+contact_name+'.png')
    cap.captureImageFromView(view_cor, r'Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\3D Slicer\Captures\Left_cor_'+contact_name+'.png')
    
    left_atlas.SetDisplayVisibility(1)
    cap.captureImageFromView(view_ax, r'Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\3D Slicer\Captures\Left_ax_thal_'+contact_name+'.png')
    cap.captureImageFromView(view_sag, r'Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\3D Slicer\Captures\Left_sag_thal_'+contact_name+'.png')
    cap.captureImageFromView(view_cor, r'Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\3D Slicer\Captures\Left_cor_thal_'+contact_name+'.png')
left_atlas.SetDisplayVisibility(0)

# Right Side
for contact in range(0,4):
    contact_name = right_contacts.GetNthControlPointLabel(contact) #set up locations
    coords = right_contacts.GetNthControlPointPosition(contact)
    slicer.modules.markups.logic().JumpSlicesToLocation(coords[0],coords[1],coords[2], True)
    crosshair.SetCrosshairRAS(coords)
    
    right_atlas.SetDisplayVisibility(0)
    cap.captureImageFromView(view_ax, r'Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\3D Slicer\Captures\Right_ax_'+contact_name+'.png')
    cap.captureImageFromView(view_sag, r'Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\3D Slicer\Captures\Right_sag_'+contact_name+'.png')
    cap.captureImageFromView(view_cor, r'Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\3D Slicer\Captures\Right_cor_'+contact_name+'.png')
    
    right_atlas.SetDisplayVisibility(1)
    cap.captureImageFromView(view_ax, r'Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\3D Slicer\Captures\Right_ax_thal_'+contact_name+'.png')
    cap.captureImageFromView(view_sag, r'Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\3D Slicer\Captures\Right_sag_thal_'+contact_name+'.png')
    cap.captureImageFromView(view_cor, r'Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\3D Slicer\Captures\Right_cor_thal_'+contact_name+'.png')
right_atlas.SetDisplayVisibility(0)