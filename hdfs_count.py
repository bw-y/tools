#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import commands

def get_directory_info(webhdfs_url, hdfs_path):
    # 构建WebHDFS接口URL
    url = "{}/webhdfs/v1{}?op=GETCONTENTSUMMARY".format(webhdfs_url, hdfs_path)

    try:
        # 构建curl命令
        curl_command = "curl -s --negotiate -u : {}".format(url)

        # 使用commands模块执行curl命令并获取输出
        status, output = commands.getstatusoutput(curl_command)

        # 检查命令执行状态
        if status != 0:
            print("Error executing curl command.")
            print("Command output:", output)
            return 0, 0, 0

        # 解析JSON响应
        data = json.loads(output)

        # 检查是否包含有效的内容摘要信息
        if 'ContentSummary' in data:
            content_summary = data['ContentSummary']
            
            # 获取目录下文件的数量、平均文件大小和总占用空间
            file_count = content_summary.get('fileCount', 0)
            length = content_summary.get('length', 0)
            space_consumed = content_summary.get('spaceConsumed', 0)

            # 计算平均文件大小（仅计算单副本）
            avg_file_size = length / max(1, file_count)

            return file_count, avg_file_size, space_consumed

        else:
            return 0, 0, 0

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        print("JSON data:", output)
        return 0, 0, 0

def list_directory_info(webhdfs_url, hdfs_path):
    # 获取当前目录的文件数量、平均文件大小和总占用空间
    file_count, avg_file_size, space_consumed = get_directory_info(webhdfs_url, hdfs_path)

    # 获取当前目录的绝对路径
    current_absolute_path = hdfs_path if hdfs_path.endswith('/') else hdfs_path + '/'

    # 输出目录信息
    print("{} {} {} {}".format(file_count, avg_file_size, space_consumed, current_absolute_path))

    # 获取当前目录下的子目录列表
    subdirectories = []

    # 构建WebHDFS接口URL
    url = "{}/webhdfs/v1{}?op=LISTSTATUS".format(webhdfs_url, hdfs_path)

    try:
        # 构建curl命令
        curl_command = "curl -s --negotiate -u : {}".format(url)

        # 使用commands模块执行curl命令并获取输出
        status, output = commands.getstatusoutput(curl_command)

        # 检查命令执行状态
        if status == 0:
            # 解析JSON响应
            data = json.loads(output)

            # 检查是否包含有效目录信息
            if 'FileStatuses' in data and 'FileStatus' in data['FileStatuses']:
                file_statuses = data['FileStatuses']['FileStatus']

                # 遍历目录下的每个文件/目录
                for file_status in file_statuses:
                    # 检查是否为目录
                    if file_status['type'] == 'DIRECTORY':
                        subdirectory_path = current_absolute_path + file_status['pathSuffix']

                        # 递归处理每个子目录
                        list_directory_info(webhdfs_url, subdirectory_path)

        else:
            print("Error executing curl command.")
            print("Command output:", output)

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        print("JSON data:", output)


# 传入WebHDFS接口URL和要递归列出信息的HDFS路径
webhdfs_url = "http://node21.test.com:14000"
hdfs_path_to_list = sys.argv[1]

# 调用函数递归列出目录信息并输出
list_directory_info(webhdfs_url, hdfs_path_to_list)

