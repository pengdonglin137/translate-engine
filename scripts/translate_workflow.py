#!/usr/bin/env python3
"""
翻译工作流自动化脚本
支持增量翻译、质量检查、构建验证
"""

import os
import sys
import yaml
from pathlib import Path

class TranslationWorkflow:
    def __init__(self, engine_dir):
        self.engine_dir = Path(engine_dir)
        self.projects_dir = self.engine_dir / 'projects'
    
    def list_projects(self):
        """列出所有翻译项目"""
        projects = []
        for p in self.projects_dir.iterdir():
            if p.is_dir() and (p / 'config.yaml').exists():
                projects.append(p.name)
        return projects
    
    def get_project_config(self, project_name):
        """获取项目配置"""
        config_path = self.projects_dir / project_name / 'config.yaml'
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return None
    
    def analyze_translation_progress(self, project_name):
        """分析翻译进度"""
        project_dir = self.projects_dir / project_name
        config = self.get_project_config(project_name)
        
        if not config:
            print(f"错误: 无法读取项目 {project_name} 的配置")
            return
        
        source_type = config.get('source', {}).get('type', 'markdown')
        extensions = {
            'latex': ['*.tex'],
            'markdown': ['*.md'],
        }
        
        total_files = 0
        translated_files = 0
        
        for ext in extensions.get(source_type, ['*.md']):
            for file_path in project_dir.rglob(ext):
                if '.git' in file_path.parts:
                    continue
                total_files += 1
                # 简单检测：文件是否包含中文
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if any('一' <= c <= '鿿' for c in content):
                            translated_files += 1
                except:
                    pass
        
        progress = (translated_files / total_files * 100) if total_files > 0 else 0
        print(f"\n翻译进度: {translated_files}/{total_files} 文件 ({progress:.1f}%)")
        return progress
    
    def check_terms_consistency(self, project_name):
        """检查术语一致性"""
        project_dir = self.projects_dir / project_name
        terms_path = project_dir / 'terms.yaml'
        
        if not terms_path.exists():
            print(f"警告: 项目 {project_name} 没有术语表")
            return
        
        # 这里可以调用 check_terms.py
        print(f"术语检查: {project_name}")
    
    def build_project(self, project_name):
        """构建项目"""
        project_dir = self.projects_dir / project_name
        
        # 读取配置
        config = self.get_project_config(project_name)
        if not config:
            print(f"错误: 无法读取项目 {project_name} 的配置")
            return False
        
        # 根据配置执行构建
        build_config = config.get('build', {})
        build_command = build_config.get('command', '')
        
        if build_command:
            print(f"执行构建命令: {build_command}")
            os.system(f"cd {project_dir} && {build_command}")
            return True
        
        # 默认构建逻辑
        if (project_dir / 'Makefile').exists():
            print("使用 make 构建...")
            os.system(f"cd {project_dir} && make")
            return True
        elif (project_dir / 'export_book.py').exists():
            print("使用 pandoc 构建...")
            os.system(f"cd {project_dir} && python3 export_book.py && xelatex book.tex")
            return True
        
        print("错误: 未检测到构建配置")
        return False

if __name__ == '__main__':
    workflow = TranslationWorkflow(Path(__file__).parent.parent)
    
    if len(sys.argv) < 2:
        print("用法: translate_workflow.py <command> [project_name]")
        print("命令: list, progress, check, build")
        sys.exit(1)
    
    command = sys.argv[1]
    project_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    if command == 'list':
        projects = workflow.list_projects()
        print(f"\n可用项目 ({len(projects)}):")
        for p in projects:
            print(f"  - {p}")
    
    elif command == 'progress':
        if not project_name:
            print("错误: 请指定项目名称")
            sys.exit(1)
        workflow.analyze_translation_progress(project_name)
    
    elif command == 'check':
        if not project_name:
            print("错误: 请指定项目名称")
            sys.exit(1)
        workflow.check_terms_consistency(project_name)
    
    elif command == 'build':
        if not project_name:
            print("错误: 请指定项目名称")
            sys.exit(1)
        workflow.build_project(project_name)
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)
