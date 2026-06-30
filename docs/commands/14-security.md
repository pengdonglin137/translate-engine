# Linux Kernel - 安全机制

## 概述
- Linux内核提供多层安全机制
- 从访问控制到强制安全策略
- SELinux、AppArmor、Yama等

## 访问控制
- DAC（自主访问控制）：传统UNIX权限
- MAC（强制访问控制）：SELinux、AppArmor
- 能力（Capabilities）：细粒度权限

## SELinux
- 强制访问控制框架
- 基于安全上下文的策略
- 类型强制（Type Enforcement）
- 常用于Fedora、RHEL

## AppArmor
- 基于路径的访问控制
- 更简单的策略语言
- 常用于Ubuntu、Debian

## Yama
- ptrace保护
- 软链接保护
- /proc/PID/访问控制

## seccomp
- 系统调用过滤
- 限制进程可用的系统调用
- 沙箱化应用
