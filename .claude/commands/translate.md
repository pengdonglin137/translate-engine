全自动翻译 — 零干预，分层规则，一键完成。

## 输入

$ARGUMENTS 是项目名（如 `perfbook`）。

## 执行流程（不可中断，不询问用户）

### Step 1: 定位与配置
1. 定位 `projects/<name>/`
2. 如果 config.yaml 不存在 → 自动分析生成
3. 读取 config.yaml，获取 `domains` 配置

### Step 2: 加载分层规则
按顺序加载，后者覆盖前者：

**第一层：全局规则（必须加载）**
- 读取 `conventions/rules/global.md`
- 信雅达标准、翻译腔消除、术语一致性、质量评分

**第二层：领域规则（根据 config.yaml domains 加载）**
- 读取 `conventions/domains/<domain>.md`
- 每个 domain 加载对应文件：
  - `technical` → 技术文档规则（格式处理、代码保留、术语参考）
  - `academic` → 学术论文规则（引用保留、学术术语）
  - `literary` → 文学翻译规则（风格再现、文化适配）
- 可多选，全部加载

**第三层：项目规则**
- 读取 `conventions/style/xinyada.md`（信雅达标准详解）
- 读取 `projects/<name>/terms.yaml`（项目术语表）

### Step 3: 扫描未翻译文件
1. 根据 source.type 扫描源文件
2. 计算翻译率，筛选 < 95% 的文件
3. 按翻译率升序排列

### Step 4: 翻译
对每个未完成的文件：
1. 读取文件
2. 逐段翻译，综合应用所有已加载的规则
3. 用 Edit 工具写入
4. 翻译完一个立即进入下一个

### Step 5: 术语自动修复
1. 运行 check_terms.py
2. 自动修复发现的问题
3. 重试直到通过

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

当规则冲突时，项目规则优先于领域规则，领域规则优先于全局规则。
术语表（terms.yaml）是最终权威。
