import os
import numpy as np
import argparse
import json
import pandas as pd

def build_parser():
    parser = argparse.ArgumentParser(
        prog = "exemplar_regions",
        description = "generates ordered csv of regions included in exemplar output",
        epilog = "output: region list"
    )

    parser.add_argument("-r", "--raw", required=True,
                        help="raw exemplar weights csv",
                        dest="raw")
    
    parser.add_argument("-p", "--profile", required=True,
                        help="experiment profile used for exemplars",
                        dest="profile")
    
    parser.add_argument("-m", "--macro", required=True,
                        help="macro HCP regions",
                        dest="macro")
    return parser
    
def main():
    parser = build_parser()
    args = parser.parse_args()

    raw = [float(i) for i in np.loadtxt(args.raw, delimiter=",", dtype=str) if not i == ""]
    try:
        cleaned = [float(i) for i in np.loadtxt(args.raw.replace('_raw',''), delimiter=",", dtype=str) if not i == ""]
    except:
        cleaned = [float(i) for i in np.loadtxt(args.raw.replace('_raw',''), delimiter=" ", dtype=str) if not i == ""]

    # print(raw)
    # print(cleaned)
    with open(args.profile, 'r') as js_file:
        profile = json.load(js_file)
    
    with open(args.macro, 'r') as js_file:
        macro = json.load(js_file)

    lookup_table = profile["lookup_table"]
    fibertractPath = profile["fibertractPath"]
    indexPath = profile["Connectome_maker"]["Output_files"]["matkey_outputname"]
    # print(lookup_table)
    # print(indexPath)

    lookup = pd.read_csv(lookup_table)
    index = pd.read_csv(indexPath)

    mrtrix_node = []
    weights = []
    
    for i,weight in enumerate(raw):
        if weight in cleaned:
            mrtrix_node.append(i)
            weights.append(weight)

    # print(index["Lookup Index"][mrtrix_node])

    # print('Nodes:',mrtrix_node)
    lookup_node = []
    lookup_regions = []
    lookup_node = np.array(index["Lookup Index"][mrtrix_node], dtype=int)
    # print('Nodes:',lookup_node)

    for i in range(len(lookup_node)):
        lookup_search = lookup.loc[lookup['Index'] == lookup_node[i], 'Labels']
        if lookup_search.tolist()[0] == "L_CL":
            print((lookup_node[i], mrtrix_node[i], weights[i]))
        lookup_regions.append(lookup_search.iloc[0])
    # print("Regions:",lookup_regions)

    HCP_all = [x for xs in macro.values() for x in xs]
    HCP_regions = []
    for region in lookup_regions:
        try:
            name = region.split('_')[1]
        except:
            name = region
        if name not in HCP_all:
                HCP_regions.append(name)
        for group in macro:
            if name in macro[group]:
                HCP_regions.append(group)

    region_list = {'Region': HCP_regions,'Name':lookup_regions, 'Connectivity':cleaned}
    print(len(region_list['Region']),len(region_list['Name']),len(region_list['Connectivity']))

    df_output = pd.DataFrame(region_list)
    out_path = os.path.dirname(args.raw)
    out_name = os.path.basename(args.raw.replace('_raw','')).split('.')[0] + '_regions.csv'
    df_outputfile = os.path.join(out_path,out_name)
    print(df_outputfile)
    df_output.to_csv(df_outputfile, index=False)

if __name__ == "__main__":
    main()
    



