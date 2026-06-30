# Linux Kernel - 进程创建

## 历史背景
- 传统UNIX使用fork/exec模型
- fork创建进程副本，exec加载新程序
- 传统fork效率低，需复制整个地址空间
- Linux从2.0开始使用写时复制（COW）机制
- 2.2版本实现线程支持，fork性能大幅提升

## vfork()
- 与fork不同，vfork不会复制页表
- 保证子进程先运行
- 父进程阻塞直到子进程调用exec或退出
- 现代Linux中vfork通过克隆标志实现

## clone()
- 最通用的进程/线程创建机制
- 通过flags参数控制共享哪些资源
- 主要clone标志：
  - CLONE_VM：共享地址空间
  - CLONE_FS：共享文件系统信息
  - CLONE_FILES：共享文件描述符表
  - CLONE_SIGHAND：共享信号处理
  - CLONE_THREAD：共享线程组

## 写时复制（COW）
- fork后父子进程共享物理页
- 当任一方修改页面时，内核创建副本
- 大幅减少fork的内存开销

## 进程终止
- exit()系统调用触发
- 释放资源，通知父进程
- 父进程通过wait()回收子进程
- 僵尸进程：子进程退出但父进程未回收
