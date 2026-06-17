# CLAUDE.md

本文件为 Claude Code 提供翻译项目的工作指引。

## 项目概述

这是一个 AI 翻译项目，使用 translate-engine 进行全自动翻译。

## 使用 translate-engine

```bash
# 从 translate-engine 根目录运行
python scripts/translate.py --project <项目名> check    # 术语检查
python scripts/translate.py --project <项目名> build    # 构建 PDF
```

## 翻译规范

翻译时遵循以下规则（按优先级）：

1. **术语表** (`terms.yaml`) — 最高优先级
2. **领域规则** — 技术/学术/文学（由 config.yaml `domains` 字段指定）
3. **全局规则** (`conventions/rules/global.md`) — 基础规则

### 信雅达标准
- **信**: 忠实原文含义，不误译不遗漏
- **雅**: 避免翻译腔，使用自然中文
- **达**: 清晰易懂，逻辑通顺

### 术语处理
- 首次出现：`中文（English）` 格式
- 后续出现：只用中文
- keep_english 术语保留英文
- 同一术语全文统一

### LaTeX 规则
- 翻译：散文段落、标题、图表标题
- 保留：`\label{}`、`\cite{}`、代码环境、数学公式

### Markdown 规则
- 翻译：正文、标题
- 保留：代码块、链接

## 构建

```bash
make 1c        # 单栏
make           # 双栏
make a4        # A4 纸张
```

## 常见问题

### Q: 如何添加新术语？
A: 编辑 `terms.yaml`，添加术语映射。

### Q: 翻译构建失败怎么办？
A: 检查 LaTeX 语法错误，通常是括号不匹配或命令拼写错误。
