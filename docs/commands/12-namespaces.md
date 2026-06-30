# Linux Kernel - 命名空间

## 概述
- 命名空间是Linux内核的隔离机制
- 为进程提供独立的系统资源视图
- 是容器技术的基础

## 命名空间类型
- PID：进程ID隔离
- NET：网络栈隔离
- MNT：挂载点隔离
- UTS：主机名隔离
- IPC：进程间通信隔离
- USER：用户和组ID隔离
- Cgroup：cgroup根目录隔离

## 使用方法
```bash
# 创建新命名空间
unshare --pid --fork /bin/bash

# 查看进程的命名空间
ls -la /proc/$PID/ns/

# 使用nsenter进入其他进程的命名空间
nsenter -t $PID -p -m -n
```

## 与容器的关系
- 容器使用命名空间隔离进程视图
- 结合cgroups实现完整隔离
- Docker和Kubernetes都依赖命名空间

## 性能影响
- 命名空间本身开销很小
- 主要开销来自资源隔离
- 网络命名空间可能有性能损失
