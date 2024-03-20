#!/bin/bash

# set up paths to run the DBSPipeline code.
# https://github.com/SCIInstitute/DBSpipeline

 . ./sysUtils.sh

# custom functions
sysname=$(getSysName)
echo System: $(getSysName)

codedir=$(getCodeDir)
configdir=$(getConfigDir)

sysconfig_fname=$configdir/$sysname.config

echo $sysconfig_fname

#echo $(checkSysConfig "$sysconfig_fname")
if ! $(checkSysConfig "$sysconfig_fname")
then
  echo config file not found.  run makeSysConfig.sh to make one.
  exit
fi

readConfigFile $sysconfig_fname

#vars=($(readConfigFile $sysconfig_fname))
#for v in ${vars[@]}
#do
#
#echo line: $v
#done






