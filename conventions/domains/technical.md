# 技术文档翻译规则

适用于技术手册、API 文档、编程指南、系统架构文档等。

## 翻译原则

- 准确性优先：技术概念必须精确传达
- 一致性优先：同一术语全文统一
- 可读性：让读者能根据译文理解技术细节

## 格式处理

### LaTeX
- **翻译**: 散文段落、标题、图表标题
- **保留**: `\label{}`、`\cite{}`、`\cref{}`、`\co{}`、代码环境、数学公式、索引命令
- **注意**: 不要破坏 LaTeX 语法，不要翻译宏定义

### Markdown
- **翻译**: 正文、标题
- **保留**: 代码块、链接 URL、图片

### Word
- **翻译**: 正文、标题、表格内容
- **保留**: 域代码、交叉引用、目录

## 术语处理

- 代码中的标识符不翻译（变量名、函数名、类名）
- 命令行命令不翻译
- 配置文件内容不翻译
- 错误信息保留英文，可加中文注释

## 常见技术术语翻译参考

| 英文 | 中文 | 说明 |
|------|------|------|
| API | API | 保留英文 |
| SDK | SDK | 保留英文 |
| framework | 框架 | |
| library | 库 | |
| dependency | 依赖 | |
| repository | 仓库 | |
| commit | 提交 | |
| branch | 分支 | |
| merge | 合并 | |
| deploy | 部署 | |
| pipeline | 流水线 | |
| container | 容器 | |
| virtual machine | 虚拟机 | |
| thread | 线程 | |
| process | 进程 | |
| memory | 内存 | |
| buffer | 缓冲区 | |
| cache | 缓存 | |
| deadlock | 死锁 | |
| race condition | 竞态条件 | |
| exception | 异常 | |
| callback | 回调 | |
| middleware | 中间件 | |
