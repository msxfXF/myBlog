---
title: 3.Go-micro微服务框架
tags:
  - 微服务
  - Golang
  - Go-micro
categories:
  - k8s
date: 2022-05-19 15:23:59
---
## gRPC
- RPC代指远程过程调用(Remote Procedure Call)
- 包含了传输协议和编码(对象序列号)协议
- 允许运行于一台计算机的程序调用另- -台计算机的子程序.


- 使用RPC好处
    - 简单、通用、高效
### gRPC
- gRPC是一一个高性能、开源、通用的RPC框架
- 基于HTTP2.0协议标准设计开发
- 支持多语言，默认采用Protocol Buffers数据序列化协议
![](3-Go-micro微服务框架/2022-05-19-16-50-16.png)
![](3-Go-micro微服务框架/2022-05-19-16-51-12.png)

## ProtoBuf

### 什么是Protocol Buffers ?
- 是一种轻便高效的序列化结构化数据的协议
- 通常用在存储数据和需要远程数据通信的程序上
- 跨语言,更小、更快、也更简单
- 加速站点之间数据传输速度
- 解决数据传输不规范问题


## Docker使用Proto生成go文件