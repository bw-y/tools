# 个人小工具

#### Table of Contents

1. [特定文件清理](#特定文件清理)
2. [检查目录内容是否有变更](#检查目录内容是否有变更)
3. [ftp操作脚本](#ftp操作脚本)
4. [获取日期范围脚本](#获取日期范围脚本)
5. [监控nginx和upstream的延迟的nagios脚本](#nginx/upstream监控脚本)

## 特定文件清理

### `clean_files.py`

* 清理指定目录下,文件名中包含日期格式(例:`201510091058`)的文件; 
* 脚本接收最多三个有效参数
* 参数1: 文件所在目录的绝对路径
* 参数2: 保留的天数/分钟,有效值为整形数字
* 参数3: 指定参数2的单位是天还是分钟,此参数不传递时,默认为天

```
帮助信息:
# ./clean_files.py 
Usage: ./clean_files.py /path/dir 10 [-m|-d]
  -m minutes
  -d days [default]

例1: 清理/opt/logs目录下的5天前的文件
# ./clean_files.py /opt/logs 5 

例2: 清理/opt/logs目录下600分钟前的文件
# ./clean_files.py /opt/logs 600 -m
```

## 检查目录内容是否有变更

### `check_rsync_stat.py`

* 脚本接收两个参数, 参数1: 目录 , 参数2: 分钟
* 脚本有个内置可选配置文件, 用于管理部分时间可以不检查
* 内置配置文件路径(此文件可以不存在)`/etc/check_rsync_invalid.ini`

```
例1: 常规检查两个目录的内容30分钟内是否有变更:
# ./check_rsync_stat.py /var/log/ 30
rsync OK in 30 minute

# ./check_rsync_stat.py /opt 30
Too long time no synchronization 

############
例2: 检查三个目录,其中两个有忽略时间规则
# cat /etc/check_rsync_invalid.ini 
/var/log 0-6,21-23
/opt 0,4,6,20-23

# ./check_rsync_stat.py /etc 30
rsync OK in 30 minute

# ./check_rsync_stat.py /opt 30
No check: /opt, Now Hour: 00, Ignore list: ['00', '04', '06', '20', '21', '22']

# ./check_rsync_stat.py /var/log 30
No check: /var/log, Now Hour: 00, Ignore list: ['00', '01', '02', '03', '04', '05', '21', '22']
```

## ftp操作脚本

### `ftp_op.sh`

* 脚本支持lftp命令行内的所有操作,直接以参数的形式传递即可
* 需要在脚本内需要预先填写ftp对应的类型/用户/密码/主机等信息

```
例1: 同步本地目的/local/dir1到ftp目录/ftp/dir2:
# /opt/ftp_op/ftp_op.sh mirror -R /local/dir1/ /ftp/dir2/
```

## 获取日期范围脚本 

### `date_range.sh`

* 脚本需要两个日期参数
* 第一个日期参数必须早于第二个参数

```
例1:
# ./date_range.sh 20150228 20150302
20150228
20150301
20150302
```

## nginx/upstream监控脚本

### `check_nginx_timeout.py`

* 此脚本仅用于nagios被动监控场景
* 此脚本需要部署在nginx所在节点
* 此脚本需要读取一个指定格式得nginx日志文件,其ngx的log_format为: `$request_time $upstream_addr`
* 此脚本需要知道ngx的pid路径,默认路径为`/var/run/nginx.pid`
* ngx日志文件在每次被检查后,会被清理,脚本会控制ngx重新记录一个新文件.
* nagios server端地址,直接修改倒数第二行中的IP即可.

```
例子1: 
    大于0.1s的比例低于1%时OK; 超过1%时WARN; 超过2%时critical;
    nagios的监控服务为chk_ngx_timeout; ngx的pid为/var/run/nginx.pid;
    修改脚本文件最后倒数第二行为如下;
# vim check_nginx_timeout.py 
    obj = Base("/var/log/nginx/check_upsteam.log", trigger=0.1, warn=100, critical=200, tag="chk_ngx_timeout", nginx_pid_path="/var/run/nginx.pid")