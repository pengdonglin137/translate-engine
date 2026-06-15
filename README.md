# Translate Engine

通用翻译项目框架，提供翻译工具、流程规范和 CI/CD 模板。

## 特性

- 🔧 **通用工具**: 术语检查、进度统计、质量评估
- 📋 **规范模板**: 技术文档、学术论文、文学作品翻译规范
- 🔄 **CI/CD**: GitHub Actions 自动构建和质量门禁
- 🌍 **多语言**: 支持任意目标语言
- 📄 **多格式**: LaTeX, Markdown, Word, reStructuredText

## 快速开始

### 1. 初始化翻译项目

```bash
# 克隆引擎
git clone https://github.com/your-org/translate-engine.git

# 创建翻译项目（使用模板）
mkdir my-project-cn && cd my-project-cn
git init
git submodule add ../translate-engine .translate-engine

# 复制模板
cp .translate-engine/templates/config.yaml .
cp .translate-engine/templates/CLAUDE.md .
```

### 2. 配置项目

编辑 `config.yaml`，设置原文源、目标语言、文件格式等。

### 3. 开始翻译

```bash
# 检查术语一致性
python .translate-engine/scripts/check_terms.py

# 查看翻译进度
python .translate-engine/scripts/check_progress.py
```

## 项目结构

```
translate-engine/
├── scripts/              # 工具脚本
├── conventions/          # 翻译规范
├── workflows/            # GitHub Actions 模板
├── templates/            # 项目模板
└── plugins/              # 格式处理插件
```

## 作为 Submodule 使用

```bash
# 在翻译项目中添加引擎
git submodule add https://github.com/your-org/translate-engine.git .translate-engine
```
