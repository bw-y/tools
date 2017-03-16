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

rec $1
