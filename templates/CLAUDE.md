# CLAUDE.md

本文件为 Claude Code 提供翻译项目的工作指引。

## 项目概述

这是一个翻译项目，使用 translate-engine 框架管理翻译流程。

## 工具使用

### 质量检查
```bash
# 术语一致性检查
python .translate-engine/scripts/check_terms.py

# 翻译进度统计
python .translate-engine/scripts/check_progress.py
```

### 构建
```bash
# 构建 PDF
make 1c        # 单栏
make           # 双栏
make a4        # A4 纸张
```

## 翻译规范

### 核心标准：信雅达
- **信** (Faithfulness): 忠实原文含义，不误译、不遗漏
- **雅** (Elegance): 避免翻译腔，使用自然流畅的中文
- **达** (Expressiveness): 清晰易懂，逻辑通顺

### 术语表
- 术语表位于 `terms.yaml`
- 翻译前先检查术语表
- 首次出现的术语加括号标注英文：`锁（lock）`

### 文件处理规则

**LaTeX 文件:**
- 翻译：散文段落、标题、图表标题、QuickQuiz
- 保留英文：`\label{}`、`\cite{}`、`\co{}`、代码环境

**Markdown 文件:**
- 翻译：正文、标题
- 保留英文：代码块、链接、图片

### 翻译方法

1. 读取 200-300 行原文
2. 逐段翻译
3. 使用 Edit 工具修改（不要用 Write 覆盖整个文件）
4. 保持 LaTeX/Markdown 语法正确
5. 翻译后验证构建

## 常见问题

### Q: 如何添加新术语？
A: 编辑 `terms.yaml`，添加术语映射。

### Q: 翻译构建失败怎么办？
A: 检查 LaTeX 语法错误，通常是括号不匹配或命令拼写错误。

### Q: 如何同步上游原文？
A: 使用 `git subtree pull` 或手动合并。
