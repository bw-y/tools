# 个人python小工具

#### Table of Contents

1. [特定文件清理](#特定文件清理)

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
