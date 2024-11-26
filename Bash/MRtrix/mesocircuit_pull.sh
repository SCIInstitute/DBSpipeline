#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8gb
#SBATCH --time=1:00:00
#SBATCH --job-name=mesocircuit
#SBATCH --mail-type=ALL
#SBATCH --output=meso_%j.out

#########

# Pull mesocircuit tracts from connectomes. **Currently only to be used on CL_only profile**

# sbatch --mail-user="user"@ufl.edu $CODEDIR/Bash/MRtrix/mesocircuit_pull.sh p102

#########

set -e

if [[ -z "$SYSNAME" ]]; then
echo environment not set.  run makeSysConfig.sh
exit
fi

if [ $SYSNAME == "hipergator" ]
then
	module load mrtrix
fi

subject=$1
sub_dir="${DATADIR}/${subject}"

# assignment=assignments_CLonly.txt
# left_roi=371
# right_roi=372
# roi_name=CL

# assignment=assignments_Therapy.txt
# left_roi=415
# right_roi=416
# roi_name=Stim

assignment=assignments_CM.txt
left_roi=373
right_roi=387
roi_name=CM

# Anterior Cingulate and Medial Prefrontal projection
echo -e "\nAnterior Cingulate and Medial Prefrontal projection\n"
projection=ACC
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR
region=58,238,59,239,57,237,180,360,61,241,60,240,179,359,62,242,64,244,165,345,63,243,69,249,65,245,88,268,164,344
#Left side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/${projection}_ -nodes ${region},${left_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/*${left_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck -force
#Right side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/${projection}_ -nodes ${region},${right_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/*${right_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck -force

tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.vtk -force
tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.vtk -force
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR


# Caudate
echo -e "\nCaudate\n"
projection=Caudate
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR
region=361,366
#Left side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/${projection}_ -nodes ${region},${left_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/*${left_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck -force
#Right side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/${projection}_ -nodes ${region},${right_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/*${right_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck -force

tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.vtk -force
tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.vtk -force
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR



# DorsoLateral Prefrontal projection
echo -e "\nDorsoLateral Prefrontal projection\n"
projection=DLpfc
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR
region=26,206,98,278,97,277,70,250,68,248,67,247,73,253,71,251,87,267,86,266,84,264,85,265,83,263
#Left side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/${projection}_ -nodes ${region},${left_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/*${left_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck -force
#Right side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/${projection}_ -nodes ${region},${right_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/*${right_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck -force

tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.vtk -force
tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.vtk -force
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR



# Inferior Parietal projection
echo -e "\nInferior Parietal projection\n"
projection=InfPar
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR
region=143,323,146,326,145,325,144,324,148,328,116,296,147,327,149,329,150,330,151,331
#Left side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/${projection}_ -nodes ${region},${left_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/*${left_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck -force
#Right side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/${projection}_ -nodes ${region},${right_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/*${right_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck -force

tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.vtk -force
tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.vtk -force
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR



# Insular and Frontal Opercular projection
echo -e "\nInsular and Frontal Opercular projection\n"
projection=InsFroOp
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR
region=103,283,178,358,168,348,167,347,106,286,115,295,110,290,112,292,109,289,114,294,108,288,169,349,111,291
#Left side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/${projection}_ -nodes ${region},${left_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/*${left_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck -force
#Right side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/${projection}_ -nodes ${region},${right_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/*${right_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck -force

tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.vtk -force
tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.vtk -force
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR



# Premotor projection
echo -e "\nPremotor projection\n"
projection=Premotor
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR
region=96,276,54,234,10,190,11,191,12,192,56,236,78,258
#Left side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/${projection}_ -nodes ${region},${left_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/*${left_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck -force
#Right side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/${projection}_ -nodes ${region},${right_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/*${right_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck -force

tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.vtk -force
tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.vtk -force
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR



# Somatosensory and Motor projection
echo -e "\nSomatosensory and Motor projection\n"
projection=SomaMot
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR
region=8,188,9,189,53,233,51,231,52,232
#Left side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/${projection}_ -nodes ${region},${left_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/*${left_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck -force
#Right side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/${projection}_ -nodes ${region},${right_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/*${right_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck -force

tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.vtk -force
tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.vtk -force
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR



# Superior Parietal projection
echo -e "\nSuperior Parietal projection\n"
projection=SupPar
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR
region=50,230,48,228,49,229,95,275,117,297,47,227,45,225,42,222,29,209,46,226
#Left side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/${projection}_ -nodes ${region},${left_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/*${left_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck -force
#Right side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/${projection}_ -nodes ${region},${right_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/*${right_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck -force

tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.vtk -force
tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.vtk -force
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR



# Temporo-Parieto-Occipital Junction Projection
echo -e "\nTemporo-Parieto-Occipital Junction Projection\n"
projection=TempParOcc
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR
region=140,320,141,321,139,319,28,208,25,205
#Left side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/${projection}_ -nodes ${region},${left_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/*${left_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck -force
#Right side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/${projection}_ -nodes ${region},${right_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/*${right_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck -force

tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.vtk -force
tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.vtk -force
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR



# Paracentral Lobular and Mid Cingulate Projection
echo -e "\nParacentral Lobular and Mid Cingulate Projection\n"
projection=ParaLobMidCC
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
mkdir -p ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR
region=39,219,36,216,37,217,40,220,41,221,55,235,44,224,43,223
#Left side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/${projection}_ -nodes ${region},${left_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL/*${left_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck -force
#Right side
connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/${projection}_ -nodes ${region},${right_roi} -exclusive -force
tckedit ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR/*${right_roi}* ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck -force
tcktransform ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck -force

tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_left_${projection}_ACPC.vtk -force
tckconvert ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.tck ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/${roi_name}_right_${projection}_ACPC.vtk -force
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpL
rm -r ${sub_dir}/Tractography/Cleaned/Fibers/${projection}/tmpR
