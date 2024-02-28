# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 09:30:43 2023

@author: Matthew
"""

thal_parts = {                     # Different parts of the thalamus.
'1': 'THALAMUS',        # The numbers correspond to the numbers
'2': 'AV',              # used in the THOMAS algorithm
'4': 'VA',
'5': 'VLA',
'6': 'VLP',
'7': 'VPL',
'8': 'PUL',
'9': 'LGN',
'10': 'MGN',
'11': 'CM',
'12': 'MDPF',
'13': 'HB',
'14': 'MTT',
'17': 'CL',
'18': 'VPM',
}

segmentations = slicer.util.getNodes('*SegmentationNode*')

for atlas in segmentations.keys():
    segments = segmentations[atlas]
    IDS = list(segments.GetSegmentation().GetSegmentIDs())
    for segID in IDS:
        nuc_name = thal_parts[segID]
        segment = segments.GetSegmentation().GetSegment(segID)
        segment.SetName(nuc_name)
    