# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:08:54 2023

@author: Matthew
"""

models=slicer.util.getNodes('*ModelDisplayNode*')
[models[mod].Visibility2DOn() for mod in models.keys()]