# H5P 多智能体架构

## 愿景

一个智能系统，能够根据任何学习材料（主题、练习题、学习单元）自动生成最佳的 H5P 内容——从简单的测验到复杂的互动式图书。

## 架构概览

```
┌───────────────────────────────────────────────────────────────────────┐
│                           编排（Orchestrator）Agent                    │
│                                                                       │
│  输入：主题 / 工作表 / 学习单元 / 文档                                   │
│                                                                       │
│  阶段 1：分析                                                          │
│  ├── 提取学习目标                                                      │
│  ├── 识别认知操作词（列举、匹配、解释……）                                │
│  ├── 识别内容结构（事实、分类、时间顺序……）                              │
│  └── 评估复杂度（简单 → 复杂）                                          │
│                                                                       │
│  阶段 2：规划                                                          │
│  ├── 应用决策矩阵                                                      │
│  ├── 选择 H5P 类型（单一类型 + 容器类型）                               │
│  ├── 制定执行计划                                                      │
│  └── 分配子 Agent                                                     │
│                                                                      │
│  阶段 3：协调                                                         │
│  ├── 并行启动各子 Agent                                               │
│  ├── 监控执行进度                                                     │
│  ├── 处理错误（重试、回退）                                            │
│  └── 汇总结果                                                         │
└──────────────────────────────────────────────────────────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            ▼                       ▼                       ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│     QUIZ Agent      │  │     CARD Agent      │  │     DRAG Agent      │
│                     │  │                     │  │                     │
│  专长：             │  │  专长：              │  │  专长：             │
│  • 判断题           │  │  • Flashcards       │  │  • Drag & Drop      │
│  • 选择题           │  │  • Accordion        │  │  • Drag the Words   │
│  • 单选题           │  │  • Timeline         │  │  • Mark the Words   │
│  • Summary          │  │  • Memory Game      │  │  • Fill in Blanks  │
│                     │  │                     │  │                    │
│  自我修正：          │  │  自我修正：           │  │  自我修正：         │
│  • 验证              │  │  • 验证              │  │  • 验证             │
│  • 自动重试          │  │  • 自动重试           │  │  • 自动重试         │
│  • 回退类型          │  │  • 回退类型           │  │  • 回退类型         │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           COMBINER Agent                                │
│                                                                         │
│  将单个 H5P 元素组合为复杂的容器类型：                                     │
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │
│  │ Course          │  │ Column          │  │ Interactive     │          │
│  │ Presentation    │  │                 │  │ Book            │          │
│  │                 │  │                 │  │                 │          │
│  │ 包含嵌入式       │  │ 垂直排列多个     │  │ 按章节组织，     │          │
│  │ H5P 元素的幻灯片 │  │ H5P 元素        │  │ 包含页面和子内容  │          │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘          │
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐                               │
│  │ Question Set    │  │ Branching       │                               │
│  │                 │  │ Scenario        │                               │
│  │ 一系列          │   │                │                                │
│  │ 测验题目        │   │ 分支式学习路径   │                               │
│  └─────────────────┘  └─────────────────┘                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────┐
                        │        输出           │
                        │                       │
                        │   📦 .h5p 文件        │
                        │   📋 生成报告         │
                        │   💾 模板更新         │
                        └───────────────────────┘
```

---

## 组件详解

### 1. 编排代理

**职责：** 集中控制整个工作流

#### 1.1 分析阶段

```python
class ContentAnalysis:
    """内容分析结果"""
    learning_goals: list[str]        # 提取学习目标
    operators: list[str]             # 名称、分配、解释……
    content_structure: str           # 事实、类别、时间顺序、流程
    complexity: str                  # 简单、中等、复杂
    estimated_elements: int          # 预估 H5P 单项元素数量
    suggested_container: str | None  # 列、课程演示、图书
```

**操作识别：**

| 操作 | 识别模式 | 推荐的 H5P 内容类型 |
|----------|------------------|----------------|
| 名称 | "名称", "列表", "计数" | Flashcards |
| 描述 | "描述", "简要解释" | True/False, Summary |
| 分配 | "分配", "类别" | Drag & Drop |
| 解释 | "解释", "论证" | Accordion |
| 排序 | "按时间顺序排序", "顺序" | Timeline |
| 添加 | "添加", "填写" | Fill Blanks, Drag Text |
| 标记 | "标记", "标签" | Mark Words |
| 评估 | "评估", "决策" | Branching Scenario |

#### 1.2 规划阶段

```python
class ExecutionPlan:
    """子代理的执行计划"""
    elements: list[PlannedElement]   # 已规划的 H5P 元素
    container: ContainerConfig       # 容器类型配置
    execution_order: list[str]       # 执行顺序
    dependencies: dict[str, list]    # 元素之间的依赖关系
```

**决策矩阵：**

```
输入复杂度 → 容器推荐
──────────────────────────────────────────────
1 个学习目标，1 个操作     → 单个 H5P 元素
2-3 个学习目标，2-3 个操作 → Column
3-5 个学习目标，混合式     → Course Presentation
5 个以上学习目标，结构化   → Interactive Book
l选择路径                 → Branching Scenario
```

#### 1.3 协调阶段

```python
async def coordinate_generation(plan: ExecutionPlan):
    """并行执行并处理错误"""

    # 阶段 1：并行生成各个元素
    tasks = [
        generate_element(e) for e in plan.elements
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 阶段 2：处理错误
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            # 使用回退类型重试
            results[i] = await retry_with_fallback(plan.elements[i])

    # 阶段 3：如果计划要创建容器，则创建
    if plan.container:
        return await combine_elements(results, plan.container)

    return results
```

---

### 2. 子代理

#### 2.1 测验代理

**专精：** 选择合适的测验题型

| 类型 | 适用场景 | 验证 |
|-----|----------------|-------------|
| True/False | 检查事实 | 至少 2 个陈述 |
| Multiple Choice | 多个选项，详细知识 | 至少 1 个正确答案 |
| Single Choice | 快速决策 | 恰好 1 个正确答案 |
| Summary | 识别关键信息 | 至少 2 组陈述 |

**自我纠错：**
```python
def validate_and_correct(self, result: H5PResult) -> H5PResult:
    if not result.success:
        回退：如果数量过多，则选择多选题 → 单选题选项较少
        if self.type == "multi_choice" and self.error == "not_enough_options":
            return self.generate_as_single_choice()
    return result
```

#### 2.2 卡片代理

**专精：** 闪卡和结构化信息

| 类型 | 适用场景 | 验证 |
|-----|----------------|-------------|
| Flashcards | 词汇、定义、术语 | 至少 3 张卡片 |
| Accordion | 解释、常见问题解答、结构 | 至少 2 项 |
| Timeline | 时间顺序、历史、流程 | 至少 2 个带日期的事件 |
| Memory | 视觉匹配、游戏化 | 至少 4 对图像 |

**自我纠错：**
```python
def validate_and_correct(self, result: H5PResult) -> H5PResult:
    if self.type == "timeline" and not self.has_valid_dates():
        # 回退：如果没有时间数据，则改用 Accordion
        return self.generate_as_accordion()
    return result
```

#### 2.3 拖拽代理

**专精：** 交互式匹配

| 类型 | 适用场景 | 验证 |
|-----|----------------|-------------|
| Drag & Drop | 类别、分类 | 至少 2 个放置区域，3 个可拖拽元素 |
| Drag Text | 用拖拽代替输入进行填空练习 | 至少 2 个空格 |
| Mark Words | 识别文本 | 至少选择 2 个单词 |
| Fill Blanks | 填空练习（需输入内容） | 至少填入 1 个空格 |

**自我纠错：**
```python
def validate_and_correct(self, result: H5PResult) -> H5PResult:
    if self.type == "drag_drop" and self.dropzones_outside_canvas():
        # 自动修复：修正坐标
        return self.regenerate_with_fixed_coordinates()
    return result
```

---

### 3. 组合代理

**职责：** 将单个元素组合成复杂类型

#### 3.1 容器类型

##### 列（最简单组合）

```json
{
  "mainLibrary": "H5P.Column",
  "content": [
    { "library": "H5P.AdvancedText", "params": {...} },
    { "library": "H5P.MultiChoice", "params": {...} },
    { "library": "H5P.DragQuestion", "params": {...} }
  ]
}
```

**应用：** 垂直放置 2-5 个元素

##### Course Presentation（幻灯片）

```json
{
  "mainLibrary": "H5P.CoursePresentation",
  "slides": [
    {
      "elements": [
        { "library": "H5P.AdvancedText", "x": 0, "y": 0 },
        { "library": "H5P.Image", "x": 50, "y": 0 }
      ]
    },
    {
      "elements": [
        { "library": "H5P.MultiChoice", "x": 0, "y": 0 }
      ]
    }
  ]
}
```

**应用：** 演示文稿、带导航的教程

##### Interactive Book（章节）


```json
{
  "mainLibrary": "H5P.InteractiveBook",
  "chapters": [
    {
      "title": "说明",
      "content": [
        { "library": "H5P.AdvancedText", "params": {...} }
      ]
    },
    {
      "title": "练习",
      "content": [
        { "library": "H5P.QuestionSet", "params": {...} }
      ]
    }
  ]
}
```

**应用：** 包含章节的综合学习单元

##### Question Set（测验序列/试卷）

```json
{
  "mainLibrary": "H5P.QuestionSet",
  "questions": [
    { "library": "H5P.MultiChoice", "params": {...} },
    { "library": "H5P.TrueFalse", "params": {...} },
    { "library": "H5P.DragText", "params": {...} }
  ],
  "passPercentage": 70,
  "showResults": true
}
```

**应用：** 小测验，考试

#### 3.2 容器类型选择

```python
def choose_container(elements: list, structure: str) -> str | None:
    """选择最佳容器类型"""

    count = len(elements)

    if count == 1:
        return None  # 不需要容器

    if count <= 3 and structure == "sequential":
        return "column"

    if structure == "presentation" or count <= 5:
        return "course_presentation"

    if structure == "chapters" or count > 5:
        return "interactive_book"

    if all(is_quiz_type(e) for e in elements):
        return "question_set"

    return "column"  # 默认容器类型
```

---

## 实施计划

### 第一阶段：基础 ✅ 已完成

| 任务 | 描述 | 状态 |
|------|--------------|--------|
| 1.1 | 带有分析逻辑的 Orchestrator 类 | ✅ |
| 1.2 | 带有自纠错功能的子代理基类 | ✅ |
| 1.3 | 实现测验代理 | ✅ |
| 1.4 | 实现卡片代理 | ✅ |
| 1.5 | 实现拖拽代理 | ✅ |

### 第二阶段：设计与品牌样式 ✅ 已完成

| 任务 | 描述 | 状态 |
|------|--------------|--------|
| 2.1 | 使用预设样式进行品牌样式设置 | ✅ |
| 2.2 | 实现设计代理 | ✅ |
| 2.3 | 集成到 Orchestrator | ✅ |
| 2.4 | 6 个品牌样式预设（bswi、minimal、dark 等） | ✅ |

### 第三阶段：系统集成 ✅ 已完成

| 任务 | 描述 | 状态 |
|------|--------------|--------|
| 3.1 | H5PSystem 统一 API | ✅ |
| 3.2 | CLI 界面 | ✅ |
| 3.3 | 便捷功能 | ✅ |
| 3.4 | 集成测试（10/10 通过） | ✅ |

### 第四阶段：容器类型（计划中）

| 任务 | 描述 | 状态 |
|------|--------------|--------|
| 4.1 | Column 生成器 | ⬜ |
| 4.2 | Question Set 生成器 | ⬜ |
| 4.3 | Course Presentation 生成器 | ⬜ |
| 4.4 | 组合代理逻辑 | ⬜ |

---

## 示例工作流程

### 输入

```markdown
# Scrum 简介

## 学习目标
- 学生能够说出三个 Scrum 角色
- 学生能够为这些角色分配任务
- 学生能够解释 Sprint 流程

## 内容
- 产品负责人：确定待办事项列表的优先级，定义 User Stories
- Scrum 主持人：排除障碍，主持会议
- 开发团队：开发功能，评估工作量

## Sprint 阶段
1. Sprint 计划会议（第 1 天）
2. 每日站会（每天）
3. Sprint 评审会议（最后一天）
4. Sprint 回顾会议（最后一天）
```

### 编排分析

```python
ContentAnalysis(
    learning_goals=[
        "说出 Scrum 角色名称",
        "能合理分配任务",
        "解释 Sprint 流程"
    ],
    operators=["名称", "分配", "解释"],
    content_structure="mixed",
    complexity="medium",
    estimated_elements=4,
    suggested_container="course_presentation"
)
```

### 执行计划

```python
ExecutionPlan(
    elements=[
        PlannedElement(type="flashcards", agent="card", content="角色定义"),
        PlannedElement(type="drag_drop", agent="drag", content="任务分配"),
        PlannedElement(type="timeline", agent="card", content="冲刺阶段"),
        PlannedElement(type="summary", agent="quiz", content="要点")
    ],
    container=ContainerConfig(type="course_presentation", slides=4),
    execution_order=["parallel:all", "combine"]
)
```

### 输出

```
📦 scrum-einfuehrung.h5p
   └── Course Presentation （4 张幻灯片）
       ├── Slide 1: Flashcards （3 个角色）
       ├── Slide 2: Drag & Drop （任务 → 角色）
       ├── Slide 3: Timeline （Sprint 阶段）
       └── Slide 4: Summary （要点）
```

---

## 文件结构

```
h5p-generator/
├── scripts/
│   ├── __init__.py               # Package exports
│   ├── h5p_generator.py          # 基础生成器（12 种类型）
│   ├── h5p_system.py             # ✅ 统一 API（主入口点）
│   ├── cli.py                    # ✅ 命令行界面
│   ├── orchestrator.py           # ✅ 编排代理
│   ├── brand_config.py           # ✅ 品牌预设配置预设
│   ├── agent_workflow.py         # 旧版代理（已弃用）
│   ├── sub_agents/               # ✅ 子代理
│   │   ├── __init__.py
│   │   ├── base_agent.py         # 带自纠错功能的基类
│   │   ├── quiz_agent.py         # True/False, MultiChoice, Summary
│   │   ├── card_agent.py         # Flashcards, Accordion, Timeline
│   │   ├── drag_agent.py         # Drag&Drop, DragText, MarkWords
│   │   └── design_agent.py       # ✅ 应用品牌样式预设/CI
│   ├── test_integration.py       # ✅ 集成测试
│   └── combiner.py               # TODO: 容器组合器
├── references/
│   ├── templates/
│   │   ├── decision-matrix.md
│   │   └── saved/
│   └── h5p-json-structure.md
├── test-output/                  # 生成的 H5P 文件
├── SKILL.md
├── AGENT_WORKFLOW.md
└── MULTI_AGENT_ARCHITECTURE.md   # 此文件
```

## 当前系统架构 (v2.0)

```
                    ┌─────────────────────────┐
                    │      H5PSystem          │  ← Unified API
                    │   (h5p_system.py)       │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │         H5POrchestrator           │
              │      (orchestrator.py)            │
              │  分析 → 计划 → 执行 → 设计│
              └─────────────────┬─────────────────┘
                                │
        ┌───────────┬───────────┼───────────┬───────────┐
        │           │           │           │           │
        ▼           ▼           ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
   │  Quiz   │ │  Card   │ │  Drag   │ │ Design  │ │ Combiner│
   │  代理   │ │  代理    │ │  代理   │ │  代理    │ │ (TODO)  │
   └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
        │           │           │           │
        └───────────┴───────────┴───────────┘
                        │
                        ▼
              ┌─────────────────────┐
              │  Brand Presets      │
              │  (brand_config.py)  │
              │  bswi, minimal,     │
              │  dark, professional │
              └─────────────────────┘
```

---

## 成功标准
| 标准 | 衡量指标 | 目标值 |
|-----------|---------|------|
| H5P 内容类型选择正确率 | 操作 → 类型匹配 | >90% |
| 生成成功率 | 无错误的 H5P 文件 | >95% |
| 自我纠错率 | 自动修正错误 | >80% |
| 容器质量 | 有效组合 | >85% |
| 生成速度 | 生成H5P文件所用时间 | <30s |

---

## 快速入门

### Python API

```python
from scripts import H5PSystem

# 最简用法
system = H5PSystem(brand='bswi')
result = system.generate_from_text('''
## 学习目标
- 学生能够命名 Scrum 角色
''', content_items=[
    {'cards': [
        {'front': 'PO', 'back': '产品负责人'},
        {'front': 'SM', 'back': 'Scrum Master'},
    ]}
])

print(result.summary()
```

### CLI

```bash
# 系统信息
python cli.py info

# 从文件生成带品牌标识的内容
python cli.py generate -f lerneinheit.md -b bswi

# 批量生成
python cli.py batch elements.json -o ./output

# 显示指定品牌样式详情
python cli.py brands bswi

# H5P 内容类型信息
python cli.py types flashcards
```

### 快速函数

```python
from scripts import quick_flashcards, quick_quiz, quick_drag_drop

# 快速闪卡
result = quick_flashcards('词汇', [
    {'front': 'house', 'back': '房子'},
    {'front': 'car', 'back': '汽车'},
], brand='bswi')

# 快速测验
result = quick_quiz('测试', [
    {'text': 'Python 是一种编程语言。', 'correct': True}
])

# 快速 Drag & Drop
result = quick_drag_drop('作业',
    dropzones=['A', 'B'],
    draggables=[{'text': 'Item1', 'dropzone': 0}]
)
```

---

## 品牌样式预设

| 预设 | 描述 | 主色 |
|--------|--------------|---------------|
| `default` | 默认主题 | #1a73e8 |
| `bswi` | BS:WI Hamburg | #003366 |
| `minimal` | 极简 | #333333 |
| `dark` | 深色模式 | #8ab4f8 |
| `professional` | 商务 | #1976d2 |
| `accessible` | 高对比度 | #0000ff |

--

## 更新日志

### v2.0.0（当前版本）
- ✅ H5P 系统统一 API
- ✅ 包含所有命令的 CLI 界面
- ✅ 品牌样式设计代理
- ✅ 6 个品牌样式预设
- ✅ 通过 10 项集成测试
- ✅ 便捷功能

### v1.0.0
- ✅ 包含分析/计划/执行功能的编排器
- ✅ 测验代理、卡片代理、拖拽代理
- ✅ 包含 12 种 H5P 类型的基础生成器
- ✅ 自我纠错和回退逻辑

### v0.1（规划阶段）
- 已创建架构文档
- 已制定实施计划
- 已编写示例工作流程文档

---

*多代理 H5P 生成系统 v2.0 - 文档*
