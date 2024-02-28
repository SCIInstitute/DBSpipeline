# syntax in Seg3D python console
# exec(open(r'D:\Docs\UF\Employment\Neurology Student Assistant\Python\Seg3D Automation\Right_test.py').read())

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
    print(self.layerID, " ", layerStatus)
    with self.condition:
      self.condition.wait_for(lambda: "available" == get(stateid=stateIDData), timeout=self.TIMEOUT)
    print("Layer {} done processing".format(self.layerID))

def wait_on_layer(layer, timeout=2.0):
  thread = MyThread(layer, timeout)
  thread.start()
  thread.join()


avoid = [] #used for boolean remove later, meant to keep certain layers from being transformed
layer_count = get(stateid='project_1::inputfiles_count') #Total number of layers
for i in range(layer_count): #find WMNull and atlas layers
    num = str(i)
    #print('\nlayer_'+num)
    layer = 'layer_'+num
    print(layer)
    name = get(stateid=layer+'::name')
    if 'THALAMUS' in name: #Thalamus layer location for invert thalamus later
        thal = str(i)
        avoid.append(layer_count)
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

print('\nInput Layers:',layer_count)
print('WMNull: layer',WMNull)
print('atlas: layer',atlas)

atlas_name = get(stateid='layer_'+atlas+'::name')

if 'RIGHT' in atlas_name.upper():
    for i in range(layer_count):
        num = str(i)
        if num == atlas or num == WMNull:
            continue
        layer = 'layer_'+num
        action = threshold(layerid=layer, lower_threshold=1, upper_threshold=1)
        wait_on_layer(action,0.5)
        deletelayers(layers=layer)
        avoid.append(i)
    layer_count = int(action[-2:])
