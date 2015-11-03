#!/bin/bash

export PATH='/sbin:/bin:/usr/sbin:/usr/bin'

# pid文件校验
pidCheck(){
  [[ ! -f $1 ]] && echo $$ > $1 && return 0
  if [[ -f $1 ]];then
    ps -p $(cat $1) &> /dev/null ; local rev=$?
    [[ $rev -eq 1 ]] && echo $$ > $1 && return 0
    echo "$(date) : $(cat $1) pid($1) exist." 
    exit 1
  fi
}

# 调用lftp操作
ftpOp(){
  lftp << EOF
set net:timeout $ftp_timeout
set net:max-retries 2
set net:reconnect-interval-base 5
set net:reconnect-interval-multiplier 1
open $ftp_type://$ftp_user:$ftp_pass@$ftp_host
$*
EOF
}

ftp_timeout=5
ftp_type='sftp'
ftp_user='username'
ftp_pass='password'
ftp_host='172.16.31.22'

pid_file=/tmp/$(basename $0).pid
pidCheck $pid_file

ftpOp $@

rm -f $pid_file
