---
title: Dokcer中配置IDA
tags: Docker IDA
categories:
  - k8s
date: 2022-09-08 00:31:31
---

## 宿主机

开启xhost，允许docker连接
``` bash
sudo apt-get install x11-xserver-utils
xhost + 
```

## Docker
docker采用ubuntu 18.04作为原镜像，中间需要安装许多依赖包才能运行。

这时候，采用`apt-file search xxxx.so`可以更高效的定位依赖。
``` bash
   apt-get update
   export QT_DEBUG_PLUGINS=1
   export DISPLAY=unix:1
   apt-get install wget
   apt-get install libglib2.0-0
   apt-get install libfontconfig1
   apt-get install libxcb-icccm4
   apt-get install libxcb-image0
   apt-get install libxcb-keysyms1
   apt-get install libxcb-randr0
   apt-get install libxcb-render-util0
   apt-get install libxcb-shape0
   apt-get install libxcb-xfixes0
   apt-get install libxcb-xinerama0
   apt-get install libxcb-xkb1
   apt-get install libxkbcommon-x11-0
   apt-get install libdbus-1-3
   wget https://out7.hex-rays.com/files/idafree80_linux.run
   chmod +x idafree80_linux.run 
```

## Dockerfile
```Dockerfile
FROM ubuntu:18.04
RUN apt-get update
RUN export QT_DEBUG_PLUGINS=1 && export DISPLAY=unix:1
RUN apt-get install -y wget libglib2.0-0 libfontconfig1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xfixes0 libxcb-xinerama0 libxcb-xkb1 libxcb-xkb1 
libxkbcommon-x11-0 libdbus-1-3
RUN wget https://out7.hex-rays.com/files/idafree80_linux.run
RUN chmod +x ./idafree80_linux.run
ENTRYPOINT ["./idafree80_linux.run"]
``` 

