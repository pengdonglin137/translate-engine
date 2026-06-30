# Linux Kernel Documentation - Memory Management (部分)
## 虚拟内存管理

文件列表:
- accounting/
- admin-guide/
- arm/
- sh/
- riscv/
- sv39x4/
- bootup.txt
- boulevard.txt
- concepts/
- controlling-memcg-gw.txt
- damon/
- design-page-alloc-debugging.rst
- fbcon.rst
- huge_kernelheap.rst
- index.rst
- initialization.rst
- kabi.rst
- memory-hotplug.rst
- multi_gen_lru.rst
- nommu-mmap.rst
- numa_memory_policy.rst
- overcommit-accounting.rst
- pagemap.rst
- profile.rst
- remove_dma_reservations.rst
- soft-dirty.txt
- swap_badness.rst
- swap_numa.rst
- sysctl/
- transmission.txt
- unevictable_lru.rst
- unshared_page.rst
- zswap.rst

# Linux Kernel - I/O 依赖

基于I/O的LRU页面生成（也称为跨设备LRU或xd-lru）是可选的，可以为具有可移动LRU页面的块设备启用。在启用时，页面在第一次映射时被添加到生成列表中，如果在写回过程中被修改，则被提升到下一个较旧的代。I/O依赖的提升会将写入同一文件的页面在LRU上的距离限制在一个页面大小以内。

# Linux Kernel - I/O 限制

# 限制设备I/O
# ==================
#
# 限制进程可以向设备发送的I/O带宽。
# 请参阅 Documentation/admin-guide/cgroup-v2.rst，了解有关此 cgroup 控制器的一般信息。

# 使用blk-iolatency cgroup控制文件
# ==================
#
# 文件
# ------
# /sys/fs/cgroup/<group>/io.latency
#
# io.latency的格式：
# target=<微秒>：设置延迟目标。
# 0：禁用此cgroup的目标。

# 没有直接方法从用户空间直接禁用cgroup控制器。可以将cgroup的io.latency值设置为0来停止此cgroup的节流。一旦节流开始，控制器会创建另一个子cgroup（.trim）以跟踪实际带宽。如果更改io.latency目标，.trim子cgroup将被删除并重新创建。

# 从磁盘IO到IO cgroup的映射不简单。一个设备可能同时受到多个不同cgroup的限制。IO延迟控制器必须考虑所有因素，包括其他IO控制器和物理设备限制，以确定合适的节流决策。

# 用户指南
# =========
#
# 如果您在系统上有多个cgroup处于活动状态，请将io.latency设置为一个目标值。

# 以下是示例：
# 系统有一个后台备份job，一个数据库，一个web服务器。
# 数据库是最重要的，web服务器次之。备份应以低于web服务器的优先级运行。
#
# cgroup层次结构如下所示：
#
#       root
#      /    \
#   db      web
#           |
#           backup
#
# $ cat /sys/fs/cgroup/io.latency
# target=0
#
# # 数据库是关键任务
# $ echo "target=10000" > /sys/fs/cgroup/db/io.latency
#
# # web服务器是次关键的
# $ echo "target=75000" > /sys/fs/cgroup/web/io.latency
#
# # 备份是次重要的
# $ echo "target=100000" > /sys/fs/cgroup/web/backup/io.latency
#
# 现在数据库将获得至少10毫秒的延迟，web服务器获得至少75毫秒，备份获得至少100毫秒。如果数据库工作负载超过其分配，备份将节流，使数据库获得更大的份额。

# 重要：延迟值是存储设备本身的延迟，而不是进程的端到端延迟。
# 目标值0表示不进行节流，目标值100000（100ms）表示相当温和的限制。
# 如果需要，这些值可以相当激进，但请注意，如果您将延迟值设置得非常低，可能导致系统不稳定。
