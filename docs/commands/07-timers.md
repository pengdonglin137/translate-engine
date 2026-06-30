# Linux Kernel - 定时器

## 时间子系统
- 系统时钟：基于硬件定时器中断
- 高精度定时器（hrtimer）：纳秒级精度
- 动态定时器：可设置到期时间

## 定时器类型
- 定时器（timer）：一次性或周期性触发
- hrtimer：高精度定时器，支持纳秒级
- posix timer：用户空间定时器接口

## 时间源
- TSC（Time Stamp Counter）：CPU时钟周期计数
- HPET：高精度事件定时器
- ACPI PM Timer：电源管理定时器

## 延迟和调度
- usleep：微秒级延迟
- msleep：毫秒级延迟
- ssleep：秒级延迟
- 内核调度器根据延迟选择最佳方法

## 时钟源框架
- 统一的时钟源抽象
- 支持多种硬件时钟
- 提供单调时钟和挂钟时间
