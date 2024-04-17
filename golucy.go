package main

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"time"
)

func simulateLottery(userNumbers []int) {
	// 解析用户输入的号码
	userBlueBall := userNumbers[len(userNumbers)-1]
	userNumbers = userNumbers[:len(userNumbers)-1]

	// 初始化计数变量
	count := 0
	weeks := 0
	years := 0
	lastOutputYear := 0

	// 循环模拟开奖
	for {
		// 生成随机的双色球号码
		redBalls := generateRandomBalls(6, 1, 34)
		blueBall := rand.Intn(16) + 1

		// 检查是否完全匹配
		if arrEqual(redBalls, userNumbers) && blueBall == userBlueBall {
			break
		}

		// 更新计数变量
		count++
		if count%3 == 0 {
			weeks++
		}
		if weeks%52 == 0 {
			years++
		}

		// 每隔100000年输出提示信息
		if years-lastOutputYear >= 100000 {
			currentTime := time.Now()
			fmt.Printf("C:%d, Y:%d, %s, %v + %d, 未中奖.\n", count, years, currentTime.Format("2006/01/02 15:04:05"), userNumbers, userBlueBall)
			lastOutputYear = years
		}
	}

	// 输出结果
	fmt.Printf("您的号码是: %v + %d\n", userNumbers, userBlueBall)
	fmt.Printf("中奖需要 %d 次模拟,相当于 %d 年 %d 周。\n", count, years, weeks%52)
}

func generateRandomBalls(count, min, max int) []int {
	balls := make([]int, count)
	for i := 0; i < count; i++ {
		balls[i] = rand.Intn(max-min+1) + min
	}
	return balls
}

func arrEqual(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i, v := range a {
		if v != b[i] {
			return false
		}
	}
	return true
}

func main() {
	// 设置随机种子
	rand.Seed(time.Now().UnixNano())
	// 检查命令行参数
	if len(os.Args) < 8 {
		fmt.Println("请提供6个红球号码和1个蓝球号码作为参数。")
		return
	}
	// 解析用户输入的号码
	userNumbers := make([]int, 0, 7)
	for i := 1; i < 8; i++ {
		num, err := strconv.Atoi(os.Args[i])
		if err != nil {
			fmt.Println("参数格式错误,请输入数字。")
			return
		}
		userNumbers = append(userNumbers, num)
	}
	// 运行模拟
	simulateLottery(userNumbers)
}
