# Automate the process of dilating CL and its addition into THOMAS atlas
# exec(open(r'C:\Users\Matthew\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\Seg3D Automation\atlas_maker.py').read())
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

for i in range(id): #create masks of nuclei
    num = str(i)
    layer = 'layer_'+num
    max = get(stateid=layer+'::max')
    if max == 1: #Thomas segments will only have a max of 1
        action = threshold(layerid=layer, lower_threshold=1, upper_threshold=1)
        wait_on_layer(action,0.5)
        deletelayers(layers=layer)



action = importlayer(filename='['+atlas_dir+']',importer='[ITK Importer]',mode='data',inputfiles_id=str(id*2)) #load atlas
wait_on_layer(action[0], 0.5)
atlas = action[0]
atlas = atlas.split('_')
atlas = atlas[1]
id += 1
action = importlayer(filename='['+image_vol+']',importer='[ITK Importer]',mode='data',inputfiles_id=str(id*2)) #load WM/FGATIR
wait_on_layer(action[0], 0.5)

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


# thresholding
CL_thresh = threshold(layerid='layer_'+atlas, lower_threshold=17, upper_threshold=17)
wait_on_layer(CL_thresh,0.5)

VPM_thresh = threshold(layerid='layer_'+atlas, lower_threshold=18, upper_threshold=18)
wait_on_layer(VPM_thresh,0.5)

# Dilation
#CL
CL_dilate = dilatefilter(layerid=CL_thresh,replace='false',radius='2',mask='<none>',invert_mask='false',only2d='false',slice_type='0')
wait_on_layer(CL_dilate,0.5)
#VPM
VPM_dilate = dilatefilter(layerid=VPM_thresh,replace='false',radius='2',mask='<none>',invert_mask='false',only2d='false',slice_type='0')
wait_on_layer(VPM_dilate,0.5)

#Invert thalamus
inv_thal = invert(layerid=thal,replace='false')
wait_on_layer(inv_thal,0.5)


#Boolean Remove
#Doing invert-thalamus first in case order matters
action = removefilter(layerid=CL_dilate,mask=inv_thal,replace='true')
wait_on_layer(action,0.5)

for mask in masks: #everything else
    if mask == thal:
        continue #skip thalamus
    action = removefilter(layerid=CL_dilate,mask=mask,replace='true')
    wait_on_layer(action,0.5)
