#!/usr/bin/env python3
"""
AI 翻译质量保障工具

提供术语一致性检查和构建验证。

用法:
    python translate.py list                              # 列出所有项目
    python translate.py init <name>                       # 初始化新项目
    python translate.py --project <dir> check             # 术语检查
    python translate.py --project <dir> build             # 构建 PDF
    python translate.py --project <dir> all               # 检查 + 构建
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


# 引擎根目录（scripts/ 的父目录）
ENGINE_DIR = Path(__file__).resolve().parent.parent


def run_command(cmd, check: bool = True, shell: bool = False, cwd: str = None) -> tuple:
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check,
            shell=shell,
            cwd=cwd
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr


def find_projects() -> list:
    """查找 projects/ 下的所有翻译项目"""
    projects_dir = ENGINE_DIR / 'projects'
    if not projects_dir.exists():
        return []

    projects = []
    for item in sorted(projects_dir.iterdir()):
        if item.is_dir() and (item / 'config.yaml').exists():
            projects.append(item)
    return projects


def resolve_project(project_arg: str, require_config: bool = True) -> Path:
    """解析项目路径"""
    project_dir = Path(project_arg)
    if not project_dir.is_absolute():
        candidates = [
            ENGINE_DIR / 'projects' / project_dir,
            Path.cwd() / project_dir,
            project_dir,
        ]
        for candidate in candidates:
            if candidate.is_dir():
                if not require_config or (candidate / 'config.yaml').exists():
                    return candidate
        if require_config:
            print(f"错误: 找不到项目 '{project_arg}'（尝试了 projects/{project_arg} 等路径）")
        else:
            print(f"错误: 项目目录 '{project_arg}' 不存在")
        sys.exit(1)

    if not project_dir.is_dir():
        print(f"错误: 项目目录 {project_dir} 不存在")
        sys.exit(1)

    return project_dir


def cmd_list(args):
    """列出所有翻译项目"""
    projects = find_projects()

    if not projects:
        print("未找到翻译项目。")
        print(f"将项目添加为 submodule:")
        print(f"  cd {ENGINE_DIR}")
        print(f"  git submodule add <repo-url> projects/<name>")
        return 0

    print(f"\n翻译项目 ({len(projects)} 个):")
    print("=" * 50)

    for proj in projects:
        name = proj.name
        config_path = proj / 'config.yaml'

        try:
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            title = config.get('project', {}).get('title_translated',
                     config.get('project', {}).get('name', name))
        except Exception:
            title = name

        print(f"\n  📁 {name}")
        print(f"     标题: {title}")
        print(f"     路径: {proj.relative_to(ENGINE_DIR)}")

    print()
    return 0


def cmd_init(args):
    """初始化新项目"""
    project_name = args.name
    projects_dir = ENGINE_DIR / 'projects'
    project_dir = projects_dir / project_name

    if project_dir.exists():
        print(f"错误: 项目 {project_name} 已存在于 {project_dir}")
        return 1

    templates_dir = ENGINE_DIR / 'templates'
    project_dir.mkdir(parents=True, exist_ok=True)

    for template_file in ['config.yaml', 'CLAUDE.md']:
        src = templates_dir / template_file
        dst = project_dir / template_file
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✓ 创建 {template_file}")

    # 创建空的 terms.yaml
    terms_dst = project_dir / 'terms.yaml'
    terms_dst.write_text(
        'version: "1.0"\nlanguage: zh-CN\nterms:\n',
        encoding='utf-8'
    )
    print(f"  ✓ 创建 terms.yaml")

    print(f"\n✓ 项目 {project_name} 已创建在 {project_dir}")
    print(f"  编辑 config.yaml 和 terms.yaml 配置项目")
    print(f"  运行 python scripts/translate.py --project {project_name} check 运行术语检查")
    return 0


def cmd_check(args):
    """术语一致性检查"""
    project_dir = Path(args.project)

    print("🔍 运行术语一致性检查...")
    print("=" * 50)

    rc, stdout, stderr = run_command(
        ['python3', str(ENGINE_DIR / 'scripts' / 'check_terms.py'),
         '--project', str(project_dir)] +
        (['--verbose'] if args.verbose else []),
        check=False
    )
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)

    return rc


def cmd_build(args):
    """构建 PDF"""
    project_dir = Path(args.project)

    # 读取配置
    try:
        import yaml
        with open(project_dir / 'config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        config_path = project_dir / 'config.yaml'
        print(f"错误: 无法读取配置 {config_path}: {e}")
        return 1

    build_config = config.get('build', {})
    custom_command = build_config.get('command', '').strip()
    source_type = config.get('source', {}).get('type', 'latex')

    # 确定构建命令
    if custom_command:
        build_cmd = custom_command
    elif source_type == 'latex':
        build_cmd = 'make 1c'
    elif source_type == 'markdown':
        build_cmd = 'echo "请手动构建 markdown 项目"'
    else:
        build_cmd = 'echo "请手动构建此类型项目"'

    print(f"🔨 构建 PDF ({build_cmd})...")
    print("=" * 50)

    # 执行构建命令（支持 shell 管道等）
    rc, stdout, stderr = run_command(build_cmd, check=False, shell=True,
                                     cwd=str(project_dir))
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)

    if rc == 0:
        print(f"\n✅ 构建成功")
    else:
        print(f"\n❌ 构建失败 (exit code: {rc})")

    return rc


def cmd_all(args):
    """术语检查 + 构建"""
    # 先检查术语
    rc = cmd_check(args)
    # 再构建（不询问，直接继续）
    return cmd_build(args)


def cmd_analyze(args):
    """分析项目结构，生成 config.yaml 和 terms.yaml"""
    project_dir = Path(args.project)

    print(f"🔍 分析项目: {project_dir.name}")
    print("=" * 50)

    # Phase 1: 扫描文件类型
    extensions = {}
    for f in project_dir.rglob('*'):
        if f.is_file() and not any(p.startswith('.') for p in f.relative_to(project_dir).parts):
            ext = f.suffix.lower()
            extensions[ext] = extensions.get(ext, 0) + 1

    print("\n📁 文件类型统计:")
    for ext, count in sorted(extensions.items(), key=lambda x: -x[1])[:10]:
        print(f"  {ext or '(无后缀)'}: {count} 个")

    # 检测源文件类型
    source_type = 'latex'
    if extensions.get('.tex', 0) > 0:
        source_type = 'latex'
    elif extensions.get('.md', 0) > 0:
        source_type = 'markdown'
    elif extensions.get('.rst', 0) > 0:
        source_type = 'rst'
    elif extensions.get('.docx', 0) > 0:
        source_type = 'word'
    print(f"\n  → 检测到 source.type: {source_type}")

    # Phase 2: 检测构建系统
    build_command = ''
    if (project_dir / 'Makefile').exists():
        # 读取 Makefile 找 PDF 构建目标
        makefile_content = (project_dir / 'Makefile').read_text(errors='ignore')
        if '1c' in makefile_content:
            build_command = 'make 1c'
        elif 'pdf' in makefile_content.lower():
            build_command = 'make pdf'
        else:
            build_command = 'make'
        print(f"  → 检测到 Makefile, build.command: {build_command}")
    elif (project_dir / 'CMakeLists.txt').exists():
        build_command = 'cmake --build build'
        print(f"  → 检测到 CMakeLists.txt")
    elif source_type == 'markdown':
        build_command = 'pandoc -o output.pdf'
        print(f"  → Markdown 项目, build.command: {build_command}")

    # Phase 3: 检测 LaTeX 引擎
    engine = 'pdflatex'
    if source_type == 'latex':
        for tex_file in project_dir.glob('*.tex'):
            try:
                content = tex_file.read_text(errors='ignore')[:5000]
                if 'xeCJK' in content or 'ctex' in content or 'fontspec' in content:
                    engine = 'xelatex'
                    break
            except Exception:
                pass
        print(f"  → LaTeX 引擎: {engine}")

    # Phase 4: 提取 git 信息
    upstream = ''
    branch = 'master'
    try:
        import subprocess
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'],
                               capture_output=True, text=True, cwd=str(project_dir))
        if result.returncode == 0:
            upstream = result.stdout.strip()
            print(f"  → upstream: {upstream}")
        result = subprocess.run(['git', 'branch', '-r', '--list', 'origin/main'],
                               capture_output=True, text=True, cwd=str(project_dir))
        if result.returncode == 0 and result.stdout.strip():
            branch = 'main'
    except Exception:
        pass

    # Phase 5: 读取项目信息
    title = project_dir.name
    author = ''
    license_type = ''

    # 尝试从 README 获取信息
    for readme_name in ['README.md', 'README.rst', 'README.txt', 'README']:
        readme_path = project_dir / readme_name
        if readme_path.exists():
            try:
                content = readme_path.read_text(errors='ignore')[:2000]
                lines = content.strip().split('\n')
                if lines:
                    # 第一个非空非标题行可能是描述
                    for line in lines:
                        if line.strip() and not line.startswith('#'):
                            title = line.strip()[:100]
                            break
            except Exception:
                pass
            break

    # 检查 LICENSE
    for license_name in ['LICENSE', 'LICENSE.md', 'COPYING']:
        if (project_dir / license_name).exists():
            try:
                content = (project_dir / license_name).read_text(errors='ignore')[:500]
                if 'MIT' in content:
                    license_type = 'MIT'
                elif 'GPL' in content:
                    license_type = 'GPL'
                elif 'Apache' in content:
                    license_type = 'Apache-2.0'
                elif 'BSD' in content:
                    license_type = 'BSD'
                elif 'CC' in content:
                    license_type = 'CC-BY-SA-3.0'
            except Exception:
                pass
            break

    # Phase 5.5: 检测领域类型
    domains = ['technical']  # 默认
    try:
        # 扫描文件内容判断领域
        has_code = False
        has_academic = False
        has_literary = False

        for tex_file in list(project_dir.rglob('*.tex'))[:20]:  # 采样前20个
            try:
                content = tex_file.read_text(errors='ignore')[:3000]
                if any(kw in content for kw in ['\\begin{lstlisting}', '\\begin{Verbatim}', '```', 'def ', 'class ', 'import ']):
                    has_code = True
                if any(kw in content for kw in ['\\begin{abstract}', '\\bibliography', '\\cite{', 'experiment', 'hypothesis']):
                    has_academic = True
                if any(kw in content for kw in ['\\chapter{', '"', '"', 'said', 'he said', 'she said']):
                    has_literary = True
            except Exception:
                pass

        if has_literary and not has_code:
            domains = ['literary']
        elif has_academic and not has_code:
            domains = ['academic']
        else:
            domains = ['technical']

        print(f"  → 领域类型: {', '.join(domains)}")
    except Exception:
        pass

    # Phase 6: 生成 config.yaml
    print(f"\n📄 生成 config.yaml...")
    domains_yaml = '\n'.join(f'  - {d}' for d in domains)
    config_content = f"""# {project_dir.name} 翻译项目配置
# 由 translate-engine 自动生成，请根据实际情况修改

project:
  name: "{project_dir.name}"
  title: "{title}"
  title_translated: ""  # TODO: 填写翻译标题
  author: "{author}"
  license: "{license_type}"
  version: ""

source:
  type: {source_type}
  upstream: "{upstream}"
  branch: {branch}
  sync_strategy: submodule

translation:
  target_language: zh-CN
  engine: {engine}

domains:
{domains_yaml}

terminology:
  file: terms.yaml
  auto_check: true

build:
  command: "{build_command}"
  targets: [pdf]
"""
    config_path = project_dir / 'config.yaml'
    if config_path.exists() and not args.force:
        print(f"  ⚠️  config.yaml 已存在，跳过（使用 --force 覆盖）")
    else:
        config_path.write_text(config_content, encoding='utf-8')
        print(f"  ✓ 写入 {config_path}")

    # Phase 7: 生成 terms.yaml
    print(f"\n📄 生成 terms.yaml...")
    terms_content = f"""# {project_dir.name} 术语表
# 由 translate-engine 自动生成，请根据实际情况修改

version: "1.0"
language: zh-CN

terms: []
  # 添加术语示例:
  # - en: "deadlock"
  #   zh: "死锁"
  # - en: "RCU"
  #   zh: "RCU"
  #   rule: "keep_english"
"""
    terms_path = project_dir / 'terms.yaml'
    if terms_path.exists() and not args.force:
        print(f"  ⚠️  terms.yaml 已存在，跳过（使用 --force 覆盖）")
    else:
        terms_path.write_text(terms_content, encoding='utf-8')
        print(f"  ✓ 写入 {terms_path}")

    print(f"\n✅ 项目分析完成")
    print(f"  编辑 config.yaml 填写 title_translated 等字段")
    print(f"  编辑 terms.yaml 添加术语映射")
    return 0


def main():
    parser = argparse.ArgumentParser(description='AI 翻译质量保障工具')
    parser.add_argument('--project', '-p', default=None, help='项目目录（相对于 projects/ 或绝对路径）')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # list 命令
    subparsers.add_parser('list', help='列出所有翻译项目')

    # init 命令
    init_parser = subparsers.add_parser('init', help='初始化新项目')
    init_parser.add_argument('name', help='项目名称')

    # analyze 命令
    analyze_parser = subparsers.add_parser('analyze', help='分析已有项目并生成配置')
    analyze_parser.add_argument('name', help='项目名称（projects/ 下的目录名）')
    analyze_parser.add_argument('-f', '--force', action='store_true', help='覆盖已有配置文件')

    # check 命令
    check_parser = subparsers.add_parser('check', help='术语一致性检查')
    check_parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')

    # build 命令
    subparsers.add_parser('build', help='构建 PDF')

    # all 命令
    all_parser = subparsers.add_parser('all', help='术语检查 + 构建')
    all_parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')

    args = parser.parse_args()

    # list、init、analyze 不需要 --project
    if args.command in ('list', 'init', 'analyze'):
        if args.command == 'list':
            return cmd_list(args)
        elif args.command == 'init':
            return cmd_init(args)
        elif args.command == 'analyze':
            args.project = str(resolve_project(args.name, require_config=False))
            return cmd_analyze(args)

    # 其他命令需要 --project
    if args.project is None:
        parser.error("--project 参数是必需的（list/init 除外）")

    args.project = str(resolve_project(args.project))

    if args.command == 'check':
        return cmd_check(args)
    elif args.command == 'build':
        return cmd_build(args)
    elif args.command == 'all':
        return cmd_all(args)
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    sys.exit(main())
