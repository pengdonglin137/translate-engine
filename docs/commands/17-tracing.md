# Linux Kernel - 追踪和调试

## 追踪机制
- ftrace：函数追踪器
- perf：性能分析工具
- eBPF：可编程追踪
- tracepoints：静态追踪点

## ftrace
- 内核函数调用追踪
- 可追踪调度、中断、系统调用
- /sys/kernel/debug/tracing/接口

## perf
- CPU性能监控单元（PMU）访问
- 硬件性能计数器
- 软件事件追踪
- 火焰图生成

## eBPF
- 可编程内核钩子
- 安全的沙箱执行
- 高性能网络和安全应用

## strace/ltrace
- 系统调用追踪（strace）
- 库函数追踪（ltrace）
- 调试和分析工具
