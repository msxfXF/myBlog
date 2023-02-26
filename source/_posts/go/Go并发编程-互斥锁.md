---
title: Go并发编程-基本并发原语
tags: Go
categories:
  - go
date: 2022-10-27 09:31:26
---
## 学习路线

### 学习Go并发编程可能遇到的困难

1. 在面对并发难题时，感觉无从下手，不知道该用什么并发原语来解决问题。 
2. 如果多个并发原语都可以解决问题，那么，究竟哪个是最优解呢？比如说是用互斥锁，还是用 Channel。
3. 不知道如何编排并发任务。并发编程不像是传统的串行编程，程序的运行存在着很大的不确定性。这个时候，就会面临一个问题，怎么才能让相应的任务按照你设想的流程运行呢？
4. 有时候，按照正常理解的并发方式去实现的程序，结果莫名其妙就panic或者死锁了，排查起来非常困难。
5. 已知的并发原语都不能解决并发问题，程序写起来异常复杂，而且代码混乱，容易出错。

### Go并发编程的两条主线————知识主线和学习主线
![](Go并发编程-基本并发原语/2022-10-27-09-32-15.png)

- 基本并发原语: Mutex、RWMutex、Waitgroup、Cond、 Pool、Context 等标准库中的并发原语。
- 原子操作: 原子操作是其它并发原语的基础，主要是Go标准库提供的原子操作。
- Channel: 基本用法和处理场景。
- 扩展并发原语: 信号量、SingleFlight、循环栅栏、ErrGroup。
- 分布式并发原语: Leader选举、分布式互斥锁、分布式读写锁、分布式队列

## Mutex

### 互斥锁的实现机制

在并发编程中，如果程序中的一部分会被**并发访问或修改**，为了避免并发访问导致的意想不到的结果，这部分程序需要被保护起来，这部分被保护起来的程序，就叫做**临界区**。

临界区就是一个**被共享的资源**，或者说是一个整体的一组共享资源，比如对数据库的访问、对某一个共享数据结构的操作、对一个 I/O 设备的使用、对一个连接池中的连接的调用。

使用互斥锁，限定临界区只能同时由一个线程持有，其它线程如果想进入这个临界区就会返回失败，或者是等待持有线程退出。因此，很好地解决了资源竞争问题。

**同步原语的适用场景**

- 共享资源。并发地读写共享资源，会出现数据竞争（data race）的问题，所以需要Mutex、RWMutex这样的并发原语来保护。
- 任务编排。需要goroutine按照一定的规律执行，而goroutine之间有相互等待或者依赖的顺序关系，我们常常使用WaitGroup或者Channel来实现。
- 消息传递。信息交流以及不同的goroutine之间的线程安全的数据交流，常常使用Channel来实现。

### Mutex 的基本使用方法
Mutex实现了package sync提供的Locker接口，进入临界区之前调用Lock方法，退出临界区的时候调用Unlock方法。
``` golang
type Locker interface {
    Lock()
    Unlock()
}
```
``` golang
func(m *Mutex)Lock()
func(m *Mutex)Unlock()
```

当一个goroutine通过调用Lock方法获得了这个锁的拥有权后，其它请求锁的goroutine就会**阻塞**在Lock方法的调用上，直到锁被释放并且自己获取到了这个锁的拥有权。

### Race detection
Go race detector是基于Google的C/C++ sanitizers技术实现的，编译器通过在内存访问时插桩来监控读写操作，定位对共享变量的非同步访问并打印警告。

用法：在编译（compile）、测试（test）或者运行（run）Go代码的时候，加上race参数。

``` golang
package main

import (
	"fmt"
	"sync"
)

func main() {
	var count = 0
	// 使用WaitGroup等待10个goroutine完成
	var wg sync.WaitGroup
	wg.Add(10)
	for i := 0; i < 10; i++ {
		go func() {
			defer wg.Done()
			for j := 0; j < 100000; j++ {
				count++
			}
		}()
	}
	// 等待10个goroutine完成
	wg.Wait()
	fmt.Println(count)
}
```
``` bash
go run -race counter.go
```
![](Go并发编程-基本并发原语/2022-10-27-10-32-13.png)

生成汇编代码
```
go tool compile -S counter.go
```
![](Go并发编程-基本并发原语/2022-10-27-10-32-26.png)
(这里留个坑，虽然优化成了INCQ指令，但是由于多核CPU存中SMP的竞争。具体内容之后再看)
[指令集的原子操作](https://www.51cto.com/article/718443.html)

通过在改变变量前后增加`mu.Lock()`, `mu.Unlock()`即可消除竞争警告
![](Go并发编程-基本并发原语/2022-10-27-10-47-16.png)
**Mutex 的零值是还没有 goroutine 等待的未加锁的状态**

## Mutex的其它用法
**Mutex会嵌入到其它struct中使用**
``` golang
type Counter struct { 
    mu sync.Mutex
    Count uint64 
    }
```

**采用嵌入字段的方式**
``` golang
type Counter struct { 
    sync.Mutex
    Count uint64 
    }
```
**把获取锁、释放锁、计数加一的逻辑封装成一个方法**
代码略

### 饥饿模式和正常模式
![](Go并发编程-基本并发原语/2022-11-08-22-00-37.png)
Mutex 可能处于两种操作模式下：正常模式和饥饿模式。

正常模式下，waiter 都是进入先入先出队列，被唤醒的 waiter 并不会直接持有锁，而是要和新来的 goroutine 进行竞争。新来的goroutine有先天的优势，它们正在CPU中运行。所以，在高并发情况下，被唤醒的 waiter 可能获取不到锁，这时，它会被插入到队列的前面。如果 waiter 获取不到锁的时间超过阈值1毫秒，那么，就进入到了饥饿模式。

在饥饿模式下，Mutex 的拥有者将直接把锁交给队列最前面的 waiter。新来的 goroutine 不会尝试获取锁，即使看起来锁没有被持有，它也不会去抢，也不会 spin，它会乖乖地加入到等待队列的尾部。

两种情况的其中之一Mutex 转换成正常模式:
- 此waiter已经是队列中的最后一个waiter了，没有其它的等待锁的goroutine了。
- 此 waiter 的等待时间小于1毫秒。

饥饿模式是对公平性和性能的一种平衡，它避免了某些 goroutine 长时间的等待锁。

### Mutex 四种易错场景
- Lock/Unlock 不是成对出现
- Copy 已使用的 Mutex
	Package sync 的同步原语在使用后是不能复制的。在并发环境下，不知道要复制的 Mutex 状态是什么，因为状态时刻改变。
- 重入，Mutex不是可重入的锁。
	当一个线程获取锁时，如果没有其它线程拥有这个锁，那么，这个线程就成功获取到这个锁。之后，如果其它线程再请求这个锁，就会处于阻塞等待的状态。但是，如果拥有这把锁的线程再请求这把锁的话，不会阻塞，而是成功返回，叫可重入锁。
- 死锁
	死锁产生的必要条件：
	- 互斥：至少一个资源是被排他性独享的，其他线程必须处于等待状态，直到资源被释放。
	- 持有和等待：goroutine持有一个资源，并且还在请求其它goroutine持有的资源
	- 不可剥夺：资源只能由持有它的goroutine来释放。
	- 环路等待：一般来说，存在一组goroutine依次等待其它goroutine的资源，形成了一个环路等待的死结。
## 思维导图
![](Go并发编程-基本并发原语/2022-11-08-22-26-54.png)
## 其它资料
[sync.mutex 源代码分析](https://colobu.com/2018/12/18/dive-into-sync-mutex/)
[深入理解原子操作的本质](https://blog.fanscore.cn/p/2/)