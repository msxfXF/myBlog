---
title: 3.浅学Goroutine
date: 2022-05-17 18:10:15
tags: 
- Golang
- 云原生
categories: 云原生
---
## 并发和并行
- 并发(concurrency)两个或多个事件在同一时间间隔发生
- 并行(parallellism)两个或者多个事件在同一时刻发生

## 进程 线程 协程
- 进程：
    - 分配系统**资源**（CPU 时间、内存等）基本单位
    - 有独立的内存空间，切换开销大
- 线程：进程的一个执行流，是 CPU **调度**并能独立运行的的基本单位
    - 同一进程中的多线程共享内存空间，线程切换代价小
    - 多线程通信方便
    - 从内核层面来看线程其实也是一种特殊的进程，它跟父进程共享了打开的文件和文件系统信息，共享了地址空间和信号处理函数
- 协程
    - Go 语言中的轻量级线程实现
    - Go遇到长时间执行或者进行系统调用时，会主动把当前 goroutine 的 CPU (P) 转让出去，让其他 goroutine 能被调度并执行，也就是 Golang 从**语言层面**支持了协程

## CSP并发模型
Communicating Sequential Process

- CSP
    - 描述两个独立的并发实体通过共享的通讯 channel 进行通信的并发模型。
- goroutine
    - 是一种轻量线程，它**不是操作系统的线程**，而是将一个操作系统线程分段使用，通过调度器实现协作式调度。
    - 是一种绿色线程，微线程，它与 Coroutine 协程也有区别，能够在发现堵塞后启动新的微线程。
- 通道 channel
    - 类似 Unix 的 Pipe，用于协程之间通讯和同步。
    - 协程之间虽然解耦，但是它们和 Channel 有着耦合

goroutine和coroutine的区别(是否是抢占式调度): 

[Is a Go goroutine a coroutine?](https://stackoverflow.com/questions/18058164/is-a-go-goroutine-a-coroutine)

## 线程和协程的差异
- 每个 goroutine (协程) 默认占用内存远比 Java 、C 的线程少
    - goroutine：2KB
    - 线程：8MB
- 线程/goroutine 切换开销方面，goroutine 远比线程小
    - 线程：涉及模式切换(从用户态切换到内核态)、16个寄存器、PC、SP...等寄存器的刷新
    - goroutine：只有三个寄存器的值修改 - PC / SP / DX.
- GOMAXPROCS
    - 控制并行线程数量

## 通道channel
- 基于 Channel 的通信是同步的
- 当缓冲区满时，数据的发送是阻塞的
- 通过 make 关键字创建通道时可定义缓冲区容量，默认缓冲区容量为 0
- 缓冲区为0时，相当于信号量用于同步和互斥
- 遍历通道缓冲区可以用**循环读取**或**for range**

```golang
ch := make(chan int, 10)
//方式一
go func() {
    for i := 0; i < 10; i++ {
        rand.Seed(time.Now().UnixNano())
        n := rand.Intn(10) // n will be between 0 and 10
        fmt.Println("putting: ", n)
        ch <- n
    }
    close(ch)
}()

//方式二
for v := range ch {
    fmt.Println("receiving: ", v)
}
```

### 单向通道
- 只发送通道
    - var sendOnly chan<- int
- 只接收通道
    - var readOnly <-chan int

在传参时候改变类型，或强制转换类型

```golang
var c = make(chan int)
go prod(c)
go consume(c)

func prod(ch chan<- int){
    for { ch <- 1 }
}
func consume(ch <-chan int) {
    for { <-ch }
}
```

### 关闭通道
- 通道无需每次关闭
- 关闭的作用是告诉接收者该通道再无新数据发送
- 只有发送方需要关闭通道
- 可以使用`defer close(ch)`

### select
- 当多个协程同时运行时，可通过 select 轮询多个通道
- 如果所有通道都阻塞则等待，如定义了 default 则执行 default
- 如多个通道就绪则**随机选择**

```golang
select {
    case v:= <- ch1:
        //...
    case v:= <- ch2:
        //...
    default:
        //...
}
```

## 定时器Timer
- time.Ticker 以指定的时间间隔重复的向通道** C **发送时间值
- 用**time.NewTimer()**创建定时器
```golang
timer := time.NewTimer(time.Second)

select {
    // check normal channel
    case <-ch:
        fmt.Println("received from ch")
    case <-timer.C:
        fmt.Println("timeout waiting from channel ch")
}
```

## **上下文 Context**
- 可用于超时、取消操作或者一些异常情况，往往需要进行抢占操作或者中断后续操作
- 可用于传递请求相关值，设置截止日期、同步信号的结构体

原型：
```golang
type Context interface {
    Deadline() (deadline time.Time, ok bool)
    Done() <-chan struct{}
    Err() error
    Value(key interface{}) interface{}
}
```
方法：

```golang
context.Background()
context.TODO()
context.WithDeadline()
context.WithValue()
context.WithCancel()
```

### 例子，使用Context停止子协程

```golang
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    go func(ctx context.Context) {
        for {
            select {
            case <-ctx.Done():
                return
            default:
                // do something
            }
        }
    }(ctx)
    time.Sleep(time.Second)
    cancel()
}
```

### 例子，使用Context传递key, value参数到子协程

```golang
func main() {
    ctx := context.Background()
    ctx = context.WithValue(ctx, "key", "value")
    go func(ctx context.Context) {
        if value := ctx.Value("key"); value != nil {
            fmt.Println("value:", value)
        }
    }(ctx)
    time.Sleep(time.Second)
}
```
ctx.Value(key)返回是interface{}类型，需要使用类型断言
