# Linux Kernel - 控制组（cgroups）

## 概述
- 控制组（cgroups）是Linux内核的资源管理机制
- 允许对进程组进行资源限制、优先级控制、资源统计
- 是容器技术（Docker、Kubernetes）的基础

## cgroups v1 vs v2
- v1：每个资源控制器独立层级
- v2：统一层级，更简洁
- 推荐使用v2

## 资源控制器
- cpu：CPU时间分配
- memory：内存使用限制
- blkio：块设备I/O限制
- cpuset：CPU和内存节点绑定
- pids：进程数量限制

## 使用方法
```bash
# 创建cgroup
mkdir /sys/fs/cgroup/mygroup

# 限制内存为100MB
echo 104857600 > /sys/fs/cgroup/mygroup/memory.max

# 将进程加入cgroup
echo $PID > /sys/fs/cgroup/mygroup/cgroup.procs
```

## 与容器的关系
- Docker使用cgroups隔离资源
- Kubernetes通过cgroups管理Pod资源
- systemd集成cgroups管理服务
