#!/bin/bash

. ./sysUtils.sh

sysconfig_fname=$(getConfigDir)/$(getSysName).config
readConfigFile $sysconfig_fname


echo $SYSNAME
echo $DATADIR
echo $CODEDIR
echo $TEMPDIR


python "${CODEDIR}/Python/Freesurfer/Connectome_maker.py" --subject $subject --lookup $lookup
