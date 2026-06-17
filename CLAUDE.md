# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

translate-engine 是 AI 翻译的质量保障工具。自动检测项目类型、加载分层规则、一键完成翻译全流程。

## 架构

```
translate-engine/
├── scripts/
│   ├── check_terms.py              # 术语一致性检查
│   └── translate.py                # 工作流工具（list/init/analyze/check/build/all）
├── conventions/
│   ├── rules/global.md             # 全局翻译规则（所有项目必须遵守）
│   ├── domains/                    # 领域规则（按类型加载）
│   │   ├── technical.md            #   技术文档
│   │   ├── academic.md             #   学术论文
│   │   └── literary.md             #   文学翻译
│   ├── terms/template.yaml         # 术语表模板
│   └── style/xinyada.md            # 信雅达标准详解
├── projects/                       # 翻译项目（submodule）
│   └── perfbook/
├── templates/                      # 新项目模板
│   ├── config.yaml
│   ├── CLAUDE.md
│   └── terms/template.yaml
├── .claude/commands/               # Claude Code 命令
│   ├── translate.md                #   /translate — 全自动翻译
│   ├── init-project.md             #   /init-project — 分析项目生成配置
│   ├── check-terms.md              #   /check-terms — 术语检查+修复
│   └── build.md                    #   /build — 构建 PDF
├── .github/workflows/              # 引擎 CI
├── work/                           # 临时工作区（.gitignore）
└── workflows/build.yml             # 消费方项目 CI 模板
```

## Claude Code 命令

在 Claude Code 中输入以下命令，零干预完成翻译：

| 命令 | 功能 |
|------|------|
| `/translate <project>` | 全自动翻译（检测配置→加载规则→翻译→术语修复→构建） |
| `/init-project <project>` | 分析项目结构，自动生成 config.yaml 和 terms.yaml |
| `/check-terms <project>` | 术语检查 + 自动修复 |
| `/build <project>` | 构建 PDF |

示例：
```
/translate perfbook              # 一键翻译整个项目
/init-project new-project        # 分析新项目并生成配置
/check-terms perfbook            # 术语检查并自动修复
/build perfbook                  # 构建 PDF
```

## 分层规则体系

翻译规则按三层叠加，后者覆盖前者：

```
项目 terms.yaml（最高优先级）
  ↑
领域规则（technical / academic / literary）
  ↑
全局规则 global.md（最低优先级）
```

### 全局规则（`conventions/rules/global.md`）
- 信雅达标准（信40% + 雅30% + 达30%）
- 翻译腔消除（被动→主动、的字堆叠、长句拆分、英文句式→中文）
- 术语一致性（首次标注、统一译法、keep_english）
- 质量评分（1-5分）

### 领域规则（`conventions/domains/`）

| 领域 | 适用场景 | 核心规则 |
|------|---------|---------|
| `technical` | 技术手册、API 文档、编程指南 | 代码不翻译、配置不翻译、技术术语参考表 |
| `academic` | 学术论文、研究报告 | 引用不翻译、学术术语标准译法 |
| `literary` | 小说、散文、诗歌 | 风格再现、文化适配、保留修辞 |

### 项目规则
- `config.yaml` 中的 `domains` 字段指定加载哪些领域规则
- `terms.yaml` 中的术语映射是最终权威

### 自动检测
`/translate` 和 `/init-project` 会自动检测项目领域：
- 代码示例、API → `technical`
- 摘要、参考文献 → `academic`
- 叙事、对话 → `literary`

## config.yaml

每个项目需要 `config.yaml`。**不需要手动创建** — `/translate` 会自动生成。

自动检测的内容：
- `source.type`：从文件扩展名（.tex/.md/.docx）
- `build.command`：从 Makefile/CMake/CI 配置
- `translation.engine`：从 LaTeX 包（xeCJK/ctex → xelatex）
- `domains`：从文件内容（代码/学术/文学特征）
- `upstream`：从 git remote
- `branch`：从远程分支

用户只需填写 `title_translated`（翻译标题）。

## 命令行工具

```bash
python scripts/translate.py list                          # 列出项目
python scripts/translate.py init <name>                   # 创建新项目
python scripts/translate.py analyze <name>                # 分析项目生成配置
python scripts/translate.py --project <name> check        # 术语检查
python scripts/translate.py --project <name> build        # 构建 PDF
python scripts/translate.py --project <name> all          # 检查+构建
python scripts/check_terms.py --project <name> [--verbose] # 术语检查（直接调用）
```

`--project` 参数：项目名（自动查找 `projects/<name>`）、相对路径、或绝对路径。

## 添加翻译项目

```bash
git submodule add <repo-url> projects/<name>
```

然后运行 `/translate <name>` — 自动分析、生成配置、开始翻译。

## CI/CD

- `.github/workflows/test.yml`：引擎自身测试
- `.github/workflows/quality.yml`：对 projects/ 下所有项目运行术语检查
- `workflows/build.yml`：消费方项目的 CI 模板
