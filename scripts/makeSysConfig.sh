#!/bin/bash

# set up paths to run the DBSPipeline code.
# https://github.com/SCIInstitute/DBSpipeline

 . ./sysUtils.sh

# custom functions
sysname=$(getSysName)
echo System: $(getSysName)

codedir=$(getCodeDir)
echo using $(getCodeDir) as code directory

configdir=$(getConfigDir)

sysconfig_fname=$configdir/$sysname.config


if ! $(checkSysConfig "$sysconfig_fname")
then
  echo config file not found.  Making new one:
  echo $sysconfig_fname
else
#  echo $sysconfig_fname
  read -p "config file $sysconfig_fname exists.
  Overwrite [y/N]" owrite
  if [ ! "$owrite" == "y" ] || [ -z "${owrite}" ]
  then
    echo Exiting
    exit
  fi
fi


message="enter data root location.  This is usually Dropbox folder:
"

data_dir=$(getUserDir "$message" | tail -n 1 )

echo ---- testing:
echo $data_dir


echo Data dir is: $data_dir

# tmp directory
# tracking directories
# envs

#/Users/jess/Dropbox/CT DBS Human/CENTURY S Patients/pDummy_connectome
#/Users/jess/UF_brainstim/scratch/


# default temp in unix - /var/tmp/

tempdirroot=/var/tmp
tempdir=$tempdirroot/DBSPipeline
#echo making a temp directory

temp_message="
default temp location is:
$tempdirroot
We will make a directory (DBSPipeline) here to use.
do you want to set a different location? [y/N]:"
read -p "$temp_message" tmp_q

if [ "$tmp_q" == "y" ]
then
  message="enter Temp directory path:
"
  tempdirroot=$(getUserDir "$message" | tail -n 1 )
fi

tempdir=$tempdirroot/DBSPipeline
echo  temp dir is: $tempdir
mkdir -p $tempdir

FSdir=$tempdirroot/FreeSurfer
echo  FreeSurfer dir is: $FSdir
mkdir -p $FSdir

echo writing config file
echo $sysconfig_fname

header_str="
##############
# system config file for the DBS pipeline code.
# config files should not be added to github,
# except for public/shared systems and paths
#
"

echo "$header_str" > $sysconfig_fname
echo export SYSNAME=\"$sysname\" >> $sysconfig_fname
echo export DATADIR=\"$data_dir\" >> $sysconfig_fname
echo export CODEDIR=\"$codedir\" >> $sysconfig_fname
echo export TEMPDIR=\"$tempdir\" >> $sysconfig_fname
echo export FREESURFERDIR=\"$FSdir\" >> $sysconfig_fname
echo export PATH='$PATH:'\"$codedir/scripts\" >> $sysconfig_fname


read -p "add $sysconfig_fname to .basrc file? [y/N]:" profile
if [ ! "$profile" == "y" ] || [ -z "${profile}" ]
then
  echo Exiting
  exit
fi

addConfigProfile $sysconfig_fname

