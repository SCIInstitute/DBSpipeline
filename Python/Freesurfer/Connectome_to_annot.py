# Order connectivity data by HCP region for visualization


import nibabel.freesurfer.io as fsio
import numpy as np
import sys

def annot_swap(annot,data,side):
    labels, ctab, names = fsio.read_annot(annot)
    # print(names)
    if side == "right":
        labels = labels + 180
    if len(data) == 1:
        labels = np.zeros(len(labels),dtype=int)
    connectivity_label = []
    for index_label in labels:
        connectivity_label.append(data[index_label])

    return connectivity_label


# file = "connectome_matrix_MixSim_stim_3-Right_-4.2_nan_nan_nan-.csv"
# file = "connectome_matrix_MixSim_stim_1-Left_nan_nan_-3.5_-3.5-Right_nan_nan_-3.5_-3.5-.csv"
file = sys.argv[1]
con_mat = np.loadtxt(file,delimiter=",")
print(np.shape(con_mat))

left_label = "lh.HCPMMP1.annot"
right_label = "rh.HCPMMP1.annot"
mu = np.loadtxt("sift2_mu.txt")

if "Left" in file and "Right" in file:
    left_con = con_mat[-2,:]
    right_con = con_mat[-1,:]
elif "Left" in file:
    left_con = con_mat[-1,:]
    print("No Right Side")
    # right_con = [0]
    right_con = np.zeros(len(left_con))
elif "Right" in file:
    right_con = con_mat[-1,:]
    print("No Left Side")
    # left_con = [0]
    left_con = np.zeros(len(right_con))

    

# left_output = annot_swap(left_label,left_con,"left") * mu
# print(left_output[-5:])
# right_output = annot_swap(right_label,right_con,"right") * mu
# print(right_output[-5:])

# np.savetxt("con_left.txt",left_output)
# np.savetxt("con_right.txt",right_output)

np.savetxt("con_left.txt",left_con*mu)
np.savetxt("con_right.txt",right_con*mu)