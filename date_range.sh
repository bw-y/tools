#!/bin/bash

# 简单参数检查
argCheck(){
  if [[ -z $1 || -z $2 ]];then
    echo "Usage: $0 YYYYMMDD YYYYMMDD"
    exit 0
  fi
  if [[ $1 > $2 ]];then
    echo "The $1 > $2; Please input the right date. Exam:"
    echo "  $0 20140120 20140202"
    exit 0
  fi
}

# 替换echo行,或者直接引用输出
dateEach(){
  argCheck $1 $2
  local beg_date=$1 ; local end_date=$2
  while :;do
    
    echo "$beg_date"

    [[ "$beg_date" == "$end_date" ]] && break
    local beg_date=$(/bin/date -d "$beg_date 1 days" '+%Y%m%d')
    
  done
}

dateEach $1 $2
