# 翻译工作流优化方案

## 优化前后对比

### 优化前
1. 手动克隆项目
2. 手动安装依赖（pandoc、pandoc-crossref）
3. 手动逐文件翻译
4. 手动构建 PDF
5. 无质量检查

### 优化后
1. 自动化项目管理
2. 标准化构建环境（Docker）
3. 自动化翻译工作流
4. 自动化构建脚本
5. 内置质量检查

## 新增工具

### 1. 构建环境 Docker 镜像
```bash
docker build -f docker/Dockerfile.builder -t translate-builder .
```

### 2. 自动化构建脚本
```bash
./scripts/build_project.sh perf-book
```

### 3. 翻译工作流管理
```bash
python3 scripts/translate_workflow.py list           # 列出项目
python3 scripts/translate_workflow.py progress perfbook  # 查看翻译进度
python3 scripts/translate_workflow.py check perfbook     # 检查术语
python3 scripts/translate_workflow.py build perfbook     # 构建项目
```

### 4. 质量检查
```bash
python3 scripts/quality_check.py perfbook
```

## 工作流程

### 完整翻译流程
1. 添加翻译项目为 submodule
2. 运行 `/translate` 命令自动翻译
3. 运行质量检查确保术语一致性
4. 构建 PDF
5. 验证输出

### 增量翻译流程
1. 检查翻译进度
2. 翻译未完成的文件
3. 运行术语检查
4. 构建更新的 PDF

## 依赖要求

### 系统依赖
- Python 3.6+
- Make
- Git

### LaTeX 依赖
- xelatex
- texlive-lang-chinese
- fonts-noto-cjk

### Pandoc 依赖（perf-book 项目）
- pandoc 2.9.x
- pandoc-crossref 0.3.x
- pandoc-fignos
- pandoc-tablenos

### Python 依赖
- pyyaml
- natsort
