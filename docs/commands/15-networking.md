# Linux Kernel - 网络

## 概述
- Linux内核包含完整的TCP/IP协议栈
- 支持高性能网络编程
- socket API是主要编程接口

## 网络层次
- 应用层：HTTP、FTP、DNS等
- 传输层：TCP、UDP
- 网络层：IP、ICMP
- 链路层：以太网、WiFi

## socket类型
- SOCK_STREAM：TCP
- SOCK_DGRAM：UDP
- SOCK_RAW：原始socket

## 高性能网络
- 多队列网卡（RSS）
- XDP（eXpress Data Path）
- io_uring异步I/O
- TCP BBR拥塞控制

## 网络命名空间
- 容器网络隔离
- veth对连接命名空间
- 桥接、NAT、路由

## 防火墙
- iptables：传统防火墙
- nftables：新一代防火墙
- eBPF：可编程网络过滤
