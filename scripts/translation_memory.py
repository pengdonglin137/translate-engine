#!/usr/bin/env python3
"""
翻译记忆系统

记录和复用已翻译的段落，提高翻译一致性和效率。

功能：
1. 记录已翻译的段落
2. 查询相似段落的翻译
3. 导出/导入翻译记忆

用法:
    python translation_memory.py add --source "English text" --target "中文翻译"
    python translation_memory.py search --query "English text"
    python translation_memory.py export --output tm.json
    python translation_memory.py import --input tm.json
"""

import argparse
import json
import hashlib
import sys
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime


class TranslationMemory:
    """翻译记忆存储"""

    def __init__(self, memory_file: str = ".translate-memory.json"):
        self.memory_file = Path(memory_file)
        self.data = self._load()

    def _load(self) -> dict:
        """加载翻译记忆"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "entries": []
        }

    def _save(self):
        """保存翻译记忆"""
        self.data["updated"] = datetime.now().isoformat()
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def _hash(self, text: str) -> str:
        """计算文本哈希"""
        return hashlib.md5(text.encode()).hexdigest()

    def add(self, source: str, target: str, context: str = "", file_path: str = "", line_num: int = 0):
        """添加翻译记录"""
        entry = {
            "hash": self._hash(source),
            "source": source,
            "target": target,
            "context": context,
            "file": file_path,
            "line": line_num,
            "created": datetime.now().isoformat(),
            "usage_count": 0
        }

        # 检查是否已存在
        for i, existing in enumerate(self.data["entries"]):
            if existing["hash"] == entry["hash"]:
                # 更新现有记录
                self.data["entries"][i]["target"] = target
                self.data["entries"][i]["updated"] = datetime.now().isoformat()
                self._save()
                return True

        # 添加新记录
        self.data["entries"].append(entry)
        self._save()
        return True

    def search(self, query: str, threshold: float = 0.3) -> List[dict]:
        """搜索相似翻译"""
        results = []
        query_hash = self._hash(query)

        for entry in self.data["entries"]:
            # 精确匹配
            if entry["hash"] == query_hash:
                entry["match_type"] = "exact"
                entry["score"] = 1.0
                results.append(entry)
                continue

            # 简单相似度计算（基于共同词）
            source_words = set(query.lower().split())
            entry_words = set(entry["source"].lower().split())

            if not source_words or not entry_words:
                continue

            intersection = source_words & entry_words
            union = source_words | entry_words
            similarity = len(intersection) / len(union)

            if similarity >= threshold:
                entry_copy = entry.copy()
                entry_copy["match_type"] = "fuzzy"
                entry_copy["score"] = similarity
                results.append(entry_copy)

        # 按分数排序
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:10]  # 最多返回 10 个结果

    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "total_entries": len(self.data["entries"]),
            "created": self.data.get("created", ""),
            "updated": self.data.get("updated", "")
        }

    def export(self, output_file: str):
        """导出翻译记忆"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def import_memory(self, input_file: str):
        """导入翻译记忆"""
        with open(input_file, 'r', encoding='utf-8') as f:
            imported = json.load(f)

        # 合并记录
        existing_hashes = {e["hash"] for e in self.data["entries"]}
        new_count = 0

        for entry in imported.get("entries", []):
            if entry["hash"] not in existing_hashes:
                self.data["entries"].append(entry)
                existing_hashes.add(entry["hash"])
                new_count += 1

        self._save()
        return new_count


def main():
    parser = argparse.ArgumentParser(description='翻译记忆系统')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # add 命令
    add_parser = subparsers.add_parser('add', help='添加翻译记录')
    add_parser.add_argument('--source', required=True, help='原文')
    add_parser.add_argument('--target', required=True, help='译文')
    add_parser.add_argument('--context', default='', help='上下文')
    add_parser.add_argument('--file', default='', help='文件路径')
    add_parser.add_argument('--line', type=int, default=0, help='行号')

    # search 命令
    search_parser = subparsers.add_parser('search', help='搜索相似翻译')
    search_parser.add_argument('--query', required=True, help='搜索查询')
    search_parser.add_argument('--threshold', type=float, default=0.3, help='相似度阈值')

    # stats 命令
    subparsers.add_parser('stats', help='显示统计信息')

    # export 命令
    export_parser = subparsers.add_parser('export', help='导出翻译记忆')
    export_parser.add_argument('--output', required=True, help='输出文件')

    # import 命令
    import_parser = subparsers.add_parser('import', help='导入翻译记忆')
    import_parser.add_argument('--input', required=True, help='输入文件')

    args = parser.parse_args()

    tm = TranslationMemory()

    if args.command == 'add':
        tm.add(args.source, args.target, args.context, args.file, args.line)
        print(f"✓ 已添加翻译记录")

    elif args.command == 'search':
        results = tm.search(args.query, args.threshold)
        if results:
            print(f"\n找到 {len(results)} 个相似翻译:\n")
            for r in results:
                match_type = "精确" if r["match_type"] == "exact" else f"相似({r['score']:.2%})"
                print(f"  [{match_type}] {r['source'][:50]}...")
                print(f"    → {r['target'][:50]}...")
                print()
        else:
            print("未找到相似翻译")

    elif args.command == 'stats':
        stats = tm.get_stats()
        print(f"\n翻译记忆统计:")
        print(f"  总记录数: {stats['total_entries']}")
        print(f"  创建时间: {stats['created']}")
        print(f"  更新时间: {stats['updated']}")

    elif args.command == 'export':
        tm.export(args.output)
        print(f"✓ 已导出到 {args.output}")

    elif args.command == 'import':
        new_count = tm.import_memory(args.input)
        print(f"✓ 已导入 {new_count} 条新记录")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
