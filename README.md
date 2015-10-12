# 个人python小工具

#### Table of Contents

1. [特定文件清理](#特定文件清理)
2. [检查目录内容是否有变更](#检查目录内容是否有变更)

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
