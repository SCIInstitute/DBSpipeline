#/bin/bash

# set up paths to run the DBSPipeline code.
# https://github.com/SCIInstitute/DBSpipeline

script_fn="${BASH_SOURCE[0]}"
script=$(readlink -f $script_fn)
script_dir=$(dirname $script)

verbose_mode=false
dryrun=false

usage() {
  echo "Usage: $0 [OPTIONS]"
  echo "Options:"
  echo " -h, --help      Display this help message"
  echo " -v, --verbose   Enable verbose mode"
  echo " -n, --dry-run   check files of the script, but no action"
}

has_argument() {
    [[ ("$1" == *=* && -n ${1#*=}) || ( ! -z "$2" && "$2" != -*)  ]];
}

extract_argument() {
  echo "${2:-${1#*=}}"
}

# Function to handle options and arguments
handle_options() {
  verbose_mode=false
  dryrun=false
  while [ $# -gt 0 ]; do
    case $1 in
      -h | --help)
        usage
        exit 0
        ;;
      -v | --verbose)
        verbose_mode=true
        ;;
      --n | --dry-run)
        dryrun=true
        ;;
      *)
        echo "Invalid option: $1" >&2
        usage
        exit 1
        ;;
    esac
    shift
  done
}

# Main script execution

  
checkSysConfig(){
#  handle_options "$@"
#  if [ "$verbose_mode" = true ]; then
#   echo $sysconfig_fname
#  fi
  
  local sysconfig_fname="$1"
  
  if [ ! -f "$sysconfig_fname" ]; then
    if [ "$verbose_mode" = true ]; then
      echo file does not exist
    fi
    exit 0
  fi
  
  echo true
  exit 1
  
}

getSysName() {
  hname=$(hostname)
  if [[ $hname == *"ufhpc"* ]]; then
    sysname="hipergator"
  else
    sysname=${hname%%.*}
  fi
  echo $sysname
}

getCodeDir() {
#  script=$(readlink -f $0)
#  cwd=$(dirname $script)
  codedir=${script_dir%/*}
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
  handle_options "$@"
  
#  if [ "$verbose_mode" = true ]; then
#    echo $(getSysName)
#    echo $(getCodeDir)
#    echo $(getConfigDir)
#    echo $sysconfig_fname
#  fi
#  
  # assumes that this file hasn't been moved out of the repo
  local sysconfig_fname=$(getConfigDir)/$(getSysName).config
  readConfigFile $sysconfig_fname
  
  if [ "$verbose_mode" = true ]; then
    echo SYSNAME:  $SYSNAME
    echo DATADIR: $DATADIR
    echo CODEDIR: $CODEDIR
    echo TEMPDIR: $TEMPDIR
    echo FREESURFERDIR: $FREESURFERDIR
  fi
  
  
}

addConfigProfile() {

  local sysconfig_fname="$1"
  if ! $(checkSysConfig "$sysconfig_fname")
  then
    echo config file not found.  cannot add to .bashrc
    exit
  fi
  
  
  cat "${sysconfig_fname}" >> "${HOME}/.bashrc"

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
