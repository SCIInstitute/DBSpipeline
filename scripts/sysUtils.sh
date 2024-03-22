#/bib/bash

# set up paths to run the DBSPipeline code.
# https://github.com/SCIInstitute/DBSpipeline

checkSysConfig(){
  local sysconfig_fname="$1"
#  echo $sysconfig_fname
  if [ ! -f "$sysconfig_fname" ]; then
#    echo file does not exist
    exit 0
  fi
  
  echo true
  exit 1
  
}

getSysName() {
  hname=$(hostname)
  sysname=${hname%%.*}
  echo $sysname
}

getCodeDir() {
  script=$(readlink -f $0)
  cwd=$(dirname $script)
  codedir=${cwd%/*}
  echo $codedir
}

getConfigDir () {
  configdir=$(getCodeDir)/config_files
  mkdir -p $configdir
  echo $configdir
}

getUserDir () {
# trying local scope because of rewriting
  if [ -z "$1" ]
  then
    echo Line message needed
    exit 0
  fi

  local message="$1"
  local d_dir=" "

  if [ ! -z $2 ]
  then
    local d_dir="$2"
  fi

  echo $d_dir

  while [ ! -d "$d_dir" ]
  do
    echo not found
    read -p "$message" d_dir
  done

  local data_dir=$(readlink -f "$d_dir")
  echo $data_dir

}


readConfigFile () {
local fname="$1"

while read varline
do
  if [[ "$varline" == "#"* ]] || [ -z "$varline" ]; then continue; fi
  
  eval "$varline"
done <$fname
}

runConfigFile () {
# doesn't really work
  local fname="$1"

  exstr="#!/bin/bash"
  configstr="$(<$fname)"

  fname_sh=$fname.sh
  echo $exstr > $fname_sh
  echo $configstr >> $fname_sh

  chmod a+x $fname_sh

  $fname_sh
}



innitBashPaths () {
  # assumes that this file hasn't been moved out of the repo
  local sysconfig_fname=$(getConfigDir)/$(getSysName).config
  readConfigFile $sysconfig_fname
  
}


main() {
  echo "runnin utils"
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    # This script is being run.
    __name__="__main__"
else
    # This script is being sourced.
    __name__="__source__"
fi


if [ "$__name__" = "__main__" ]; then
    main "$@"
fi
