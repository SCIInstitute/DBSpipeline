import json
import numpy as np

import os





connectome_file = os.path.join(os.environ["CODEDIR"], 
"Python/connectomics/connectome_maps/HCP_MacroRegions.json")

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
    'Insular and Frontal Opercular Cortex': 
['52','PI','Ig','PoI1','PoI2','FOP2','Pir','AAIC','MI','FOP3','FOP4','FOP5','AVI'],
    'Medial Temporal Cortex': ['H','PreS','EC','PeEc','PHA1','PHA2','PHA3'],
    'Lateral Temporal Cortex': ['TGd','TGv','TF','TE2p','TE2a','TE1a','TE1m','TE1p','PHT'],
    'Temporo-Parieto-Occipital Junction': ['TPOJ2','TPOJ3','TPOJ1','STV','PSL'],
    'Superior Parietal Cortex': ['MIP','LIPv','VIP','LIPd','AIP','7PC','7Am','7AL','7Pm','7PL'],
    'Inferior Parietal Cortex': ['PGp','IP0','IP1','IP2','PF','PFt','PFop','PFm','PGi','PGs'],
    'Posterior Cingulate Cortex': 
['DVT','ProS','POS2','POS1','RSC','7m','PCV','v23ab','d23ab','31pv','31pd','31a','23d','23c'],
    'Anterior Cingulate and Medial Prefrontal Cortex': 
['33pr','a24pr','p24pr','p24','a24','p32pr','a32pr','d32','p32','s32','8BM','9m','10r','10v','25'],
    'Orbital and Polar Frontal Cortex': ['OFC','pOFC','13l','11l','47s','47m','a47r','10pp','a10p','p10p','10d'],
    'Inferior Frontal Cortex': ['44','45','47l','IFJp','IFJa','IFSp','IFSa','p47r'],
    'DorsoLateral Prefrontal Cortex': 
['SFL','s6-8','i6-8','8BL','8Ad','8Av','8C','9p','9a','9-46d','46','a9-46v','p9-46v']
}

with open(connectome_file, 'w') as fp:
    json.dump(connectome_regions, fp)



