# Linux Kernel - 调度器

## 概述
- 进程调度器决定CPU时间分配
- 目标：公平性、低延迟、高吞吐量
- CFS是默认调度器

## 调度器类型
- O(1)调度器：早期Linux
- CFS（完全公平调度器）：当前默认
- 实时调度器：SCHED_FIFO、SCHED_RR

## CFS调度器
- 基于虚拟运行时间
- 红黑树管理可运行进程
- 按权重分配CPU时间
- 支持cgroup分组

## 调度策略
- SCHED_NORMAL：普通进程
- SCHED_BATCH：批处理进程
- SCHED_IDLE：低优先级
- SCHED_FIFO：实时先入先出
- SCHED_RR：实时轮转

## 亲和性
- 进程亲和性：绑定到特定CPU
- CPU亲和性掩码
- NUMA感知调度

## 调度延迟
- 目标延迟：进程等待时间上限
- 最小粒度：最小运行时间片
