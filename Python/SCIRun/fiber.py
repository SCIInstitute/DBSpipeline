# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:36:04 2023

@author: Matthew
"""
def ViewSceneGet():
    mods = scirun_module_ids()

    for module in mods:
        if 'ViewScene' in module:
            view = module
            break
    
    item_lst = [field for field in scirun_dump_module_state(view).split('\n') if field.startswith('[Vis')] #Find the ViewScene list of objects

    item_lst = item_lst[0].split('[graphicsItem, ')[1:] #Name cleaning
    vis_lst = scirun_get_module_state(view, 'VisibleItemListState')
    return {'view':view, 'names':item_lst, 'states':vis_lst}

ViewScene = ViewSceneGet()

fibers = [i for i, field in enumerate(ViewScene['names']) if 'iber' in field]

for fib in fibers:
    vis_lst[fib] = [True, True, False, False] #Turn on all fibers
    
scirun_set_module_state(ViewScene['view'], 'VisibleItemListState', vis_lst)
    
