#!/usr/bin/env bash

# =================
# Utility functions
# =================

function read_options() {

  local options

  # https://dustymabe.com/2013/05/17/easy-getopt-for-a-bash-script/
  options=$(getopt --options k --longoptions keepalive -- "$@")

  # Call getopt to validate the provided input.
  [ $? -eq 0 ] || {
      echo "Incorrect options provided"
      exit 1
  }
  eval set -- "$options"
  while true; do
      case "$1" in
      -k)
          KEEPALIVE=true
          shift
          continue
          ;;
      --keepalive)
          KEEPALIVE=true
          shift
          continue
          ;;
      --)
          shift
          break
          ;;
      esac
      shift
  done
  SUBCOMMAND=$1

}

function title() {
  text=$1
  len=${#text}
  guard=$(printf "%${len}s" | sed 's/ /=/g')
  echo
  echo ${guard}
  echo -e "${BYELLOW}${text}${NC}"
  echo ${guard}
}

function init_colors() {
  # Reset
  NC='\033[0m'

  # Regular
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[0;33m'
  BLUE='\033[0;34m'
  PURPLE='\033[0;35m'
  CYAN='\033[0;36m'
  WHITE='\033[0;37m'

  # Bold
  BBLACK='\033[1;30m'
  BRED='\033[1;31m'
  BGREEN='\033[1;32m'
  BYELLOW='\033[1;33m'
  BBLUE='\033[1;34m'
  BPURPLE='\033[1;35m'
  BCYAN='\033[1;36m'
  BWHITE='\033[1;37m'
}
