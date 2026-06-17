# Translate Engine

AI 翻译的质量保障工具。自动检测项目类型、加载分层规则、一键完成翻译全流程。

## 快速开始

```bash
git clone https://github.com/pengdonglin137/translate-engine.git
cd translate-engine
pip install pyyaml

# 添加翻译项目
git submodule add git@github.com:user/repo.git projects/my-project

# 一键翻译（自动检测配置、加载规则、翻译、术语检查、构建）
# 在 Claude Code 中输入：
/translate my-project
```

## 核心特性

- **全自动翻译**：一键完成，零干预
- **自动配置**：分析项目结构，自动生成 config.yaml 和 terms.yaml
- **分层规则**：全局规则 → 领域规则 → 项目术语，逐层叠加
- **领域检测**：自动识别技术文档/学术论文/文学作品
- **术语保障**：自动检查术语一致性，发现问题自动修复
- **构建验证**：翻译后自动构建 PDF，验证 LaTeX 语法

## Claude Code 命令

| 命令 | 功能 |
|------|------|
| `/translate <project>` | 全自动翻译 |
| `/init-project <project>` | 分析项目并生成配置 |
| `/check-terms <project>` | 术语检查 + 自动修复 |
| `/build <project>` | 构建 PDF |

## 命令行

```bash
python scripts/translate.py list                        # 列出项目
python scripts/translate.py init <name>                 # 创建新项目
python scripts/translate.py analyze <name>              # 分析项目生成配置
python scripts/translate.py --project <name> check      # 术语检查
python scripts/translate.py --project <name> build      # 构建 PDF
python scripts/translate.py --project <name> all        # 检查+构建
```

## 分层规则体系

```
项目 terms.yaml（最高优先级）
  ↑
领域规则（technical / academic / literary）
  ↑
全局规则 global.md（最低优先级）
```

### 全局规则
信雅达标准、翻译腔消除、术语一致性、质量评分。

### 领域规则

| 领域 | 场景 | 核心规则 |
|------|------|---------|
| `technical` | 技术手册、API、编程指南 | 代码不翻译、技术术语参考 |
| `academic` | 论文、研究报告 | 引用不翻译、学术术语标准译法 |
| `literary` | 小说、散文、诗歌 | 风格再现、文化适配 |

规则文件位于 `conventions/rules/`、`conventions/domains/`、`conventions/style/`。

## 项目配置

每个项目需要 `config.yaml`。**不需要手动创建** — `/translate` 会自动生成。

自动检测：文件类型、构建系统、LaTeX 引擎、领域类型、Git 信息。

## 架构

```
translate-engine/
├── scripts/                  # 翻译工具
├── conventions/              # 分层翻译规则
│   ├── rules/global.md       #   全局规则
│   ├── domains/              #   领域规则
│   │   ├── technical.md
│   │   ├── academic.md
│   │   └── literary.md
│   └── style/xinyada.md      #   信雅达标准
├── projects/                 # 翻译项目（submodule）
├── templates/                # 新项目模板
├── .claude/commands/         # Claude Code 命令
├── .github/workflows/        # 引擎 CI
└── workflows/build.yml       # 消费方项目 CI 模板
```
