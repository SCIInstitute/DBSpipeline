# Automate the process of dilating CL and its addition into THOMAS atlas
# exec(open(r'C:\Users\Matthew\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\Seg3D Automation\atlas_maker_v2.py').read())
import os
import threading

class MyThread(threading.Thread): #Threading needed for function timing
    def __init__(self, layerID, timeout=2.0, max_iterations=1000):
        self.layerID = layerID
        self.TIMEOUT = timeout
        self.MAX_ITERATIONS = max_iterations
        self.condition = threading.Condition()
        threading.Thread.__init__(self)
    def run(self):
    #print(self.layerID[0])
    #print(type(self.layerID))
        stateIDData = self.layerID + "::data"
        layerStatus = get(stateid=stateIDData)
        print(self.layerID, layerStatus)
        with self.condition:
            self.condition.wait_for(lambda: "available" == get(stateid=stateIDData), timeout=self.TIMEOUT)
        print("Layer {} done processing".format(self.layerID))

def wait_on_layer(layer, timeout=2.0):
  thread = MyThread(layer, timeout)
  thread.start()
  thread.join()


dir_file = open(r'D:\Seg3D\Seg3D2_2.5\bin\THOMAS_dir.txt','r') # file locations

dirs = dir_file.readlines()
count = 0
for dir in dirs: #remove newlines
    dirs[count] = dir[0:-1]
    count = count + 1
print(dirs)
nuc_dir = dirs[0]
atlas_dir = dirs[1]
image_vol = dirs[2]
thomas_dir = dirs[3]

nuclei = os.listdir(nuc_dir)
#print('['+nuc_dir+'/'+nuclei[0]+']')
#importlayer(filename='['+nuc_dir+'/'+nuclei[0]+']',importer='[ITK Importer]', mode='data',inputfiles_id='1')
#importlayer(filename='[C:/Users/Matthew/Dropbox (UFL)/Projects/NeuroPaceUH3/NeuroPaceLGS_Data-Analysis/Sinai/Mock/Segmentations/Thomas/left/Resample/1-THALAMUS_resamp.nii.gz]',importer='[ITK Importer]',mode='data',inputfiles_id='1')
#print(nuclei.split('-')[0].sort(key = int))
id = 0
for nucleus in nuclei: #load the nuclei
    action = importlayer(filename='['+nuc_dir+'/'+nucleus+']',importer='[ITK Importer]', mode='data',inputfiles_id=str(id))
    wait_on_layer(action[0], 0.5)
    id = id + 1
mask_id = []
for i in range(id): #create masks of nuclei
    num = str(i)
    layer = 'layer_'+num
    max = get(stateid=layer+'::max')
    if max == 1: #Thomas segments will only have a max of 1
        action = threshold(layerid=layer, lower_threshold=1, upper_threshold=1)
        wait_on_layer(action,0.5)
        mask_id.append(action)
        deletelayers(layers=layer)

for mask in mask_id:
    if 'THALAMUS' in get(stateid=mask+'::name'):
        thal = mask
#for mask in mask_id:
#    print(mask,get(stateid=mask+'::name'))

action = importlayer(filename='['+atlas_dir+']',importer='[ITK Importer]',mode='data',inputfiles_id=str(id*2)) #load atlas
wait_on_layer(action[0], 0.5)
atlas = action[0]
#atlas = atlas.split('_')
#atlas = atlas[1]
#id += 1
action = importlayer(filename='['+image_vol+']',importer='[ITK Importer]',mode='data',inputfiles_id=str(id*2)) #load WM/FGATIR
wait_on_layer(action[0], 0.5)
WMNull = action[0]
"""
masks = []
print(get(stateid='project_1::inputfiles_count'))
layer_count = get(stateid='project_1::inputfiles_count') + len(nuclei) #Total number of layers
for i in range(layer_count): #find WMNull and atlas layers
    num = str(i)
    #print('\nlayer_'+num)
    layer = 'layer_'+num
    name = get(stateid=layer+'::name')
    if 'UNDO' in name: #skip deleted layers
        continue
    if 'THALAMUS' in name: #Thalamus layer location for invert thalamus later
        thal = layer
    max = get(stateid=layer+'::max')
    if max == 1: #Thomas segments will only have a max of 1
        masks.append(layer)
        continue
    data_type = get(stateid=layer+'::data_type')
    if data_type == 'float':
        WMNull = num #wmnull layer location
    #if data_type == 'int':
    #    atlas = num #atlas layer location
"""

# thresholding
CL_thresh = threshold(layerid=atlas, lower_threshold=17, upper_threshold=17)
wait_on_layer(CL_thresh,0.5)

VPM_thresh = threshold(layerid=atlas, lower_threshold=18, upper_threshold=18)
wait_on_layer(VPM_thresh,0.5)

# Dilation
#CL
CL_dilate = dilatefilter(layerid=CL_thresh,replace='false',radius='2',mask='<none>',invert_mask='false',only2d='false',slice_type='0')
wait_on_layer(CL_dilate,0.5)
#VPM
VPM_dilate = dilatefilter(layerid=VPM_thresh,replace='false',radius='2',mask='<none>',invert_mask='false',only2d='false',slice_type='0')
wait_on_layer(VPM_dilate,0.5)

# Invert thalamus
inv_thal = invert(layerid=thal,replace='false')
wait_on_layer(inv_thal,0.5)


# Boolean Remove
#Doing invert-thalamus first in case order matters
action = removefilter(layerid=CL_dilate,mask=inv_thal,replace='true')
wait_on_layer(action,0.5)
action = removefilter(layerid=VPM_dilate,mask=inv_thal,replace='true')
wait_on_layer(action,0.5)

for mask in mask_id: #everything else
    if mask == thal:
        continue #skip thalamus
    action = removefilter(layerid=CL_dilate,mask=mask,replace='true')
    wait_on_layer(action,0.5)
    if '_11-' in get(stateid=mask+'::name'): #prioritize CM over VPM
        action = removefilter(layerid=VPM_dilate,mask=mask,replace='true')
        wait_on_layer(action,0.5)

action = removefilter(layerid=VPM_dilate,mask=CL_dilate,replace='true') #prioritize CL
wait_on_layer(action,0.5)

# Build Blank layer
# blank = newmasklayer(groupid="group::0")
blank = duplicatelayer(layerid=VPM_dilate)
wait_on_layer(blank,0.5)
blank = removefilter(layerid=blank,mask=VPM_dilate,replace='true') #remove all data from layer, making it zeros
wait_on_layer(blank,0.5)


#Prepare Exports
export_name = get(stateid=atlas+'::name')
parts = export_name.split('_')
hemi = parts[1]
export_name = export_name.replace(hemi+'_resamp','CL_'+hemi)
#print(export_name)


export_layers = [thal] #Build layers in correct order
nuc_export = []
nuc_names_export = []
for i in range(2,17):
    check = False
    mask_val = '_'+str(i)+'-'
    for mask in mask_id:
        if mask_val in get(stateid=mask+'::name'):
            export_layers.append(mask)
            check = True
            if i == 7: #for exporting specific layers
                nuc_export.append(mask)
                nuc_names_export.append('VPL_'+hemi)
            if i == 11:
                nuc_export.append(mask)
                nuc_names_export.append('CM_'+hemi)
            if i == 12:
                nuc_export.append(mask)
                nuc_names_export.append('MD_'+hemi)
    if check == False:
        export_layers.append(blank) #if a layer is missing, fill it in with a blank one

export_layers.append(CL_dilate)
export_layers.append(VPM_dilate)

mask_names = []
for mask in export_layers:
    mask_names.append(get(stateid=mask+'::name'))

print(mask_names)

# Export Label maps
exportsegmentation(layers=export_layers,file_path='['+thomas_dir+'/'+export_name+']',mode='label_mask',extension='.nrrd',exporter='[NRRD Exporter]')

# Export Relevant Nuclei
nuc_export.append(CL_dilate)
nuc_names_export.append('CL_'+hemi)
nuc_export.append(VPM_dilate)
nuc_names_export.append('VPM_'+hemi)

if len(nuc_export) > 0:
    for i in range(0,len(nuc_export)):
        set(stateid=nuc_export[i]+'::name',value=nuc_names_export[i])
        #exportsegmentation(layers='[['+nuc_export[i]+']]',file_path='['+thomas_dir+'/'+nuc_names_export[i]+']',mode='single_mask',extension='.nii.gz',exporter='[NRRD Exporter]')
        exportsegmentation(layers='[['+nuc_export[i]+']]',file_path='['+thomas_dir+']',mode='single_mask',extension='.nii.gz',exporter='[NRRD Exporter]')

#Export WMn for registration purposes
exportlayer(layer=WMNull,file_path='['+thomas_dir+'/wmn_seg3d]',extension='.nii.gz',exporter='[ITK Data Exporter]')


#computeisosurface(layerid='layer_31',quality_factor='1',capping='true',show='true')
