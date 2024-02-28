# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 09:11:07 2023

@author: Matthew
"""
import os

path = os.getcwd()

mods = scirun_module_ids()
for module in mods:
    if 'View' in module:
        translate = str(scirun_get_module_state(module, 'CameraLookAt'))[1:-1].replace(',','')
        rotate = str(scirun_get_module_state(module, 'CameraRotation'))[1:-1].replace(',','')
        zoom = str(scirun_get_module_state(module, 'CameraDistance'))
        viewerX = str(scirun_get_module_state(module, 'WindowSizeX'))
        viewerY = str(scirun_get_module_state(module, 'WindowSizeY'))
        break

write_viewscene = open(path+'\\Transform_Plans\\viewscene.txt','w')
write_viewscene.writelines([translate,'\n',rotate,'\n',zoom,'\n',viewerX,'\n',viewerY])
'''
write_translate = open(path+'\\Transform_Plans\\viewscene_translate.txt','w')
write_translate.write(translate)
write_translate.close()

write_rotate = open(path+'\\Transform_Plans\\viewscene_rotate.txt','w')
write_rotate.write(rotate)
write_rotate.close()

write_zoom = open(path+'\\Transform_Plans\\viewscene_zoom.txt','w')
write_zoom.write(zoom)
write_zoom.close()
'''