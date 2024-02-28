#For creating masks if the layers are not ones already

# syntax in Seg3D python console
# exec(open(r'C:\Users\Matthew\Dropbox (UFL)\DataProcessing\Pipeline Code\Python\Seg3D Automation\Mask_Maker.py').read())

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



layer_count = get(stateid='project_1::inputfiles_count') #Total number of layers
for i in range(layer_count):
    num = str(i)
    layer = 'layer_'+num
    max = get(stateid=layer+'::max')
    if max == 1: #Thomas segments will only have a max of 1
        action = threshold(layerid=layer, lower_threshold=1, upper_threshold=1)
        wait_on_layer(action,0.5)
        deletelayers(layers=layer)
