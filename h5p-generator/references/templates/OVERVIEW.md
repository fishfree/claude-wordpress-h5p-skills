# H5P 模板库 - 概览

## 可用模板（24 种类型）

### 支持生成器自动生成（9 种类型）

这些类型可以使用 Python 生成器创建：

| 类型 | Library | 生成器函数 | 文件 |
|-----|---------|-------------------|-------|
| True/False | H5P.TrueFalse 1.8 | `create_true_false()` | `truefalse` |
| Multiple Choice | H5P.MultiChoice 1.16 | `create_multi_choice()` | - |
| Fill in Blanks | H5P.Blanks 1.14 | `create_fill_blanks()` | `blanks` |
| Drag and Drop | H5P.DragQuestion 1.14 | `create_drag_drop()` | `dragquestion` |
| Single Choice | H5P.SingleChoiceSet 1.11 | `create_single_choice()` | `singlechoiceset` |
| Flashcards/Dialog Cards | H5P.Dialogcards 1.9 | `create_flashcards()` | `dialogcards` |
| Mark the Words | H5P.MarkTheWords 1.11 | `create_mark_words()` | `markthewords` |
| Summary | H5P.Summary 1.10 | `create_summary()` | `summary` |
| Accordion | H5P.Accordion 1.0 | `create_accordion()` | `accordion` |

### 需在 H5P 编辑器中手动创建（15 种类型）

这些类型过于复杂，不适合自动生成。

#### 高优先级（教学价值较高）

| 类型 | Library | 用途 | 复杂度 |
|-----|---------|------------|-------------|
| **Question Set** | H5P.QuestionSet | 包含多道题目的测验 | 中 |
| **Column** | H5P.Column | 在一个页面中组合多个 H5P 内容 | 中 |
| **Timeline** | H5P.Timeline | 带事件的时间轴 | 高 |
| **Drag the Words** | H5P.DragText | 将单词拖入文本中 | 中 |

#### 基于媒体的内容

| 类型 | Library | 用途 | 复杂度 |
|-----|---------|------------|-------------|
| **Audio** | H5P.Audio | 音频播放器 | 低 |
| **Image Slider** | H5P.ImageSlider | 图片画廊 | 低 |
| **Image Juxtaposition** | H5P.ImageJuxtaposition | 图片前后对比 | 低 |
| **Memory Game** | H5P.MemoryGame | 配对记忆游戏 | 中 |

#### 专用类型

| 类型 | Library | 用途 | 复杂度 |
|-----|---------|------------|-------------|
| **Dictation** | H5P.Dictation | 带音频的听写练习 | 高 |
| **Essay** | H5P.Essay | 基于关键词评分的开放式文本 | 中 |
| **Speak the Words** | H5P.SpeakTheWords | 语音输入 | 高 |
| **Personality Quiz** | H5P.PersonalityQuiz | 性格测试 | 高 |
| **Guess the Answer** | H5P.GuessTheAnswer | 带隐藏答案的图片猜题 | 低 |
| **Arithmetic Quiz** | H5P.ArithmeticQuiz | 数学练习 | 中 |
| **Chart** | H5P.Chart | 图表 | 中 |
| **Flashcards (alt)** | H5P.Flashcards | 旧版学习卡片 | 低 |

## 文件结构

```text
references/templates/
├── OVERVIEW.md              # 本文件
├── decision-matrix.md       # 何时使用哪种类型
├── dragdrop-working.json    # 已验证的 Drag & Drop 参数
├── all-types.json           # 手工模板集合
└── all-examples.json        # 从 33 个示例中提取
```

## 示例来源

| 来源 | 数量 | 描述 |
|--------|--------|--------------|
| h5p.org | 20 | 官方参考示例 |
| UBC | 13 | 不列颠哥伦比亚大学（学术示例） |

## 使用方法

### 使用生成器

```python
from h5p_generator import create_drag_drop, THEMES

result = create_drag_drop(
    "Mein Quiz",
    "Ordne zu!",
    ["Kategorie A", "Kategorie B"],
    [{"text": "Item 1", "dropzone": 0}, {"text": "Item 2", "dropzone": 1}],
    style=THEMES['education']
)
```

### 将模板作为参考

```python
import json

# 加载模板结构
with open('references/templates/all-examples.json') as f:
    templates = json.load(f)

# 显示 Timeline 的结构
print(json.dumps(templates['timeline']['structure'], indent=2))
```

## 后续计划

1. 添加 **Interactive Video** 模板（需要支持视频上传）
2. 添加 **Branching Scenario** 模板（复杂决策树）
3. 添加 **Course Presentation** 模板（带交互的幻灯片）
4. 添加 **Interactive Book** 模板（多页学习单元）

这 4 种类型是最复杂、也是最适合 IHK（德国工商会考试）/ 德国高中毕业考试（Abitur）教学场景的 H5P 内容类型。
