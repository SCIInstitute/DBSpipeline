#Prepares directory location for LegacyVTK.py file. Place a copy of this
# file into the folder with your fibers and double click. The text file named
# "paraview_dir" will be updated with the fiber folder path for LegacyVTK.py to use

#**Note**: I am doing it this way because I suck a programming

import os
file_path = os.getcwd()

f = open('C:/Users/Matthew/Dropbox (UFL)/DataProcessing/Pipeline Code/Python/Paraview/paraview_dir.txt','w')
f.write(file_path)
f.close()
