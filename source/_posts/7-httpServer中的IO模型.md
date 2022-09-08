---
title: 7.http Server中的IO模型
date: 2022-05-23 08:41:47
tags: 
- 云原生
categories:
- 云原生
---
## 阻塞IO模型

![](7-httpServer中的IO模型/2022-05-24-08-42-51.png)

## 非阻塞IO模型

多次轮询
![](7-httpServer中的IO模型/2022-05-24-08-43-09.png)

## IO多路复用

第一次返回可读，第二次正式读取
![](7-httpServer中的IO模型/2022-05-24-08-43-39.png)

## 异步IO

![](7-httpServer中的IO模型/2022-05-24-08-45-14.png)

## Linux epoll图解

一个rbt，一个rdlist

![](7-httpServer中的IO模型/2022-05-24-08-46-43.png)

## Go实现细节

- Go 语言将Goroutine与fd绑定
- 一个socket fd与一个协程绑定
- 当socket fd未就绪时，将对应协程设置为Gwaiting状态，将CPU时间片让给其他协程
- Go语言 runtime 调度器进行调度唤醒协程时，检查fd是否就绪，如果就绪则将协程置为Grunnable并加入执行队列
- 协程被调度后处理fd数据

![](7-httpServer中的IO模型/2022-05-24-08-52-12.png)