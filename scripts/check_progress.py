#!/usr/bin/env python3
"""
翻译进度统计工具

统计翻译项目的完成进度和质量评分。

用法:
    python check_progress.py [--config config.yaml] [--format json|text|yaml]
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List
import yaml


def load_config(config_path: str) -> dict:
    """加载项目配置"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def detect_language(content: str) -> float:
    """检测内容的语言比例（中文字符占比）"""
    # 匹配中文字符
    chinese_chars = len(re.findall(r'[一-鿿]', content))
    # 匹配英文单词
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', content))

    total = chinese_chars + english_words
    if total == 0:
        return 0.0

    return chinese_chars / total


def is_prose_line(line: str, file_type: str) -> bool:
    """判断是否是可翻译的散文行"""
    stripped = line.strip()

    # 空行
    if not stripped:
        return False

    # LaTeX: 跳过命令、代码、标签
    if file_type == 'latex':
        if stripped.startswith('\\'):
            # 但保留某些可翻译的命令
            translateable_commands = [
                '\\section{', '\\subsection{', '\\subsubsection{',
                '\\caption{', '\\chapter{', '\\paragraph{',
                '\\Epigraph{', '\\QuickQuiz{', '\\QuickQuizAnswer{',
            ]
            if not any(stripped.startswith(cmd) for cmd in translateable_commands):
                return False
        if stripped.startswith('%'):  # 注释
            return False
        if stripped.startswith('\\begin{Verbatim') or stripped.startswith('\\end{Verbatim'):
            return False
        if stripped.startswith('\\begin{listing') or stripped.startswith('\\end{listing'):
            return False
        if stripped.startswith('\\begin{fcv') or stripped.startswith('\\end{fcv'):
            return False

    # Markdown: 跳过代码块
    if file_type == 'markdown':
        if stripped.startswith('```'):
            return False
        if stripped.startswith('    '):
            return False

    return True


def analyze_file(file_path: Path, file_type: str) -> dict:
    """分析单个文件的翻译进度"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, PermissionError):
        return {'total': 0, 'translatable': 0, 'translated': 0, 'ratio': 0.0}

    total_lines = len(lines)
    translatable_lines = 0
    translated_lines = 0

    for line in lines:
        if is_prose_line(line, file_type):
            translatable_lines += 1
            # 检测该行是否包含中文
            if re.search(r'[一-鿿]', line):
                translated_lines += 1

    ratio = translated_lines / translatable_lines if translatable_lines > 0 else 0.0

    return {
        'total': total_lines,
        'translatable': translatable_lines,
        'translated': translated_lines,
        'ratio': ratio
    }


def scan_project(config: dict) -> Dict[str, dict]:
    """扫描项目所有文件"""
    source_type = config.get('source', {}).get('type', 'latex')
    extensions = {
        'latex': ['*.tex'],
        'markdown': ['*.md'],
        'rst': ['*.rst'],
    }

    results = {}
    translation_dir = Path('.')

    for ext_pattern in extensions.get(source_type, ['*.tex']):
        for file_path in sorted(translation_dir.rglob(ext_pattern)):
            # 跳过 source 目录
            if 'source' in file_path.parts or '.translate-engine' in file_path.parts:
                continue
            if '.git' in file_path.parts:
                continue

            stats = analyze_file(file_path, source_type)
            if stats['translatable'] > 0:
                results[str(file_path)] = stats

    return results


def format_text_report(results: Dict[str, dict]) -> str:
    """生成文本报告"""
    lines = []
    lines.append("=" * 60)
    lines.append("翻译进度报告")
    lines.append("=" * 60)
    lines.append("")

    total_translatable = 0
    total_translated = 0

    for file_path, stats in sorted(results.items()):
        translatable = stats['translatable']
        translated = stats['translated']
        ratio = stats['ratio']
        total_translatable += translatable
        total_translated += translated

        status = "✓" if ratio >= 0.95 else "○" if ratio >= 0.5 else "✗"
        lines.append(f"  {status} {file_path}")
        lines.append(f"    可翻译: {translatable} 行, 已翻译: {translated} 行 ({ratio:.1%})")

    lines.append("")
    lines.append("-" * 60)

    overall_ratio = total_translated / total_translatable if total_translatable > 0 else 0.0
    lines.append(f"总计: {total_translatable} 行可翻译, {total_translated} 行已翻译 ({overall_ratio:.1%})")

    # 进度条
    bar_width = 40
    filled = int(bar_width * overall_ratio)
    bar = "█" * filled + "░" * (bar_width - filled)
    lines.append(f"进度: [{bar}] {overall_ratio:.1%}")

    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='翻译进度统计')
    parser.add_argument('--config', default='config.yaml', help='项目配置文件')
    parser.add_argument('--format', choices=['text', 'json', 'yaml'], default='text', help='输出格式')
    args = parser.parse_args()

    # 加载配置
    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"错误: 配置文件 {args.config} 不存在")
        sys.exit(1)

    # 扫描项目
    results = scan_project(config)

    # 输出结果
    if args.format == 'text':
        print(format_text_report(results))
    elif args.format == 'json':
        import json
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.format == 'yaml':
        print(yaml.dump(results, allow_unicode=True, default_flow_style=False))


if __name__ == '__main__':
    main()
