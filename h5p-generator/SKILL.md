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
| Interactive Video | `create_interactive_video()` | 交互视频（v3.1） |

## 容器类型 (4) - v3.0 新增
| 容器 | 函数 | 使用场景 |
| --- | --- | --- |
| Column | `create_column()` | 2-5 个元素垂直排列 |
| QuestionSet | `create_question_set()` | 带有评估的测验序列 |
| CoursePresentation | `create_course_presentation()` | 基于幻灯片的演示，可嵌入 H5P 类型 |
| InteractiveBook | `create_interactive_book()` | 基于章节的图书（章节 = H5P.Column 包装器） |

### 容器推荐
| 场景 | 容器 |
| --- | --- |
| 2-3 种测验类型 | QuestionSet |
| 3-5 种混合类型 | Column |
| 4 种以上带结构的混合类型 | InteractiveBook |
| 演示格式 | CoursePresentation |

## Interactive Book (v3.0)
每个章节都是一个 `H5P.Column 1.18` 包装器 - 所有 35+ 种兼容 Column 的类型均可使用：
```python
from h5p_containers import create_interactive_book

result = create_interactive_book(
    "Scrum-Buch",
    chapters=[
        {
            "title": "Kapitel 1: Rollen",
            "elements": [
                {"library": "H5P.AdvancedText 1.1", "params": {"text": "<h2>Rollen</h2>"}},
                {"library": "H5P.Dialogcards 1.9", "params": {"dialogs": [...]}},
                {"library": "H5P.MultiChoice 1.16", "params": {"question": "...", "answers": [...]}}
            ]
        }
    ],
    cover_description="Ein Buch ueber Scrum",
    base_color="#003366"  # BS:WI Navy
)
