# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:45:00 2023

@author: Matthew
"""
import sys

def ViewSceneGet():
    mods = scirun_module_ids()

    for module in mods:
        if 'ViewScene' in module:
            view = module
            break
    
    item_lst = [field for field in scirun_dump_module_state(view).split('\n') if field.startswith('[Vis')] #Find the ViewScene list of objects

    item_lst = item_lst[0].split('[graphicsItem, ')[1:]
    vis_lst = scirun_get_module_state(view, 'VisibleItemListState')
    return {'view':view, 'names':item_lst, 'states':vis_lst}
    