---
name: h5p-generator
description: 使用 Python 编程生成 H5P 交互式内容文件 (.h5p)。支持 16 种内容类型、4 种容器类型、可视化验证以及 BS:WI 品牌定制。适用于测验、抽认卡、拖放、互动图书、课程演示、论述题、分支场景和交互式视频。
license: MIT
---

# H5P 生成器 v3.1
直接从 Python 生成 .h5p 文件，具备强大的错误处理、容器类型支持、可视化验证以及可自定义的品牌功能。

## 支持的内容类型 (16 种)
| 类型 | 函数 | 使用场景 |
| --- | --- | --- |
| True/False | `create_true_false()` | 判断题 |
| Multiple Choice | `create_multi_choice()` | 多选题 |
| Fill in Blanks | `create_fill_blanks()` | 填空题 |
| Drag and Drop | `create_drag_drop()` | 拖拽匹配 |
| Drag the Words | `create_drag_text()` | 拖拽填空 |
| Single Choice | `create_single_choice()` | 单选题 |
| Flashcards | `create_flashcards()` | 闪卡 |
| Mark Words | `create_mark_words()` | 在文本中标记词语 |
| Summary | `create_summary()` | 总结/摘要 |
| Accordion | `create_accordion()` | 可伸缩的段落/区块（手风琴样式） |
| Timeline | `create_timeline()` | 带有事件的时间线 |
| Memory Game | `create_memory_game()` | 记忆翻牌（需要图片） |
| Essay | `create_essay()` | 基于关键词评分的写作题（v3.1） |
| Sort Paragraphs | `create_sort_paragraphs()` | 段落排序（v3.1） |
| Branching Scenario | `create_branching_scenario()` | 条件分支场景（v3.1） |
| Interactive Video | `create_interactive_video()` | 交互式视频（v3.1） |

## 容器类型 (4 种) - v3.0 新增
| 容器 | 函数 | 使用场景 |
| --- | --- | --- |
| Column | `create_column()` | 2-5 个元素垂直排列 |
| QuestionSet | `create_question_set()` | 题目集合 |
| CoursePresentation | `create_course_presentation()` | 课程演示 |
| InteractiveBook | `create_interactive_book()` | 含章节的交互式图书（章节 = H5P.Column 包装器） |

### 容器推荐
| 场景 | 容器 |
| --- | --- |
| 2-3 种题型 | QuestionSet |
| 3-5 种混合类型 | Column |
| 4 种以上带章节结构的混合类型 | InteractiveBook |
| 课程演示 | CoursePresentation |

## 交互式图书 (v3.0)
每个章节都是一个 `H5P.Column 1.18` 包装器 - 所有 35+ 种兼容 Column 的类型均可使用：
```python
from h5p_containers import create_interactive_book

result = create_interactive_book(
    "Scrum 手册",
    chapters=[
        {
            "title": "第 1 章：角色",
            "elements": [
                {"library": "H5P.AdvancedText 1.1", "params": {"text": "<h2>角色</h2>"}},
                {"library": "H5P.Dialogcards 1.9", "params": {"dialogs": [...]}},
                {"library": "H5P.MultiChoice 1.16", "params": {"question": "...", "answers": [...]}}
            ]
        }
    ],
    cover_description="一本关于 Scrum 的书",
    base_color="#003366"  # BS:WI 海军蓝
)
```

### 课程演示 (v3.0)

带有嵌入式 H5P 类型的模板系统：

```python
from h5p_containers import create_course_presentation

result = create_course_presentation(
    "Scrum 课程演示",
    slides=[
        # 布局: title_only (简介)
        {"layout": "title_only", "title": "简介"},

        # 布局: text_content
        {"layout": "text_content", "title": "什么是 Scrum？", "content": "<p>...</p>"},

        # 布局: interactive (Text + H5P 元素)
        {
            "layout": "interactive",
            "title": "测验",
            "content": "<p>回答：</p>",
            "interactive": {
                "library": "H5P.TrueFalse 1.8",
                "params": {"question": "<p>Scrum 包含 3 个角色。</p>", "correct": "true"}
            }
        },

        # 布局: interactive_full (完整)
        {
            "layout": "interactive_full",
            "title": "任务",
            "interactive": {"library": "H5P.DragText 1.10", "params": {...}}
        },

        # 布局: split (左侧为文字，右侧为交互界面)
        {"layout": "split", "title": "练习", "content": "<p>信息</p>", "interactive": {...}}
    ]
)
```

**可用的幻灯片布局**：`title_only`, `text_content`, `interactive`, `interactive_full`, `split`

## 汉堡经济与国际事务职业学校（BS:WI） 设计 (v3.0)

```python
from h5p_system import H5PSystem

# 自动应用 BS:WI 品牌标识
system = H5PSystem(brand='bswi')
result = system.generate_from_text(...)
```

**颜色:**
- `#003366` 海军蓝：按钮、导航、标题
- `#00A3E0` 浅蓝色：链接、进度条、强调色
- `#B5E505` 黄色：成功提示、高亮
- `#333333` 灰色：文本颜色

**工作原理：** CSS 将作为 `<style>` 块注入到 H5P 内容中。InteractiveBook 将获得海军蓝导航栏和经过样式设计的章节标题。

## 可视化验证 (v3.0)

```python
from h5p_system import H5PSystem

system = H5PSystem(brand='bswi')

# 生成 + 自动验证
result = system.generate_and_verify(lernmaterial, content_items)
# result.statistics['verification'] 包含屏幕截图和检查结果

# 核实个人文件
from visual_verify import verify_h5p
vr = verify_h5p("path/to/file.h5p")
print(vr.summary())
# Screenshot: path/to/file_verify.png
```

**检查项：**
- 内容可见（非空）？
- 存在交互元素（按钮）？
- 无错误信息？
- 无重叠元素（CoursePresentation）？
- 存在导航（InteractiveBook）？

**前提条件：** Node.js + 在 `scripts/` 目录下执行 `npm install` (puppeteer-core, zip-lib)

## 统一 API (H5PSystem)

```python
from h5p_system import H5PSystem

system = H5PSystem(brand='bswi')

# 高层级：输入自由文本，输出 H5P
result = system.generate_from_text(lernmaterial, content_items)

# 高层级：文本转测验
result = system.generate_from_questions("X 是什么？ - A [correct] - B - C")

# 高层级：生成 + 验证
result = system.generate_and_verify(lernmaterial, content_items, combine=True)

# 中层级：结构化元素
result = system.generate_elements([
    {'type': 'flashcards', 'title': '词汇', 'cards': [...]},
    {'type': 'drag_drop', 'title': '任务', 'dropzones': [...], 'draggables': [...]}
])

# 低层级：直接使用 Agent
system.quiz_agent.generate('multi_choice', title='测验', questions=[...])
```

## 快速开始

```python
from h5p_generator import create_true_false, THEMES

result = create_true_false(
    "Python 基础",
    [
        {"text": "Python是一种编程语言。", "correct": True},
        {"text": "Python 诞生于 2020 年。", "correct": False}
    ],
    "python-quiz",
    style=THEMES['education']
)

if result.success:
    print(f"Erstellt: {result.path}")
```

## 内容类型详情

### 判断题
```python
questions = [
    {"text": "地球是圆的。", "correct": True},
    {"text": "HTML是一种编程语言。", "correct": False}
]
create_true_false("测验", questions, "quiz")
```

### 多选题
```python
questions = [
    {
        "question": "德国首都是哪里？",
        "answers": [
            {"text": "柏林", "correct": True},
            {"text": "汉堡", "correct": False}
        ]
    }
]
create_multi_choice("Staedte", questions, "staedte")
```

### 填空题
```python
text = "<p>首都是*柏林*。货币是*欧元*。</p>"
create_fill_blanks("德国", text, "de-luecken")
```

### 拖拽匹配
```python
dropzones = ["水果", "蔬菜"]
draggables = [
    {"text": "苹果", "dropzone": 0},
    {"text": "胡萝卜", "dropzone": 1}
]
create_drag_drop("杂货", "配对成功！", dropzones, draggables, "food")
```

### 拖拽填空
```python
text = "在 *Scrum* 中，团队以*迭代*的方式工作。"
create_drag_text("敏捷开发", text, "agile-drag", task="拖动这些术语。")
```

### 闪卡
```python
cards = [
    {"front": "Haus", "back": "house", "tip": "以 H 开头"},
    {"front": "Auto", "back": "car"}
]
create_flashcards("词汇", cards, "vokabeln")
```

### 可伸缩的段落/区块（手风琴样式）
```python
panels = [
    {"title": "简介", "content": "这是……"},
    {"title": "正文", "content": "详情……"}
]
create_accordion("学习单元", panels, "lerneinheit")
```

### 基于关键词评分的写作题 (v3.1)
```python
keywords = [
    {"keyword": "产品所有者", "alternatives": ["PO"], "points": 2},
    {"keyword": "敏捷开发培训师", "alternatives": ["SM"]},
    {"keyword": "开发团队"}
]
create_essay("敏捷开发角色", "请解释敏捷开发的三种角色。", keywords)
```

### 段落排序 (v3.1)
```python
# 顺序 = 正确顺序（H5P 自动随机乱序）
paragraphs = [
    "迭代计划会议：团队制定工作计划。",
    "每日站会：每天15分钟的会议。",
    "迭代回顾：展示结果。",
    "回顾：反思过程。"
]
create_sort_paragraphs("冲刺流程", paragraphs)
```

### 条件分支场景 (v3.1)
```python
nodes = [
    {"type": "text", "title": "开始", "content": "<p>顾客到了。</p>", "next": 1},
    {"type": "question", "question": "你会作何反应？",
     "alternatives": [
         {"text": "热情地打招呼", "next": 2},
         {"text": "忽视", "next": 3}
     ]},
    {"type": "text", "title": "好的", "content": "<p>顾客满意！</p>", "next": -1},
    {"type": "text", "title": "坏的", "content": "<p>顾客离开。</p>", "next": -1}
]
create_branching_scenario("顾客来了", nodes)
```
- `next: -1` = 结束（结束画面自动生成）
- 至少 2 个节点，建议至少 1 个问题节点。

### 交互式视频 (v3.1)
```python
interactions = [
    {
        "type": "multi_choice",
        "time_from": 30, "time_to": 40,
        "pause": True,
        "params": {
            "question": "<p>什么是Python？</p>",
            "answers": [
                {"text": "<p>编程语言</p>", "correct": True},
                {"text": "<p>蛇</p>", "correct": False}
            ]
        }
    }
]
create_interactive_video("教程", "https://youtube.com/watch?v=...", interactions)
```
- 仅限 URL：YouTube 或  MP4 文件  URL（不支持文件上传）
- 8 种交互类型：multi_choice, true_false, fill_blanks, drag_text, mark_words, single_choice, summary, text

## 品牌预设
| 预设 | 描述 |
| --- | --- |
| bswi | 汉堡经济与国际事务职业学校 BS:WI（海军蓝、浅蓝、黄色） |
| default | 标准（蓝色） |
| dark | 深色背景 |
| education | 绿色强调色 |
| professional | 商务 |
| minimal | 极简主义 |
| accessible | 高对比度 |

## 输出
- 文件位于 `./h5p-output/`
- 格式：`{name}.h5p`（ZIP 压缩包）
- 导入：Moodle H5P 活动、WordPress、Lumi

## 更新日志

### v3.1 (2026-03-02)
- **Essay**：基于关键词评分的写作题 (H5P.Essay 1.5)
- **Sort Paragraphs**：段落排序 (H5P.SortParagraphs 0.11)
- **Branching Scenario**：条件分支场景 (H5P.BranchingScenario 1.8)
- **Interactive Video**：交互式视频，支持 YouTube + MP4 (H5P.InteractiveVideo 1.27)
- **ScenarioAgent + MediaAgent**：用于条件分支场景和交互式视频内容的新子代理
- **QuizAgent**：扩展支持 Essay 和 SortParagraphs
- **16 种内容类型**（之前为 12 种），5 个子代理（之前为 3 个）

### v3.0 (2026-03-02)
- **InteractiveBook**：章节使用 H5P.Column 1.18 包装器（正确的 H5P 结构）
- **InteractiveBook**：35+ 种嵌入类型（之前为 5 种），baseColor，progressAuto
- **CoursePresentation**：模板系统（title_only, text_content, interactive, split）
- **CoursePresentation**：嵌入式 H5P 类型（MultiChoice, TrueFalse, DragText 等）
- **CoursePresentation**：基于 UUID 的 subContentIds
- **BS:WI 设计**：在 H5P 包中注入 CSS（海军蓝按钮、浅蓝进度条、黄色成功提示）
- **BS:WI 设计**：InteractiveBook 中经过样式设计的章节标题
- **可视化验证**：基于 Puppeteer 的截图 + 自动检查
- **generate_and_verify()**：一步完成生成 + 验证

### v2.3 (2026-01-26)
- 文本转测验，带有干扰项生成器

### v2.2 (2026-01-24)
- Drag the Words, Timeline, Memory Game（总计 12 种内容类型）

---

*版本 3.1 - Essay, SortParagraphs, BranchingScenario, InteractiveVideo*
