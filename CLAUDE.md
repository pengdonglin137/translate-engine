# CLAUDE.md

本文件为 Claude Code 提供 translate-engine 项目的工作指引。

## 项目概述

translate-engine 是一个通用翻译项目框架，提供翻译工具、流程规范和 CI/CD 模板。支持任意目标语言和多种文件格式（LaTeX、Markdown、Word、reStructuredText）。

## 架构

```
translate-engine/
├── scripts/              # 翻译工具脚本
│   ├── check_terms.py    # 术语一致性检查（改进版，误报减少89%）
│   ├── check_progress.py # 翻译进度统计
│   ├── translation_memory.py # 翻译记忆系统
│   └── translate.py      # 工作流自动化
├── conventions/          # 翻译规范
│   ├── terms/            # 术语表模板
│   └── style/            # 风格指南（信雅达标准）
├── workflows/            # GitHub Actions 模板
└── templates/            # 项目模板
```

## 工具使用

### 术语检查
```bash
python scripts/check_terms.py --config ../project/config.yaml --terms ../project/terms.yaml
```

### 进度统计
```bash
python scripts/check_progress.py --config ../project/config.yaml
```

### 翻译记忆
```bash
python scripts/translation_memory.py add --source "lock" --target "锁"
python scripts/translation_memory.py search --query "deadlock"
```

### 工作流自动化
```bash
python scripts/translate.py status    # 查看状态
python scripts/translate.py check     # 质量检查
python scripts/translate.py suggest "English text"  # 查询建议
```

## 翻译规范

### 信雅达标准
- **信** (Faithfulness): 忠实原文含义，不误译、不遗漏
- **雅** (Elegance): 避免翻译腔，使用自然流畅的中文
- **达** (Expressiveness): 清晰易懂，逻辑通顺

### 术语处理策略
- 可翻译术语：统一翻译（lock→锁, deadlock→死锁）
- 保留英文术语：技术惯用（RCU, grace period, CPU）
- 首次标注：中文（英文）格式

## 作为 Submodule 使用

其他翻译项目通过 git submodule 引用本仓库：

```bash
# 在翻译项目中添加
git submodule add https://github.com/pengdonglin137/translate-engine.git .translate-engine
```

## 贡献指南

- 新增脚本请添加到 `scripts/` 目录
- 新增规范请添加到 `conventions/` 目录
- 保持向后兼容
- 添加必要的错误处理
