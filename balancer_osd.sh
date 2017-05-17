#!/bin/bash

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

set_zero(){
  local float_num=$1 
  while :;do
    if [[ ${float_num: -1} -ne 0 ]];then
      local float_num=$(echo $float_num|awk '{printf("%.5f\n",$1+0.00001)}') 
    else
      echo $float_num
      return
    fi
  done
}

main(){
  while :;do
    ceph_status=$(ceph health detail)
    now_weight="$(ceph osd tree|grep ${task_osd}|awk '{printf("%.5f\n",$2)}')"
    now_weight=$(set_zero ${now_weight})
    [[ ${dest_weight} == ${now_weight} ]] && break || echo "$(date '+%Y-%m-%d/%H:%M:%S') $task_osd $now_weight => $dest_weight"
    if [[ ${ceph_status} == 'HEALTH_OK' ]];then
      weight=$(echo $now_weight $increment|awk '{printf("%.5f\n",$1+$2)}')
      ceph osd crush reweight $task_osd $weight &> /dev/null 
    fi
    sleep 10
  done
}

# osd name
task_osd=${1:-osd.12}
# 增量权重步长
increment=${2:-0.00500}
# 目标权重
dest_weight=${3:-3.00000}
main
