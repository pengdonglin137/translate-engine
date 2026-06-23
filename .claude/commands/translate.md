全自动翻译 — 严格串行，零干预。

## 输入

$ARGUMENTS 是项目名（如 `perfbook`）。

## 执行规则

**严格串行：一次只翻译一个文件，翻译完一个再开始下一个。禁止并行。**

## 执行流程

### Step 1: 定位与配置
1. 定位 `projects/<name>/`
2. 如果 config.yaml 不存在 → 自动分析生成
3. 读取 config.yaml，获取 `domains` 配置

### Step 2: 加载分层规则
按顺序加载：

**第一层：全局规则**
- 读取 `conventions/rules/global.md`

**第二层：领域规则**（根据 config.yaml domains 加载）
- `technical` → `conventions/domains/technical.md`
- `academic` → `conventions/domains/academic.md`
- `literary` → `conventions/domains/literary.md`

**第三层：项目规则**
- 读取 `conventions/style/xinyada.md`
- 读取 `projects/<name>/terms.yaml`

### Step 3: 扫描未翻译文件
1. 根据 source.type 扫描源文件
2. 计算翻译率，筛选 < 95% 的文件
3. 按翻译率升序排列

### Step 4: 严格串行翻译
对列表中的每个文件：
1. 读取文件（200-300 行为一批）
2. 逐段翻译，综合应用所有已加载的规则
3. 用 Edit 工具写入
4. **确认当前文件完成后再处理下一个文件**
5. **禁止同时处理多个文件**

### Step 5: 术语自动修复
1. 运行 check_terms.py
2. 对每个问题，逐个修复（Edit）
3. 修复后重新检查，循环直到通过

### Step 6: 构建
1. 读取 build.command
2. 执行构建，失败则分析错误重试一次

### Step 7: 输出报告
翻译了几个文件、术语检查结果、构建结果。

---

## 规则优先级

```
项目 terms.yaml（最高）
  ↑
领域规则（technical/academic/literary）
  ↑
全局规则 global.md（最低）
```
