#!/usr/bin/env python3
"""
术语一致性检查工具

检查翻译项目中术语使用的一致性。
支持 LaTeX、Markdown、纯文本等格式。

用法:
    python check_terms.py [--config config.yaml] [--terms terms.yaml] [--fix]
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import yaml


def load_config(config_path: str) -> dict:
    """加载项目配置"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_terms(terms_path: str) -> List[dict]:
    """加载术语表"""
    with open(terms_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('terms', [])


def should_skip_line(line: str, file_type: str) -> bool:
    """判断是否应该跳过该行"""
    stripped = line.strip()

    # LaTeX: 跳过命令、标签、引用、代码环境
    if file_type == 'latex':
        if stripped.startswith('\\label{') or stripped.startswith('\\IX{'):
            return True
        if stripped.startswith('\\co{') or stripped.startswith('\\path{'):
            return True
        if stripped.startswith('\\cite{') or stripped.startswith('\\cref{'):
            return True
        if stripped.startswith('\\apik{') or stripped.startswith('\\api{'):
            return True
        if stripped.startswith('\\begin{Verbatim') or stripped.startswith('\\end{Verbatim'):
            return True
        if stripped.startswith('%'):  # 注释
            return True
        if '$' in stripped and '\\co{' not in stripped:  # 数学公式
            return True

    # Markdown: 跳过代码块
    if file_type == 'markdown':
        if stripped.startswith('```') or stripped.startswith('    '):
            return True
        if stripped.startswith('!['):  # 图片
            return True

    return False


def extract_prose(text: str, file_type: str) -> str:
    """提取纯文本内容（去除 LaTeX/Markdown 标记）"""
    if file_type == 'latex':
        # 去除 LaTeX 命令的参数，保留命令名
        text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', text)
        # 去除数学公式
        text = re.sub(r'\$[^$]*\$', '', text)

    if file_type == 'markdown':
        # 去除 Markdown 标记
        text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
        text = re.sub(r'[*_`]', '', text)

    return text


def check_file(file_path: Path, terms: List[dict], file_type: str) -> List[dict]:
    """检查单个文件的术语一致性"""
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, PermissionError):
        return issues

    for line_num, line in enumerate(lines, 1):
        if should_skip_line(line, file_type):
            continue

        prose = extract_prose(line, file_type)

        for term in terms:
            en_term = term['en']
            zh_term = term['zh']
            rule = term.get('rule', 'translate')

            # 检查是否在中文上下文中使用了英文术语
            if rule == 'translate' and en_term in prose:
                # 检查周围是否有中文字符（表明是中文上下文）
                zh_context = re.search(r'[一-鿿]', prose)
                if zh_context:
                    # 排除首次出现标注的情况
                    if f'{zh_term}（{en_term}）' not in prose and f'{zh_term}({en_term})' not in prose:
                        issues.append({
                            'file': str(file_path),
                            'line': line_num,
                            'term_en': en_term,
                            'term_zh': zh_term,
                            'context': line.strip()[:100],
                            'type': 'inconsistency'
                        })

    return issues


def main():
    parser = argparse.ArgumentParser(description='术语一致性检查')
    parser.add_argument('--config', default='config.yaml', help='项目配置文件')
    parser.add_argument('--terms', default='terms.yaml', help='术语表文件')
    parser.add_argument('--fix', action='store_true', help='自动修复（实验性）')
    args = parser.parse_args()

    # 加载配置
    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"错误: 配置文件 {args.config} 不存在")
        sys.exit(1)

    # 加载术语表
    try:
        terms = load_terms(args.terms)
    except FileNotFoundError:
        print(f"错误: 术语表 {args.terms} 不存在")
        sys.exit(1)

    if not terms:
        print("术语表为空，跳过检查")
        return

    # 确定文件类型
    source_type = config.get('source', {}).get('type', 'latex')

    # 扫描翻译目录
    translation_dir = Path('.')
    issues = []

    # 根据文件类型确定扩展名
    extensions = {
        'latex': ['*.tex'],
        'markdown': ['*.md', '*.markdown'],
        'rst': ['*.rst'],
    }

    for ext_pattern in extensions.get(source_type, ['*.tex', '*.md']):
        for file_path in translation_dir.rglob(ext_pattern):
            # 跳过 source 目录
            if 'source' in file_path.parts or '.translate-engine' in file_path.parts:
                continue
            issues.extend(check_file(file_path, terms, source_type))

    # 输出结果
    if issues:
        print(f"\n发现 {len(issues)} 个术语不一致问题:\n")
        for issue in issues[:20]:  # 最多显示 20 个
            print(f"  {issue['file']}:{issue['line']}")
            print(f"    英文: {issue['term_en']}")
            print(f"    中文: {issue['term_zh']}")
            print(f"    上下文: {issue['context']}")
            print()

        if len(issues) > 20:
            print(f"  ... 还有 {len(issues) - 20} 个问题未显示")

        sys.exit(1)
    else:
        print("✓ 术语一致性检查通过")
        sys.exit(0)


if __name__ == '__main__':
    main()
