# For dilating mask layers automatically in Seg3D.

# syntax in Seg3D python console
# exec(open(r'D:\Docs\UF\Employment\Neurology Student Assistant\Python\Seg3D Automation\Dilation.py').read())

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


avoid = [] #used for boolean remove later, meant to keep certain layers from being transformed
left_mask = []
layer_count = get(stateid='project_1::inputfiles_count') #Total number of layers
for i in range(layer_count): #find WMNull and atlas layers
    num = str(i)
    #print('\nlayer_'+num)
    layer = 'layer_'+num
    name = get(stateid=layer+'::name')
    if 'THALAMUS' in name: #Thalamus layer location for invert thalamus later
        thal = layer
        avoid.append(i)
    max = get(stateid=layer+'::max')
    if max == 1: #Thomas segments will only have a max of 1
        continue
    data_type = get(stateid=layer+'::data_type')
    if data_type == 'float':
        WMNull = num #wmnull layer location
        avoid.append(i)
    if data_type == 'int':
        atlas = num #atlas layer location
        avoid.append(i)
    left_mask.append(layer)

print('\nInput Layers:',layer_count)
print('WMNull: layer',WMNull)
print('atlas: layer',atlas)

atlas_name = get(stateid='layer_'+atlas+'::name')

if 'RIGHT' in atlas_name.upper():
    right_mask = []
    for i in range(layer_count):
        num = str(i)
        if num == atlas or num == WMNull:
            continue
        layer = 'layer_'+num
        action = threshold(layerid=layer, lower_threshold=1, upper_threshold=1)
        wait_on_layer(action,0.5)
        right_mask.append(action)
        if layer == thal:
            thal = action
            right_mask.pop()
        deletelayers(layers=layer)
        avoid.append(i)
    layer_count = int(action[-2:])


#CL thresholding
print('\n**Threshold**\n')
action = threshold(layerid='layer_'+atlas, lower_threshold=17, upper_threshold=17)
wait_on_layer(action,0.5)
avoid.append(int(action[-2:]))
CL_thresh = str(action)

layer_gen = str(get(stateid=action+'::generation')) #pulls when this layer was made, different from numbered layer name
if layer_gen != action[-2:]: #layer alignement, sometimes Seg3D likes to chnage layer numbers
    avoid.append(int(layer_gen))

#VPM thresholding
action = threshold(layerid='layer_'+atlas, lower_threshold=18, upper_threshold=18)
wait_on_layer(action,0.5)
avoid.append(int(action[-2:]))
VPM_thresh = str(action)
#print(VPM_thresh)

#Fast Dilate/Erode
print('\n**Fast Dilation**\n')
#CL
action = dilatefilter(layerid=CL_thresh,replace='false',radius='2',mask='<none>',invert_mask='false',only2d='false',slice_type='0')
wait_on_layer(action,0.5)
avoid.append(int(action[-2:]))
CL_dilate = str(action)
#VPM
action = dilatefilter(layerid=VPM_thresh,replace='false',radius='2',mask='<none>',invert_mask='false',only2d='false',slice_type='0')
wait_on_layer(action,0.5)
avoid.append(int(action[-2:]))
VPM_dilate = str(action)

#Invert the Thalamus
print('\n**Invert Thalamus**\n')
action = invert(layerid=thal,replace='false')
wait_on_layer(action,0.5)
avoid.append(int(action[-2:]))
inv_thal = str(action)

#Boolean Remove
print('\n**Boolean REMOVE**\n')
#Doing invert-thalamus first in case order matters
action = removefilter(layerid=CL_dilate,mask=inv_thal,replace='true')
wait_on_layer(action,0.5)
avoid.append(int(action[-2:]))

layer_count = int(action[-2:])

if 'RIGHT' in atlas_name.upper():
    for mask in right_mask:
        action = removefilter(layerid=CL_dilate,mask=mask,replace='true')
        print('Mask:',mask)
        wait_on_layer(action,0.5)
else:
    for i in range(layer_count):
        if i in avoid:  continue
        num = str(i)
        action = removefilter(layerid=CL_dilate,mask='layer_'+num,replace='true')
        print('Mask:',i)
        wait_on_layer(action,0.5)
