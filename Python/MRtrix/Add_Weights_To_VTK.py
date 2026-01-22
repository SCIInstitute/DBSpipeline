import argparse
import numpy as np # type: ignore
parser = argparse.ArgumentParser(description='Insert single column data into vtk file')
parser.add_argument('--input_vtk', help='The input .vtk File')
parser.add_argument('--output_vtk', help='The output file')
parser.add_argument('--tract_data', help='The data to be written for each point.')

args = parser.parse_args()


vtk_in = args.input_vtk
data_in = args.tract_data
output_vtk = args.output_vtk

data = np.loadtxt(data_in)
number_of_points = len(data)

data_header = "POINT_DATA "+str(number_of_points)+"\n"+"FIELD FieldData 1\ncurv 1 "+str(number_of_points)+" double\n"
print(data_header)
# data_header = ["POINT_DATA" + len() str(number_of_points) \n","FIELD FieldData 1 \n","curv 1 str(number_of_points) double\n"]
with open(output_vtk, "w") as outfile:
    with open(vtk_in) as infile:
        for line in infile:
            outfile.write(line)
    outfile.write(data_header)
    with open(data_in) as infile:
        for line in infile:
            outfile.write(line)