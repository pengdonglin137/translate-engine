#!/usr/bin/env python3
"""
翻译质量检查脚本
检查术语一致性、翻译完整性、格式正确性
"""

import os
import re
from pathlib import Path

class QualityChecker:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
    
    def check_terminology(self, terms_file):
        """检查术语一致性"""
        if not terms_file.exists():
            print(f"警告: 术语表不存在")
            return []
        
        # 读取术语表
        terms = {}
        with open(terms_file, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line and not line.startswith('#'):
                    parts = line.split(':')
                    if len(parts) >= 2:
                        en_term = parts[0].strip()
                        zh_term = parts[1].strip()
                        terms[en_term] = zh_term
        
        # 检查文件中的术语使用
        issues = []
        for file_path in self.project_dir.rglob('*.md'):
            if '.git' in file_path.parts:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    for en_term, zh_term in terms.items():
                        # 检查是否有未翻译的英文术语
                        if en_term in content and zh_term not in content:
                            issues.append(f"{file_path}: 发现未翻译的术语 '{en_term}'")
            except:
                pass
        
        return issues
    
    def check_translation_completeness(self):
        """检查翻译完整性"""
        issues = []
        
        for file_path in self.project_dir.rglob('*.md'):
            if '.git' in file_path.parts:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    # 检查是否有空行过多（可能是未翻译）
                    empty_count = sum(1 for line in lines if line.strip() == '')
                    if empty_count > len(lines) * 0.3:
                        issues.append(f"{file_path}: 空行过多 ({empty_count}/{len(lines)})")
            except:
                pass
        
        return issues
    
    def check_format(self):
        """检查格式正确性"""
        issues = []
        
        for file_path in self.project_dir.rglob('*.md'):
            if '.git' in file_path.parts:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 检查 Markdown 格式
                    # 检查标题格式
                    for i, line in enumerate(content.split('\n'), 1):
                        if line.startswith('#') and not line.startswith('# '):
                            if not line.startswith('##'):
                                issues.append(f"{file_path}:{i}: 标题格式不正确")
            except:
                pass
        
        return issues
    
    def run_all_checks(self):
        """运行所有检查"""
        print("\n=== 翻译质量检查 ===\n")
        
        terms_file = self.project_dir / 'terms.yaml'
        
        print("1. 检查术语一致性...")
        term_issues = self.check_terminology(terms_file)
        if term_issues:
            print(f"   发现 {len(term_issues)} 个术语问题")
            for issue in term_issues[:5]:
                print(f"   - {issue}")
        else:
            print("   ✓ 术语一致性检查通过")
        
        print("\n2. 检查翻译完整性...")
        completeness_issues = self.check_translation_completeness()
        if completeness_issues:
            print(f"   发现 {len(completeness_issues)} 个完整性问题")
            for issue in completeness_issues[:5]:
                print(f"   - {issue}")
        else:
            print("   ✓ 翻译完整性检查通过")
        
        print("\n3. 检查格式正确性...")
        format_issues = self.check_format()
        if format_issues:
            print(f"   发现 {len(format_issues)} 个格式问题")
            for issue in format_issues[:5]:
                print(f"   - {issue}")
        else:
            print("   ✓ 格式检查通过")
        
        # 总结
        total_issues = len(term_issues) + len(completeness_issues) + len(format_issues)
        print(f"\n=== 检查完成 ===")
        print(f"总计: {total_issues} 个问题")
        
        return total_issues == 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: quality_check.py <project_name>")
        sys.exit(1)
    
    project_name = sys.argv[1]
    project_dir = Path(__file__).parent.parent / 'projects' / project_name
    
    if not project_dir.exists():
        print(f"错误: 项目 {project_name} 不存在")
        sys.exit(1)
    
    checker = QualityChecker(project_dir)
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)
