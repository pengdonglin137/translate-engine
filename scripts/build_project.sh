#!/bin/bash
# 自动化翻译项目构建脚本
# 用法: ./scripts/build_project.sh <project_name>

set -e

PROJECT_NAME=$1
PROJECT_DIR="projects/$PROJECT_NAME"

if [ -z "$PROJECT_NAME" ]; then
    echo "用法: $0 <project_name>"
    echo "可用项目:"
    ls projects/
    exit 1
fi

if [ ! -d "$PROJECT_DIR" ]; then
    echo "错误: 项目 $PROJECT_NAME 不存在"
    exit 1
fi

echo "=== 构建翻译项目: $PROJECT_NAME ==="

# 检测项目类型和构建方法
cd "$PROJECT_DIR"

if [ -f "Makefile" ]; then
    echo "检测到 Makefile，使用 make 构建..."
    make
elif [ -f "export_book.py" ]; then
    echo "检测到 export_book.py，使用 pandoc 构建..."
    python3 export_book.py
    xelatex -interaction=nonstopmode book.tex
elif [ -f "conf.py" ]; then
    echo "检测到 conf.py，使用 Sphinx 构建..."
    sphinx-build -b html . _build/html
else
    echo "错误: 未检测到构建配置"
    exit 1
fi

echo "=== 构建完成 ==="
ls -lh *.pdf 2>/dev/null || ls -lh _build/html/index.html 2>/dev/null
