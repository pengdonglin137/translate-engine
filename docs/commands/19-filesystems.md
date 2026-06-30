# Linux Kernel - 文件系统

## 概述
- Linux支持多种文件系统
- 虚拟文件系统（VFS）提供统一接口
- 支持本地和网络文件系统

## 常见文件系统
- ext4：默认Linux文件系统
- XFS：高性能大文件系统
- Btrfs：快照和压缩
- tmpfs：内存文件系统

## 虚拟文件系统（VFS）
- 统一的文件系统接口
- inode、dentry、superblock抽象
- 支持多种后端实现

## 特殊文件系统
- /proc：进程信息
- /sys：设备信息
- /dev：设备节点
- cgroupfs：cgroup接口

## 网络文件系统
- NFS：网络文件系统
- CIFS/SMB：Windows文件共享
- 9P：轻量级网络文件系统
