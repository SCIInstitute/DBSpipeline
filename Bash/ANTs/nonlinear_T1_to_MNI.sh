#!/bin/bash

docker run -v ${PWD}:${PWD} -w ${PWD} --rm -t thomas bash -c "antsRegistrationSyN.sh -d 3 -f $2 -m $1 -o T1_to_MNI_ -n 8"
