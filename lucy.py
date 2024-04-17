#!/usr/bin/python3
import random
import datetime
import sys

def simulate_lottery(user_numbers):
    # 解析用户输入的号码
    user_blue_ball = int(user_numbers.pop())
    user_numbers = [int(num) for num in user_numbers]

    # 初始化计数变量
    count = 0
    weeks = 0
    years = 0
    last_output_year = 0

    # 循环模拟开奖
    while True:
        # 生成随机的双色球号码
        red_balls = random.sample(range(1, 34), 6)
        blue_ball = random.randint(1, 16)

        # 检查是否完全匹配
        if red_balls == user_numbers and blue_ball == user_blue_ball:
            break

        # 更新计数变量
        count += 1
        if count % 3 == 0:
            weeks += 1
        if weeks % 52 == 0:
            years += 1

        # 每隔100000年输出提示信息
        if years - last_output_year >= 100000:
            current_time = datetime.datetime.now()
            print(f"C:{count}, Y:{years}, {current_time.strftime('%Y/%m/%d %H:%M:%S')}, {user_numbers} + {user_blue_ball}, 未中奖.")
            last_output_year = years

    # 输出结果
    print(f"您的号码是: {user_numbers} + {user_blue_ball}")
    print(f"中奖需要 {count} 次模拟,相当于 {years} 年 {weeks%52} 周。")

# 运行模拟
if len(sys.argv) < 8:
    print("请提供6个红球号码和1个蓝球号码作为参数。")
else:
    simulate_lottery(sys.argv[1:])
