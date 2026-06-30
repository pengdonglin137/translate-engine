# Linux Kernel - 系统调用接口

## 系统调用概述
- 用户空间到内核空间的桥梁
- 提供操作系统服务的编程接口
- 通过软中断（int 0x80）或sysenter/syscall指令进入

## 常用系统调用
- 文件操作：open, read, write, close
- 进程控制：fork, exec, exit, wait
- 内存管理：mmap, brk, mprotect
- 网络：socket, bind, listen, accept, connect

## 系统调用号
- 每个系统调用有唯一编号
- 通过eax寄存器传递
- 参数通过ebx, ecx, edx, esi, edi传递

## VDSO（虚拟动态共享对象）
- 优化的系统调用路径
- 避免完整的上下文切换
- 用于gettimeofday等高频调用

## seccomp
- 系统调用过滤
- 限制进程可用的系统调用
- 提高安全性
