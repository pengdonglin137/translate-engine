#!/usr/bin/env python3
"""
术语一致性检查工具（改进版）

检查翻译项目中术语使用的一致性。
支持 LaTeX、Markdown、纯文本等格式。

主要改进：
1. 智能排除首次出现标注（如 "锁（lock）"）
2. 排除 LaTeX 命令、代码环境、标签等
3. 排除注释和数学公式
4. 支持词边界匹配，避免 "deadlock" 中的 "lock" 被误报
5. 支持上下文感知的术语检查

用法:
    python check_terms.py [--config config.yaml] [--terms terms.yaml] [--verbose]
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
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


class LineSkipper:
    """判断是否应该跳过某行或某行的特定部分"""

    def __init__(self, file_type: str):
        self.file_type = file_type
        self.in_verbatim = False
        self.in_comment = False

    def should_skip_line(self, line: str) -> bool:
        """判断整行是否应该跳过"""
        stripped = line.strip()

        # LaTeX 环境追踪
        if self.file_type == 'latex':
            if '\\begin{Verbatim' in stripped or '\\begin{listing' in stripped:
                self.in_verbatim = True
            if '\\end{Verbatim' in stripped or '\\end{listing' in stripped:
                self.in_verbatim = False
                return True

            if self.in_verbatim:
                return True

            # 跳过纯注释行
            if stripped.startswith('%'):
                return True

            # 跳过纯标签/引用行
            if stripped.startswith('\\label{') or stripped.startswith('\\IX{'):
                return True
            if stripped.startswith('\\cref{') or stripped.startswith('\\Cref{'):
                return True
            if stripped.startswith('\\cpageref{'):
                return True

            # 跳过纯代码引用行
            if stripped.startswith('\\co{') and len(stripped) < 50:
                return True

            # 跳过 index 相关
            if stripped.startswith('\\api{') or stripped.startswith('\\apik{'):
                return True
            if stripped.startswith('\\IXalt{') or stripped.startswith('\\IXr{'):
                return True

        # Markdown: 跳过代码块
        if self.file_type == 'markdown':
            if stripped.startswith('```'):
                self.in_verbatim = not self.in_verbatim
                return True
            if self.in_verbatim:
                return True
            if stripped.startswith('    '):
                return True
            if stripped.startswith('!['):  # 图片
                return True

        return False

    def extract_prose(self, line: str) -> str:
        """提取行中的纯文本内容（去除 LaTeX/Markdown 标记）"""
        text = line

        if self.file_type == 'latex':
            # 去除 \co{...} 中的内容
            text = re.sub(r'\\co\{[^}]*\}', '', text)
            # 去除 \path{...}
            text = re.sub(r'\\path\{[^}]*\}', '', text)
            # 去除 \url{...}
            text = re.sub(r'\\url\{[^}]*\}', '', text)
            # 去除 \cite{...}
            text = re.sub(r'\\cite\{[^}]*\}', '', text)
            # 去除 \cref{...}, \Cref{...}
            text = re.sub(r'\\[cC]ref\{[^}]*\}', '', text)
            # 去除 \cpageref{...}
            text = re.sub(r'\\cpageref\{[^}]*\}', '', text)
            # 去除 \label{...}
            text = re.sub(r'\\label\{[^}]*\}', '', text)
            # 去除 \IX{...} 等索引命令
            text = re.sub(r'\\IX\w*\{[^}]*\}', '', text)
            # 去除 \apik{...} 等 API 索引
            text = re.sub(r'\\api\w*\{[^}]*\}', '', text)
            # 去除 \ppl{...}{...} 人名命令
            text = re.sub(r'\\ppl\{[^}]*\}\{[^}]*\}', '', text)
            # 去除数学公式 $...$
            text = re.sub(r'\$[^$]*\$', '', text)
            # 去除 \emph{...} 等格式命令（保留内容）
            text = re.sub(r'\\emph\{([^}]*)\}', r'\1', text)
            # 去除其他 LaTeX 命令的参数
            text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', text)
            # 去除 LaTeX 命令（如 \label, \centering 等）
            text = re.sub(r'\\[a-zA-Z]+', '', text)

        if self.file_type == 'markdown':
            # 去除 Markdown 链接
            text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
            # 去除格式标记
            text = re.sub(r'[*_`]', '', text)

        return text


def is_first_occurrence_annotation(line: str, en_term: str, zh_term: str) -> bool:
    """检测是否是首次出现标注（如 "锁（lock）" 或 "锁(lock)"）"""
    # 模式1: 中文术语（英文术语）
    pattern1 = f'{re.escape(zh_term)}[（(]{re.escape(en_term)}[）)]'
    if re.search(pattern1, line):
        return True

    # 模式2: 英文术语在括号中，前面有中文
    pattern2 = f'[一-鿿][^一-鿿]*[（(]\\s*{re.escape(en_term)}\\s*[）)]'
    if re.search(pattern2, line):
        return True

    return False


def is_in_latex_command(line: str, en_term: str, pos: int) -> bool:
    """检测术语是否在 LaTeX 命令中"""
    # 检查是否在 \command{...} 的参数中
    # 向前搜索，看是否有 \command{ 在这个位置之前且未关闭
    prefix = line[:pos]

    # 统计未关闭的花括号
    depth = 0
    i = len(prefix) - 1
    while i >= 0:
        if prefix[i] == '}':
            depth += 1
        elif prefix[i] == '{':
            if depth == 0:
                # 这个 { 是最近的未关闭的
                # 检查前面是否是命令名
                cmd_match = re.search(r'\\([a-zA-Z]+)$', prefix[:i])
                if cmd_match:
                    return True
                break
            depth -= 1
        i -= 1

    return False


def has_chinese_context(text: str, pos: int, window: int = 20) -> bool:
    """检测位置附近是否有中文字符"""
    start = max(0, pos - window)
    end = min(len(text), pos + window)
    nearby = text[start:end]
    return bool(re.search(r'[一-鿿]', nearby))


def check_line_for_term(line: str, term: dict, skipper: LineSkipper) -> List[dict]:
    """检查一行中是否有术语不一致"""
    issues = []
    en_term = term['en']
    zh_term = term['zh']
    rule = term.get('rule', 'translate')

    # 跳过保留英文的术语
    if rule == 'keep_english':
        return issues

    # 提取纯文本
    prose = skipper.extract_prose(line)

    # 查找英文术语的所有出现位置
    for match in re.finditer(re.escape(en_term), prose):
        pos = match.start()
        end = pos + len(en_term)

        # 排除1: 首次出现标注
        if is_first_occurrence_annotation(line, en_term, zh_term):
            continue

        # 排除2: 在 LaTeX 命令中
        if is_in_latex_command(line, en_term, pos):
            continue

        # 排除3: 是更大单词的一部分（词边界检查）
        # 检查前面的字符
        if pos > 0:
            prev_char = prose[pos - 1]
            if prev_char.isalnum() or prev_char == '_':
                continue
        # 检查后面的字符
        if end < len(prose):
            next_char = prose[end]
            if next_char.isalnum() or next_char == '_':
                continue

        # 排除4: 在中文上下文中
        # 如果术语前面直接跟着中文字符，可能是有效的混合使用
        if pos > 0:
            prev_char = prose[pos - 1]
            if re.match(r'[一-鿿]', prev_char):
                # 中文+英文术语的模式，如 "读写lock"
                # 这种情况需要检查是否是已知的混合模式
                # 暂时跳过这种模式（用户可以选择严格模式）
                continue

        # 排除5: 术语后面跟着中文的"（"或"("（首次标注的变体）
        if end < len(prose):
            next_chars = prose[end:end+2]
            if next_chars in ['（', '(', '》', '>']:
                continue

        # 检查是否有中文上下文
        if has_chinese_context(prose, pos):
            issues.append({
                'file': '',  # 由调用者填充
                'line': 0,   # 由调用者填充
                'term_en': en_term,
                'term_zh': zh_term,
                'context': line.strip()[:100],
                'position': pos,
                'type': 'inconsistency'
            })

    return issues


def check_file(file_path: Path, terms: List[dict], file_type: str, verbose: bool = False, relative_to: Path = None) -> List[dict]:
    """检查单个文件的术语一致性"""
    issues = []
    skipper = LineSkipper(file_type)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, PermissionError):
        return issues

    for line_num, line in enumerate(lines, 1):
        if skipper.should_skip_line(line):
            continue

        for term in terms:
            line_issues = check_line_for_term(line, term, skipper)
            for issue in line_issues:
                if relative_to:
                    try:
                        issue['file'] = str(file_path.relative_to(relative_to))
                    except ValueError:
                        issue['file'] = str(file_path)
                else:
                    issue['file'] = str(file_path)
                issue['line'] = line_num
            issues.extend(line_issues)

    return issues


def main():
    parser = argparse.ArgumentParser(description='术语一致性检查（改进版）')
    parser.add_argument('--project', '-p', default='.', help='项目根目录（默认当前目录）')
    parser.add_argument('--config', default=None, help='项目配置文件（相对于项目目录）')
    parser.add_argument('--terms', default=None, help='术语表文件（相对于项目目录）')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    parser.add_argument('--strict', action='store_true', help='严格模式（更多检查）')
    args = parser.parse_args()

    # 解析项目目录
    project_dir = Path(args.project).resolve()
    if not project_dir.is_dir():
        print(f"错误: 项目目录 {project_dir} 不存在")
        sys.exit(1)

    # 解析配置和术语表路径（相对于项目目录）
    config_path = project_dir / (args.config or 'config.yaml')
    terms_path = project_dir / (args.terms or 'terms.yaml')

    # 加载配置
    try:
        config = load_config(str(config_path))
    except FileNotFoundError:
        print(f"错误: 配置文件 {config_path} 不存在")
        sys.exit(1)

    # 加载术语表
    try:
        terms = load_terms(str(terms_path))
    except FileNotFoundError:
        print(f"错误: 术语表 {terms_path} 不存在")
        sys.exit(1)

    if not terms:
        print("术语表为空，跳过检查")
        return

    # 确定文件类型
    source_type = config.get('source', {}).get('type', 'latex')

    # 扫描翻译目录（项目目录）
    translation_dir = project_dir
    all_issues = []

    # 根据文件类型确定扩展名
    extensions = {
        'latex': ['*.tex'],
        'markdown': ['*.md', '*.markdown'],
        'rst': ['*.rst'],
    }

    files_checked = 0
    for ext_pattern in extensions.get(source_type, ['*.tex', '*.md']):
        for file_path in sorted(translation_dir.rglob(ext_pattern)):
            # 跳过 source 目录、translate-engine 目录和生成文件
            if 'source' in file_path.parts or '.translate-engine' in file_path.parts:
                continue
            if 'translate-engine' in file_path.parts and 'projects' not in file_path.parts:
                continue
            if '.git' in file_path.parts:
                continue
            # 跳过生成的 .flat 文件
            if file_path.name.endswith('_flat.tex'):
                continue
            if file_path.name.startswith('qqz') and file_path.suffix == '.tex':
                continue  # 跳过 QuickQuiz 生成文件

            issues = check_file(file_path, terms, source_type, args.verbose, relative_to=project_dir)
            all_issues.extend(issues)
            files_checked += 1

    # 去重（同一行同一术语只报告一次）
    seen = set()
    unique_issues = []
    for issue in all_issues:
        key = (issue['file'], issue['line'], issue['term_en'])
        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)

    # 输出结果
    if unique_issues:
        print(f"\n检查了 {files_checked} 个文件，发现 {len(unique_issues)} 个术语不一致问题:\n")

        # 按文件分组
        by_file = {}
        for issue in unique_issues:
            by_file.setdefault(issue['file'], []).append(issue)

        for file_path, file_issues in sorted(by_file.items()):
            print(f"  {file_path}:")
            for issue in file_issues[:5]:  # 每个文件最多显示 5 个
                print(f"    行 {issue['line']}: {issue['term_en']} → 应为 {issue['term_zh']}")
                if args.verbose:
                    print(f"      上下文: {issue['context']}")
            if len(file_issues) > 5:
                print(f"    ... 还有 {len(file_issues) - 5} 个问题")
            print()

        if args.verbose:
            print(f"总计: {len(unique_issues)} 个问题")

        sys.exit(1)
    else:
        print(f"✓ 术语一致性检查通过（检查了 {files_checked} 个文件）")
        sys.exit(0)


if __name__ == '__main__':
    main()
