#importlayer(filename='[C:/Users/Matthew/Dropbox (UFL)/Projects/NeuroPaceUH3/NeuroPaceLGS_Data-Analysis/Sinai/Mock/Segmentations/atlas_CL_left_ACPC.nrrd]',importer='[Teem Importer]',mode='data',inputfiles_id='5')

import tkinter as tk
from tkinter import filedialog
import subprocess

root = tk.Tk()
root.lift()
root.withdraw()
nuc_dir = filedialog.askdirectory(title='Nuclei Directory')

root = tk.Tk()
root.lift()
root.withdraw()
atlas = filedialog.askopenfilename(title='Atlas')

root = tk.Tk()
root.lift()
root.withdraw()
image_vol = filedialog.askopenfilename(title='Image Volume')

dir_file = open(r'D:\Seg3D\Seg3D2_2.5\bin\THOMAS_dir.txt','w')

dir_file.writelines([nuc_dir+"\n", atlas+"\n", image_vol+"\n"]) #write file locations to txt file

dir_file.close()

#subprocess.call(r'D:\Seg3D\Seg3D2_2.5\bin\Seg3D2.exe --python=atlas_maker.py', shell=True)
subprocess.call(r'D:\Seg3D\Seg3D2_2.5\bin\Seg3D2.exe --python=atlas_maker_v2.py', shell=True)
