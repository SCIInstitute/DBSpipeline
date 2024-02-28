# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 10:04:09 2024

@author: Matthew
"""

import pandas as pd
import os
import numpy as np
import argparse

#Inputs for calculation
parser = argparse.ArgumentParser(description='Inputs')
parser.add_argument('--subject',action='store',dest='subject',default=0)
parser.add_argument('--left_ROI',action='store',dest='ROI_list_left',type=int,default=np.NaN)
parser.add_argument('--right_ROI',action='store',dest='ROI_list_right',type=int,default=np.NaN)
args = parser.parse_args()
#print(args.subject, args.ROI_list_left, args.ROI_list_right)

if np.isnan(args.ROI_list_left) or np.isnan(args.ROI_list_right):
    raise Exception('Not Valid Region')

home = os.getcwd()
file_dir = home + '/' + args.subject + 'Cleaned/Fibers'

#Note: this notebook generates figures the rely on the data being from one region to everywhere else.
# ROI lists should be related as they will be combined into one region
subject = np.loadtxt(file_dir + '/connectome_matrix.csv', delimiter=',')
mu = np.loadtxt(file_dir + '/sift2_mu.txt')
# Lookup table
with open('/home/mphook/blue_butsonc/mphook/freesurfer/hcpmmp1_subcortex.txt','r') as f:
    labels = []
    for line in f:
        if line.startswith('#') or len(line) < 10:
            continue
        else:
            labels.append(line.split()[1])
            
ROI_list_left = np.array([args.ROI_list_left]) - 1 #to deal with starting at 1
ROI_list_right = np.array([args.ROI_list_right]) - 1
data = subject[1:,1:] * mu #Remove unassigned tracts, multiply "Fudge Factor"
data_left = data[:,ROI_list_left]
data_right = data[:,ROI_list_right]
'''
data_left_sum = np.sum(data_left,axis=1) #collapse all regions
data_right_sum = np.sum(data_right,axis=1)

data = np.column_stack((data_left_sum,data_right_sum))
data_weighted = data * mu #"Fudge Factor"
data_norm = data_weighted
#data_norm = data_weighted / np.sum(data_weighted)

ROI_left = data_norm[:,0]
ROI_right = data_norm[:,1]
'''
ROI_left = np.sum(data_left,axis=1) #collapse all regions
ROI_right = np.sum(data_right,axis=1)
ROI_left[ROI_list_left] = np.NAN #Remove regions from connectivity output
ROI_right[ROI_list_right] = np.NAN



percent = 100 #top k percentage of connections, not implemented at the moment
top = percent/100
Index_left = np.argsort(ROI_left) #Sort indicies and remove nan values
Index_left = Index_left[np.argwhere(~np.isnan(ROI_left[Index_left]))].squeeze()[::-1]
Index_right = np.argsort(ROI_right)
Index_right = Index_right[np.argwhere(~np.isnan(ROI_right[Index_right]))].squeeze()[::-1]

#ROI_left_top = ROI_left[Index_left[Index_left < 360]]
ROI_left_top = ROI_left[Index_left]
ROI_right_top = ROI_right[Index_right]
labels_left = np.array(labels)[Index_left[Index_left < len(labels)]]
labels_right = np.array(labels)[Index_right[Index_right < len(labels)]]

with open(file_dir + '/labels_left.txt','w') as f:
    count = 0
    for label in labels_left:
        print(label,Index_left[count]+1,ROI_left_top[count],file=f)
        count += 1
with open(file_dir + '/labels_right.txt','w') as f:
    count = 0
    for label in labels_right:
        print(label,Index_right[count]+1,ROI_right_top[count],file=f)
        count += 1    
        
        
file_path_1 = file_dir + '/labels_left.txt'
file_path_2 = file_dir + '/labels_right.txt'

f = open(file_path_1,'r')
connectome_1 = f.readlines()
f.close()

f = open(file_path_2,'r')
connectome_2 = f.readlines()
f.close()

shared = []
conn_1 = []
conn_2 = []
count = 0
for region in connectome_1:
    if region in connectome_2:
        shared.append(region.split()[0])
    else:
        conn_1.append(region.split()[0])

for region in connectome_2:
    if region in connectome_1:
        continue
    else:
        conn_2.append(region.split()[0])
        
#HCP Macro-regions
connectome_regions = {
    'Primary Visual Cortex': ['V1'],
    'Early Visual Cortex': ['V2','V3','V4'],
    'Dorsal Stream Visual Cortex': ['V3A','V3B','V7','V6','V6A','IPS1'],
    'Ventral Stream Visual Cortex': ['V8','VVC','VMV1','VMV2','VMV3','PIT','FFC'],
    'MT+ Complex and Neighboring Visual Areas': ['V3CD','LO1','LO2','LO3','MT','MST','V4t','FST','PH'],
    'Somatosensory and Motor Cortex': ['4','3b','3a','5m','1','2'],
    'Paracentral Lobular and Mid Cingulate Cortex': ['5L','5m','5mv','24dd','24dv','6mp','6ma','SCEF'],
    'Premotor Cortex': ['6a','6d','FEF','PEF','55b','6v','6r'],
    'Posterior Opercular Cortex': ['43','FOP1','OP4','OP2-3','OP1','PFcm'],
    'Early Auditory Cortex': ['A1','MBelt','LBelt','PBelt','RI'],
    'Auditory Association Cortex': ['A4','A5','STSdp','STSda','STSvp','STSva','TA2','STGa'],
    'Insular and Frontal Opercular Cortex': ['52','PI','Ig','PoI1','PoI2','FOP2','Pir','AAIC','MI','FOP3','FOP4','FOP5','AVI'],
    'Medial Temporal Cortex': ['H','PreS','EC','PeEc','PHA1','PHA2','PHA3'],
    'Lateral Temporal Cortex': ['TGd','TGv','TF','TE2p','TE2a','TE1a','TE1m','TE1p','PHT'],
    'Temporo-Parieto-Occipital Junction': ['TPOJ2','TPOJ3','TPOJ1','STV','PSL'],
    'Superior Parietal Cortex': ['MIP','LIPv','VIP','LIPd','AIP','7PC','7Am','7AL','7Pm','7PL'],
    'Inferior Parietal Cortex': ['PGp','IP0','IP1','IP2','PF','PFt','PFop','PFm','PGi','PGs'],
    'Posterior Cingulate Cortex': ['DVT','ProS','POS2','POS1','RSC','7m','PCV','v23ab','d23ab','31pv','31pd','31a','23d','23c'],
    'Anterior Cingulate and Medial Prefrontal Cortex': ['33pr','a24pr','p24pr','p24','a24','p32pr','a32pr','d32','p32','s32','8BM','9m','10r','10v','25'],
    'Orbital and Polar Frontal Cortex': ['OFC','pOFC','13l','11l','47s','47m','a47r','10pp','a10p','p10p','10d'],
    'Inferior Frontal Cortex': ['44','45','47l','IFJp','IFJa','IFSp','IFSa','p47r'],
    'DorsoLateral Prefrontal Cortex': ['SFL','s6-8','i6-8','8BL','8Ad','8Av','8C','9p','9a','9-46d','46','a9-46v','p9-46v']
}

subject_id = args.subject
PatientID = subject_id.split('/')[0]
#Add up regions to get macro-connectivity, any that are not part of HCP are put in on their own
region_connectivity = {
    'Patient ID': PatientID,
    'Hemisphere': "",
    'Primary Visual Cortex': 0,
    'Early Visual Cortex': 0,
    'Dorsal Stream Visual Cortex': 0,
    'Ventral Stream Visual Cortex': 0,
    'MT+ Complex and Neighboring Visual Areas': 0,
    'Somatosensory and Motor Cortex': 0,
    'Paracentral Lobular and Mid Cingulate Cortex': 0,
    'Premotor Cortex': 0,
    'Posterior Opercular Cortex': 0,
    'Early Auditory Cortex': 0,
    'Auditory Association Cortex': 0,
    'Insular and Frontal Opercular Cortex': 0,
    'Medial Temporal Cortex': 0,
    'Lateral Temporal Cortex': 0,
    'Temporo-Parieto-Occipital Junction': 0,
    'Superior Parietal Cortex': 0,
    'Inferior Parietal Cortex': 0,
    'Posterior Cingulate Cortex': 0,
    'Anterior Cingulate and Medial Prefrontal Cortex': 0,
    'Orbital and Polar Frontal Cortex': 0,
    'Inferior Frontal Cortex': 0,
    'DorsoLateral Prefrontal Cortex': 0,
}
left_region = region_connectivity.copy()
left_region["Hemisphere"] = "Left"
right_region = region_connectivity.copy()
right_region["Hemisphere"] = "Right"
left_leftover = connectome_1.copy()
right_leftover = connectome_2.copy()

for key in connectome_regions.keys():
    for region in connectome_1:
        if region.split()[0].split('_')[-1] in connectome_regions[key]:
            region_connectivity[key] = region_connectivity[key] + float(region.split()[-1].split('\n')[0])
            left_region[key] = left_region[key] + float(region.split()[-1].split('\n')[0])
            try:
                left_leftover.remove(region)
            except:
                continue
                
for region in left_leftover:
    keyname = region.split()[0].split('_')[-1]
    try:
        left_region[keyname] = left_region[keyname] + float(region.split()[-1].split('\n')[0])
    except:
        left_region[keyname] = float(region.split()[-1].split('\n')[0])
                
for key in connectome_regions.keys():
    for region in connectome_2:
        if region.split()[0].split('_')[-1] in connectome_regions[key]:
            region_connectivity[key] = region_connectivity[key] + float(region.split()[-1].split('\n')[0])
            right_region[key] = right_region[key] + float(region.split()[-1].split('\n')[0])
            try:
                right_leftover.remove(region)
            except:
                continue
                
for region in right_leftover:
    keyname = region.split()[0].split('_')[-1]
    try:
        right_region[keyname] = right_region[keyname] + float(region.split()[-1].split('\n')[0])
    except:
        right_region[keyname] = float(region.split()[-1].split('\n')[0])
        
all_data = region_connectivity


padding = ' ' * 35
filepath = file_path_1.split('labels')[0]
with open(filepath + 'Region_connectivity.txt', 'w') as f:
    for k,v in all_data.items():
        print('{:.50s} {}'.format(k + padding,v), file=f)
        
region_both = {'Region': left_region.keys(),'Left': left_region.values(), 'Right': right_region.values()}
region_both = [left_region, right_region]
df_regions = pd.DataFrame(data=region_both)
df_regions.to_csv(filepath +'Region_Connectivity.csv', index=False)