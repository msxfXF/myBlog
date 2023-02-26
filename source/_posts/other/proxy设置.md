---
title: proxy设置
categories:
  - other
date: 2023-01-20 12:24:56
tags:
---

适用于WSL

```bash
HOST_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{ print $2 }')
WSL_IP=$(hostname -I | awk '{print $1}')
PROXY_PORT=10810
PROXY_PORT2=10811

PROXY_HTTP="http://${HOST_IP}:${PROXY_PORT2}"
PROXY_SOCKS5="socks5://${HOST_IP}:${PROXY_PORT}"
export http_proxy="${PROXY_HTTP}"
export HTTP_PROXY="${PROXY_HTTP}"
export https_proxy="${PROXY_HTTP}"
export HTTPS_proxy="${PROXY_HTTP}"
export ALL_PROXY="${PROXY_SOCKS5}"
export all_proxy="${PROXY_SOCKS5}"

git config --global http.proxy ${PROXY_HTTP}
git config --global https.proxy ${PROXY_HTTP}
```