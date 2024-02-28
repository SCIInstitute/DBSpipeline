#importlayer(filename='[C:/Users/Matthew/Dropbox (UFL)/Projects/NeuroPaceUH3/NeuroPaceLGS_Data-Analysis/Sinai/Mock/Segmentations/atlas_CL_left_ACPC.nrrd]',importer='[Teem Importer]',mode='data',inputfiles_id='5')

import tkinter as tk
from tkinter import filedialog
import subprocess

root = tk.Tk()
root.lift()
root.withdraw()
thomas_dir = filedialog.askdirectory(title='THOMAS Directory')

root = tk.Tk()
root.lift()
root.withdraw()
image_vol = filedialog.askopenfilename(title='Image Volume')


for hemi in ['left','right']: #make sure it is left,right
    nuc_dir = thomas_dir+'/'+hemi+'/Resample'
    atlas = thomas_dir+'/atlas_'+hemi+'_resamp.nii.gz'
    dir_file = open(r'D:\Seg3D\Seg3D2_2.5\bin\THOMAS_dir.txt','w')
    dir_file.writelines([nuc_dir+"\n", atlas+"\n", image_vol+"\n", thomas_dir+"\n"]) #write file locations to txt file
    dir_file.close()

    #subprocess.call(r'D:\Seg3D\Seg3D2_2.5\bin\Seg3D2.exe --python=atlas_maker.py', shell=True)
    subprocess.call(r'D:\Seg3D\Seg3D2_2.5\bin\Seg3D2.exe --python=atlas_maker_v2.py --headless', shell=True)
