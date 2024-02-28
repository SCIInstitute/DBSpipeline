# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:07:27 2023

@author: Matthew
"""

models=slicer.util.getNodes('*ModelDisplayNode*')
[models[mod].Visibility2DOff() for mod in models.keys()]