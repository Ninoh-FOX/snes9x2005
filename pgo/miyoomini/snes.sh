#!/bin/sh
# snes.sh LIST FRAMES core...: run every ROM of LIST (file names in Roms/SFC) with each core
. /tmp/sb/common.sh
L=$1; FR=$2; shift 2
OPT="/mnt/SDCARD/RetroArch/.retroarch/config/Snes9x 2005 Plus/Snes9x 2005 Plus.opt"
start
while IFS= read -r R; do
  for c in "$@"; do
    printf "%-10s %-26.26s " $(basename $c .so) "$R"
    /tmp/sb/lrbench $c "/mnt/SDCARD/Roms/SFC/$R" $FR "$OPT" 2>/dev/null | tail -1
  done
done < $L
stop
