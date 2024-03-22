#!/bin/bash

. ./sysUtils.sh

innitBashPaths


echo $SYSNAME
echo $DATADIR
echo $CODEDIR
echo $TEMPDIR


python "${CODEDIR}/Python/Freesurfer/Connectome_maker.py" --subject $subject --lookup $lookup
