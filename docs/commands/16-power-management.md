# Linux Kernel - 电源管理

## 概述
- Linux内核支持多种电源管理功能
- 延长电池寿命，降低功耗
- 适用于笔记本电脑、服务器、嵌入式设备

## CPU电源管理
- 空闲状态（C-states）：CPU空闲时降低功耗
- 频率缩放（P-states）：动态调整CPU频率
- 热管理：温度监控和降频

## 设备电源管理
- 电源挂起（suspend）：系统挂起到内存
- 休眠（hibernate）：系统休眠到磁盘
- 运行时电源管理：设备级功耗控制

## 节能技术
- CPU空闲驱动
- 设备运行时PM
- 时钟门控
- 电压调节

## 监控工具
- powertop：功耗分析
- turbostat：CPU频率和C-state监控
- /sys/devices/system/cpu/：CPU电源信息
