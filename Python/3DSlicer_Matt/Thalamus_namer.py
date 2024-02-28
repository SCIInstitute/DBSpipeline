
thal_parts = {                     # Different parts of the thalamus.
'_1_1': '_THALAMUS_1',        # The numbers correspond to the numbers
'_2_2': '_AV_2',              # used in the THOMAS algorithm
'_4_4': '_VA_4',
'_5_5': '_VLA_5',
'_6_6': '_VLP_6',
'_7_7': '_VPL_7',
'_8_8': '_PUL_8',
'_9_9': '_LGN_9',
'_10_10': '_MGN_10',
'_11_11': '_CM_11',
'_12_12': '_MDPF_12',
'_13_13': '_HB_13',
'_14_14': '_MTT_14',
'_17_17': '_CL_17',
'_18_18': '_VPM_18',
}

models = slicer.util.getNodes('*ModelNode*')


for model in models.keys():
    if 'LEFT' in model.upper():
        side = 'LEFT'
    elif 'RIGHT' in model.upper():
        side = 'RIGHT'
    else:
        continue
    for key,name in thal_parts.items():
        if key in model:
            nuc = name
            model_new = side + nuc
            models[model].SetName(model_new)
