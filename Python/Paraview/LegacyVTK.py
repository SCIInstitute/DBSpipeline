# Runs a directory of fiber data through Paraview to turn them into Ascii
# vtk files. Run this by going to the python shell in Paraview and
# clicking "Run Script". Navigate to this file and run it. You must run Dir_prep first.


import os

f = open('C:/Users/Matthew/Dropbox (UFL)/DataProcessing/Pipeline Code/Python/Paraview/paraview_dir.txt','r')
file_path = f.read(); #file directoty from Dir_prep.py

print(file_path)

files = os.listdir(file_path) #pull out all of the .vtk files
vtk_in = []
for file in files:
    if file.endswith('slicer.vtk'):
        #print(file)
        vtk_in.append(file)

#print(vtk_in)
for file in vtk_in: #convert vtk files to legacy vtk in Ascii
    reader = OpenDataFile(file_path +'/'+ file)
    file_name_new = file.replace('slicer','legacy')
    SaveData(file_path+'/'+file_name_new,reader,FileType='Ascii')

#writer = CreateWriter(file_path+'/test.vtk')
