分析项目并生成配置，零干预。

## 输入

$ARGUMENTS 是项目名（如 `new-project`）。

## 执行流程（不询问用户）

1. 扫描 `projects/<name>/` 的文件结构
2. 检测 source.type（latex/markdown/word/rst）
3. 检测构建系统（Makefile/CMake/pandoc）
4. 检测 LaTeX 引擎（xelatex/pdflatex）
5. 检测领域类型：
   - 包含代码示例、API、配置 → `technical`
   - 包含摘要、参考文献、实验 → `academic`
   - 包含叙事、对话、诗歌 → `literary`
6. 读取 git remote、README、LICENSE
7. 自动生成 config.yaml（含 domains 配置）和 terms.yaml
8. 如果文件已存在 → 跳过
9. 输出生成结果
