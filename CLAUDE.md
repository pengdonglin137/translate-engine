# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

translate-engine 是一个通用翻译项目框架，提供翻译工具、流程规范和 CI/CD 模板。其他翻译项目通过 git submodule（路径 `.translate-engine`）引用本仓库。

## 依赖

所有脚本仅依赖 `pyyaml`：`pip install pyyaml`

## 架构

```
translate-engine/
├── scripts/                  # Python 翻译工具（详见下方）
├── conventions/
│   ├── terms/template.yaml   # 术语表 YAML 模板（含 keep_english/context_dependent 规则）
│   └── style/xinyada.md      # 信雅达翻译标准详细文档
├── plugins/                  # 格式处理插件（latex/markdown/word，待实现）
├── workflows/build.yml       # GitHub Actions CI 模板（质量检查 → PDF 构建 → Release）
└── templates/
    ├── config.yaml           # 项目配置模板（source.type 决定脚本行为）
    └── CLAUDE.md             # 消费方项目的 CLAUDE.md 模板
```

## 核心脚本

### check_terms.py — 术语一致性检查

扫描翻译文件，检测英文术语是否未被翻译。关键行为：
- 根据 `config.yaml` 的 `source.type`（latex/markdown/rst）自动选择文件扩展名和跳过规则
- **智能排除**：首次出现标注（`锁（lock）`）、LaTeX 命令参数、代码环境、注释、数学公式、词边界（`deadlock` 中的 `lock` 不报）
- `--strict` 模式启用更多检查
- 退出码 1 表示发现不一致

```bash
python scripts/check_terms.py --config config.yaml --terms terms.yaml [--verbose] [--strict]
```

### check_progress.py — 翻译进度统计

统计可翻译行中中文字符占比，输出进度条。`--format json|text|yaml` 切换输出格式。

```bash
python scripts/check_progress.py --config config.yaml [--format json]
```

### translation_memory.py — 翻译记忆

基于 JSON 文件（`.translate-memory.json`）的翻译记忆系统，支持模糊搜索（Jaccard 相似度）。

```bash
python scripts/translation_memory.py add --source "lock" --target "锁"
python scripts/translation_memory.py search --query "deadlock" [--threshold 0.3]
python scripts/translation_memory.py export --output tm.json
python scripts/translation_memory.py import --input tm.json
```

### translate.py — 工作流自动化

集成入口，依次调用 check_progress 和 check_terms。设计为从消费方项目根目录运行（路径硬编码 `.translate-engine/`）。

```bash
python scripts/translate.py init                    # 检查 submodule 就绪
python scripts/translate.py status                  # 进度 + 术语检查
python scripts/translate.py check [--build]         # 质量检查（--build 追加 make 1c）
python scripts/translate.py suggest "English text"  # 查翻译记忆
python scripts/translate.py record "EN" "CN"        # 记录翻译
```

## config.yaml 结构

`templates/config.yaml` 是消费方项目的配置模板。关键字段：
- `source.type`: 决定脚本扫描的文件扩展名和解析逻辑（latex → `*.tex`, markdown → `*.md`）
- `translation.target_language`: BCP 47 语言代码
- `build.targets` / `build.pdf_variants`: 构建目标（`make 1c` / `make` / `make a4`）

## 术语表规则

`conventions/terms/template.yaml` 定义了术语 YAML 格式：
- `rule: "translate"`（默认）：必须翻译，check_terms 会检查
- `rule: "keep_english"`：保留英文（如 RCU、CPU），check_terms 跳过
- `rule: "context_dependent"`：按上下文决定翻译

## 作为 Submodule 使用

```bash
git submodule add git@github.com:pengdonglin137/translate-engine.git .translate-engine
```

消费方项目复制 `templates/config.yaml` 和 `templates/CLAUDE.md` 到根目录，编辑 `config.yaml` 匹配项目实际配置。CI 时 checkout 此仓库到 `.translate-engine/` 路径。

## CI/CD

`workflows/build.yml` 模板定义三阶段流水线：
1. **quality**: 运行 check_terms + check_progress（continue-on-error）
2. **build**: 在 `akiyks/perfbook-build` 容器中构建 PDF 变体（perfbook.pdf / 1c / a4），输出 `*_cn.pdf`
3. **release**: 仅 tag 触发，创建 GitHub Release 附带 PDF
