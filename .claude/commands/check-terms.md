术语检查 + 自动修复，零干预。

## 输入

$ARGUMENTS 是项目名（如 `perfbook`）。

## 执行流程（不询问用户）

1. 运行 `python scripts/check_terms.py --project projects/<name> --verbose`
2. 如果没有问题 → 输出"通过"，结束
3. 如果有问题 → 对每个问题：
   - 读取 terms.yaml 获取正确译文
   - 用 Edit 工具将英文术语替换为中文
4. 修复后重新检查
5. 重复直到通过或连续两次无新修复
6. 输出：修复了几个问题，最终状态
