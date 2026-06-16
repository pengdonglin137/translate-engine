#!/usr/bin/env python3
"""
翻译工作流自动化脚本

集成翻译记忆、术语检查、进度追踪于一体。

用法:
    python translate.py init                    # 初始化翻译记忆
    python translate.py status                  # 查看翻译状态
    python translate.py check                   # 运行质量检查
    python translate.py suggest "English text"  # 查询翻译建议
    python translate.py record "English" "中文" # 记录翻译
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, check: bool = True) -> tuple:
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr


def cmd_init(args):
    """初始化翻译记忆"""
    engine_dir = Path('.translate-engine')
    if not engine_dir.exists():
        print("错误: .translate-engine 目录不存在")
        print("请先添加 translate-engine submodule:")
        print("  git submodule add git@github.com:pengdonglin137/translate-engine.git .translate-engine")
        return 1

    print("✓ 翻译引擎已就绪")
    return 0


def cmd_status(args):
    """查看翻译状态"""
    # 进度统计
    print("\n📊 翻译进度:")
    print("=" * 50)

    rc, stdout, stderr = run_command(
        ['python3', '.translate-engine/scripts/check_progress.py'],
        check=False
    )
    if stdout:
        print(stdout)

    # 术语检查
    print("\n🔍 术语检查:")
    print("=" * 50)

    rc, stdout, stderr = run_command(
        ['python3', '.translate-engine/scripts/check_terms.py',
         '--config', 'config.yaml',
         '--terms', 'terms.yaml'],
        check=False
    )
    if stdout:
        print(stdout)

    return 0


def cmd_check(args):
    """运行质量检查"""
    errors = []

    # 术语检查
    print("🔍 运行术语检查...")
    rc, stdout, stderr = run_command(
        ['python3', '.translate-engine/scripts/check_terms.py',
         '--config', 'config.yaml',
         '--terms', 'terms.yaml'],
        check=False
    )
    if rc != 0:
        errors.append("术语检查失败")
        if stdout:
            print(stdout)

    # 构建检查
    if args.build:
        print("\n🔨 运行构建检查...")
        rc, stdout, stderr = run_command(['make', '1c'], check=False)
        if rc != 0:
            errors.append("构建失败")
            if stderr:
                print(stderr)

    if errors:
        print(f"\n❌ 发现 {len(errors)} 个问题:")
        for e in errors:
            print(f"  - {e}")
        return 1
    else:
        print("\n✅ 质量检查通过")
        return 0


def cmd_suggest(args):
    """查询翻译建议"""
    # 导入翻译记忆
    sys.path.insert(0, '.translate-engine/scripts')
    from translation_memory import TranslationMemory

    tm = TranslationMemory()
    results = tm.search(args.text)

    if results:
        print(f"\n找到 {len(results)} 个翻译建议:\n")
        for i, r in enumerate(results, 1):
            match_type = "精确" if r["match_type"] == "exact" else f"相似({r['score']:.0%})"
            print(f"{i}. [{match_type}]")
            print(f"   原文: {r['source'][:80]}...")
            print(f"   译文: {r['target'][:80]}...")
            print()
    else:
        print("未找到相似翻译")

    return 0


def cmd_record(args):
    """记录翻译"""
    sys.path.insert(0, '.translate-engine/scripts')
    from translation_memory import TranslationMemory

    tm = TranslationMemory()
    tm.add(args.source, args.target, file=args.file or "", line=args.line or 0)
    print(f"✓ 已记录翻译")

    return 0


def main():
    parser = argparse.ArgumentParser(description='翻译工作流自动化')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # init 命令
    subparsers.add_parser('init', help='初始化翻译记忆')

    # status 命令
    subparsers.add_parser('status', help='查看翻译状态')

    # check 命令
    check_parser = subparsers.add_parser('check', help='运行质量检查')
    check_parser.add_argument('--build', action='store_true', help='同时运行构建检查')

    # suggest 命令
    suggest_parser = subparsers.add_parser('suggest', help='查询翻译建议')
    suggest_parser.add_argument('text', help='要查询的原文')

    # record 命令
    record_parser = subparsers.add_parser('record', help='记录翻译')
    record_parser.add_argument('source', help='原文')
    record_parser.add_argument('target', help='译文')
    record_parser.add_argument('--file', help='文件路径')
    record_parser.add_argument('--line', type=int, help='行号')

    args = parser.parse_args()

    if args.command == 'init':
        return cmd_init(args)
    elif args.command == 'status':
        return cmd_status(args)
    elif args.command == 'check':
        return cmd_check(args)
    elif args.command == 'suggest':
        return cmd_suggest(args)
    elif args.command == 'record':
        return cmd_record(args)
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    sys.exit(main())
