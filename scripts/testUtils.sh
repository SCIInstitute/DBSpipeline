#!/bin/bash

#script=$(readlink -f $0)
#sc_dir=$(dirname $(readlink -f $0))
. $(dirname $(readlink -f $0))/sysUtils.sh

innitBashPaths -v


python "${CODEDIR}/Python/Freesurfer/Connectome_maker.py" --subject $subject --lookup $lookup

