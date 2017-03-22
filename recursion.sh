#!/bin/bash

export PATH="/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

rec(){
  test -f $1 && return
  for i in $(ls $1);do
    local now_path=$1/$i
    if test -f $now_path ;then
      echo "$now_path"
    elif test -d $now_path ;then
      echo "$now_path"
      rec $now_path
    fi
  done
}

get_timestamp(){
  local file_path=$(tail -1 $1)
  local end_range=${2:-1440}
  local last_timestamp=$(date -d "$(echo $file_path|sed "s@.*.\(20[1-9][0-9][0-1][0-9][0-3][0-9][0-2][0-9][0-5][0-9]\).tar.gz@\1@g"|sed "s@\(20[1-9][1-9]\)\([0-1][0-9]\)\([0-3][0-9]\)\([0-2][0-9]\)\(.*\)@\1-\2-\3 \4:\5@g")" +%s)
  local file_str=$(echo $file_path|sed "s@\(.*\)\(20[1-9].*.tar.gz\)@\1@g")
  for i in {0..1440};do
    local last_timestamp=$(($last_timestamp + 60))
    date -d @$last_timestamp "+$file_str%Y%m%d%H%M.tar.gz"
  done
}

rec $1
