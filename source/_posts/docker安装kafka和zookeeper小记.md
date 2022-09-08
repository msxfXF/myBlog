---
title: docker安装kafka和zookeeper小记
date: 2022-05-26 21:45:37
tags: 
- kafka
- zookeeper
categories: 杂记
---

## 背景
使用的是单机安装伪集群，一个zookeeper节点+3个kafka节点，另外使用kafka-map来管理kafka节点。

通过Bridge模式，用docker0虚拟网桥进行桥接。zookeeper和kafka均暴露端口出来，方便外网连接。

## zookeeper安装
```bash
docker run -d --name zookeeper -p 2181:2181 -t wurstmeister/zookeeper
```

## kafka安装
```bash
docker run -d --name kafka0 -p 9092:9092 -e KAFKA_BROKER_ID=0 -e KAFKA_ZOOKEEPER_CONNECT=43.138.39.80:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://43.138.39.80:9092 -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 -t wurstmeister/kafka

docker run -d --name kafka1 -p 9093:9093 -e KAFKA_BROKER_ID=1 -e KAFKA_ZOOKEEPER_CONNECT=43.138.39.80:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://43.138.39.80:9093 -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9093 -t wurstmeister/kafka

docker run -d --name kafka2 -p 9094:9094 -e KAFKA_BROKER_ID=2 -e KAFKA_ZOOKEEPER_CONNECT=43.138.39.80:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://43.138.39.80:9094 -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9094 -t wurstmeister/kafka
```

- -e KAFKA_BROKER_ID=0  在kafka集群中，每个kafka都有一个BROKER_ID来区分自己
- -e KAFKA_ZOOKEEPER_CONNECT=43.138.39.80:2181/kafka 配置zookeeper管理kafka的路径43.138.39.80:2181/kafka
- -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://43.138.39.80:9092  把kafka的地址端口注册给zookeeper，如果是远程访问要改成外网IP,类如Java程序访问出现无法连接。
- -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 配置kafka的监听端口
- -v /etc/localtime:/etc/localtime 容器时间同步虚拟机的时间

这里要配**物理机的IP**，不然外面连不上。

## 测试

创建话题
``` bash
kafka-topics.sh --create --zookeeper 43.138.39.80:2181 --replication-factor 3 --partitions 5 --topic test_topic
```
查看主题列表和详情
``` bash
kafka-topics.sh --list --zookeeper zookeeper:2181
kafka-topics.sh --describe --zookeeper 43.138.39.80:2181 --topic test_topic
```

消费者
```bash
docker exec -it kafka0 bash
cd /opt/kafka_2.xx-xxx/bin/
kafka-console-consumer.sh --bootstrap-server 43.138.39.80:9093 --topic test_topic --from-beginning
```

生产者
```bash
docker exec -it kafka1 bash
cd /opt/kafka_2.xx-xxx/bin/
./kafka-console-producer.sh --broker-list localhost:9092 --topic test_topic
```

## kafka-map

```bash
docker run -d -p 8088:8080 -v /opt/kafka-map/data:/usr/local/kafka-map/data -e DEFAULT_USERNAME=admin1 -e DEFAULT_PASSWORD=admin1 --name kafka-map --restart always dushixiang/kafka-map:latest
```

## 常见问题
- IP配错，导致外网无法访问
- 容器内配置和启动参数不符
- KAFKA_BROKER_ID重复，可以尝试重启zookeeper
