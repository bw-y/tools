#!/bin/bash

export PATH=/usr/sbin:/usr/bin:/sbin:/bin

check_url_set_out_put(){
  local ip_list_file=$1
  local url=${2:-v.bw-y.com}
  #local url=${2:-$(openssl rand -hex $(echo $(($RANDOM%2+1)))).z.bw-y.com}
  local location=${3:-down}
  local key=${4:-soft}
  local post=${5:-1}
  local curl_cmd="curl --connect-timeout 1 -m 2 -s -i"
  [[ $post -eq 0 ]] && local curl_cmd="$curl_cmd -d "data=$(openssl rand -hex $(echo $(($RANDOM%2+1))))""
  local ok_total=0
  for i in $(cat $ip_list_file);do 
    local tag=0
    local flag=0
    local ip=$(echo "$i"|awk -F_ '{print $1}')
    local region=$(echo "$i"|awk -F_ '{print $2}')
    echo -en "$(/bin/date "+%H:%M:%S") http: "
    $curl_cmd -H "Host: $url" "http://$ip/$location"|grep -a -q "$key"
    if [[ $? -eq 0 ]];then
      local tag=$(($tag + 1))
      echo -en "ok"
    else
      echo -en "-->> no <<--"
      local flag=$(($flag + 1))
    fi
    echo -en "; https: "
    $curl_cmd --insecure -H "Host: $url" "https://$ip/$location"|grep -a -q "$key"
    if [[ $? -eq 0 ]];then
      local tag=$(($tag + 1))
      echo -en "ok"
    else
      echo -en "-->> no <<--"
      local flag=$(($flag + 1))
    fi
    echo "; $url $ip $region"
    [[ $flag -ne 0 ]] && echo -en "$curl_cmd -H \"Host: $url\" \"http://$ip/$location\"\n$curl_cmd --insecure -H \"Host: $url\" \"https://$ip/$location\"\n"
    [[ $tag -eq 2 ]] && local ok_total=$(($ok_total + 1))
  done
  echo "total: $(cat $ip_list_file|wc -l) ok: $ok_total"
}

if [[ $1 == "-h" || $1 == "--help" || -z $1 ]];then
  echo "    Usage: $0 [list_file] [url] [location] [response key string] [0|1]"
  echo "        [list_file] - exam:"
  echo "          120.163.x.x_comment"
  echo "          113.200.x.x_comment-str1.str2"
  echo "          ..."
  echo "        [url] - exam: v.bw-y.com"
  echo "        [location] - exam: sky?_t=i"
  echo "        [response key string] - exam: GIF"
  echo "        [0|1] - 0: use post by random str , 1: not use post action"
  echo "    Exam:"
  echo "      $0 ./guest.list v.bw-y.com soft content 1"
  echo "      $0 ./guest.list bw-y.com sky?_t=i GIF 1"
  echo "      $0 ./adv.list t.bw-y.com.cn sky?_t=i GIF 0"
  echo "      $0 ./monkey.list t.bw-y.com sky?_t=i GIF 0"
  exit 0
fi

check_url_set_out_put $1 $2 $3 $4 $5 

