# Linux Kernel - 内核参数

## 概述
- 内核参数控制Linux内核的行为
- 可在启动时通过引导加载程序传递
- 运行时可通过/proc/sys或sysctl修改

## 参数来源
- 引导加载程序（GRUB）
- /proc/cmdline：当前启动参数
- /proc/sys/：运行时可修改参数
- /etc/sysctl.conf：持久化配置

## 常用参数
- `init=`：指定init进程
- `root=`：指定根文件系统
- `ro`：只读挂载根文件系统
- `quiet`：减少启动日志

## 运行时修改
```bash
# 查看参数
sysctl -a

# 修改参数
sysctl -w net.ipv4.ip_forward=1

# 持久化
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p
```

## 性能调优参数
- `vm.swappiness`：交换空间使用倾向
- `net.core.somaxconn`：最大连接队列
- `fs.file-max`：最大文件描述符数
