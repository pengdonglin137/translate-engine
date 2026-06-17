构建 PDF，零干预。

## 输入

$ARGUMENTS 是项目名（如 `perfbook`）。

## 执行流程（不询问用户）

1. 读取 `projects/<name>/config.yaml` 的 build.command
2. 如果为空，根据 source.type 选择默认命令（latex → make 1c）
3. 执行构建
4. 成功 → 报告 PDF 路径、大小、页数
5. 失败 → 分析错误，尝试修复后重试一次
