#!/bin/bash


hname=$(hostname)

sysname=${hname%%.*}
#echo $hname
echo System: $sysname

script=$(readlink -f $0)
cwd=$(dirname $script)
codedir=${cwd%/*}

echo using $codedir as code directory

configdir=$codedir/configs
mkdir -p $configdir

sysconfig_fname=$configdir/$sysname.config

echo $sysconfig_fname

message="enter data root location.  This is usually Dropbox folder: "
d_dir=""
while [ ! -d "$d_dir" ]
do
read -p "$message" d_dir
done

data_dir=$(readlink -f $d_dir)

echo Data dir is: $data_dir
