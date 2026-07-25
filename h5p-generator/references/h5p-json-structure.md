# H5P Content Types - JSON Structure Reference

## Overview

H5P files are ZIP archives with:
- `h5p.json` - Metadata and library dependencies
- `content/content.json` - The actual content

## True/False (H5P.TrueFalse)

```json
{
  "question": "<p>Statement text</p>",
  "correct": "true",  // or "false" (string!)
  "l10n": {
    "trueText": "正确",
    "falseText": "错误"
  },
  "feedbackOnCorrect": "正确！",
  "feedbackOnWrong": "很遗憾，回答错误。"
}
```

## Fill in the Blanks (H5P.Blanks)

Blanks marked with asterisks: `*answer*`

Multiple accepted answers: `*answer1/answer2*`

```json
{
  "text": "<p>德国首都是 *柏林*。</p>",
  "behaviour": {
    "caseSensitive": false,
    "acceptSpellingErrors": true
  }
}
```

## Multiple Choice (H5P.MultiChoice)

```json
{
  "question": "<p>Question text?</p>",
  "answers": [
    {"text": "<div>Option A</div>", "correct": true},
    {"text": "<div>Option B</div>", "correct": false}
  ],
  "behaviour": {
    "randomAnswers": true,
    "singlePoint": false
  }
}
```

## Drag and Drop (H5P.DragQuestion)

**注意：** 请参见文末的“关键：H5P.DragQuestion 定位”章节！

```json
{
  "question": {
    "settings": {
      "size": {"width": 620, "height": 450},
      "background": {"path": "https://...", "mime": "image/jpeg"}
    },
    "task": {
      "elements": [
        {
          "x": 5, "y": 3,
          "width": 12, "height": 6,
          "dropZones": ["0"],
          "backgroundOpacity": 80,
          "type": {
            "library": "H5P.AdvancedText 1.1",
            "params": {"text": "<p>Draggable text</p>"}
          }
        }
      ],
      "dropZones": [
        {
          "x": 3, "y": 22,
          "width": 10, "height": 73,
          "label": "<div>Zone Name</div>",
          "correctElements": ["0"],
          "showLabel": true,
          "backgroundOpacity": 70,
          "autoAlign": true
        }
      ]
    }
  }
}
```

## Question Set (H5P.QuestionSet)

Wrapper for multiple questions:

```json
{
  "introPage": {
    "showIntroPage": true,
    "title": "Quiz Title",
    "introduction": "<p>Instructions</p>"
  },
  "progressType": "dots",
  "passPercentage": 60,
  "questions": [
    {
      "params": { /* question content */ },
      "library": "H5P.TrueFalse 1.8",
      "subContentId": "unique-id"
    }
  ],
  "endGame": {
    "showResultPage": true,
    "message": "Score: @score / @total"
  }
}
```

## h5p.json Structure

```json
{
  "title": "Content Title",
  "language": "de",
  "mainLibrary": "H5P.QuestionSet",
  "embedTypes": ["iframe"],
  "license": "CC BY",
  "preloadedDependencies": [
    {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20}
  ]
}
```

## Library Versions (as of 2026)

| Library | Version | Use Case |
|---------|---------|----------|
| H5P.QuestionSet | 1.20 | 题集容器 |
| H5P.TrueFalse | 1.8 | 判断题 |
| H5P.MultiChoice | 1.16 | 多选题 |
| H5P.Blanks | 1.14 | 填空题 |
| H5P.DragQuestion | 1.14 | 拖拽题 |
| H5P.SingleChoiceSet | 1.11 | 单选题 |
| H5P.Dialogcards | 1.9 | 闪卡 |
| H5P.MarkTheWords | 1.11 | 标记单词 |
| H5P.Summary | 1.10 | 总结/摘要 |
| H5P.Accordion | 1.0 | 可折叠章节（手风琴式） |
| H5P.AdvancedText | 1.1 | 文本组件 |

## New Content Types

### Single Choice Set (H5P.SingleChoiceSet)

```json
{
  "choices": [
    {
      "question": "<p>Question?</p>",
      "answers": ["<p>Correct</p>", "<p>Wrong1</p>", "<p>Wrong2</p>"]
    }
  ],
  "behaviour": {
    "autoContinue": true,
    "timeoutCorrect": 2000,
    "enableRetry": true
  }
}
```

### Dialog Cards / Flashcards (H5P.Dialogcards)

```json
{
  "title": "<p>Title</p>",
  "dialogs": [
    {
      "text": "<p>Front side</p>",
      "answer": "<p>Back side</p>",
      "tips": [{"text": "Optional hint"}]
    }
  ],
  "behaviour": {
    "enableRetry": true,
    "randomCards": false
  }
}
```

### Mark the Words (H5P.MarkTheWords)

```json
{
  "taskDescription": "<p>Mark the correct words.</p>",
  "textField": "This is *correct* but this is wrong.",
  "behaviour": {
    "enableRetry": true,
    "enableSolutionsButton": true
  }
}
```

### Summary (H5P.Summary)

```json
{
  "intro": "<p>Choose the correct statement.</p>",
  "summaries": [
    {
      "summary": [
        {"text": "<p>Correct statement</p>"},
        {"text": "<p>Wrong statement</p>"}
      ]
    }
  ]
}
```

### Accordion (H5P.Accordion)

```json
{
  "panels": [
    {
      "title": "Section Title",
      "content": {
        "params": {"text": "<p>Content here</p>"},
        "library": "H5P.AdvancedText 1.1"
      }
    }
  ],
  "hTag": "h2"
}
```

## Notes

- All text content should be wrapped in HTML tags (`<p>`, `<div>`)
- Boolean values in some fields are strings ("true"/"false")
- subContentId must be unique within a QuestionSet

---

## 关键：H5P.DragQuestion 定位与尺寸

**重要：** DragQuestion 中的 width/height 值**不是百分比**！

### 单位换算（经验测得）

| JSON-Feld | 换算关系 | 示例 |
|-----------|------------|----------|
| `x`, `y` | 每单位约 7px | x: 37 → 259px |
| `width`, `height` | 每单位约 18px（EM） | width: 10 → 180px |

### 计算无重叠的 Dropzone

**问题：** `width: 20` 会变成约 360px → 三个区域会发生严重重叠！

**解决方案：** 使用更小的 width 值，并计算各区域的位置：

```
700px 容器中 3 个互不重叠 Dropzone 示例：

Zone 1: x=3,  width=10  → left=21px,  right=201px（宽180px）
Zone 2: x=37, width=10  → left=259px, right=439px（宽180px）
Zone 3: x=71, width=10  → left=497px, right=677px（宽180px）

间距：各区域之间约 57px ✓
```

### 位置计算公式

```
position_px = x_value * 7
width_px = width_value * 18

计算 Zone A 与 Zone B 之间的间距：
gap_px = (x_B * 7) - (x_A * 7 + width_A * 18)
```

### 可正常工作的配置（已测试）

```json
"dropZones": [
  {"x": 3,  "y": 22, "width": 10, "height": 73, "correctElements": ["0","1","2"]},
  {"x": 37, "y": 22, "width": 10, "height": 73, "correctElements": ["3","4","5"]},
  {"x": 71, "y": 22, "width": 10, "height": 73, "correctElements": ["6","7","8"]}
]
```

### Draggable Elements（推荐尺寸）

**推荐参数：**
- `width: 6-8`，根据文本长度调整（短文本：6，长文本：8）
- `height: 2`，适用于单行文本
- HTML 中使用 `font-size: 12px`

**配置示例：**
```json
{
  "x": 2, "y": 2,
  "width": 7, "height": 2,
  "backgroundOpacity": 80,
  "type": {
    "library": "H5P.AdvancedText 1.1",
    "params": {
      "text": "<p style='text-align:center;margin:0;font-size:12px;font-weight:bold;'>短文本</p>"
    }
  }
}
```

**文本长度 → 宽度：**
| 字符数 | 宽度 |
|---------|-------|
| 10-15 | 6 |
| 16-19 | 7 |
| 20+ | 8 |

- 可以相互重叠（拖拽过程中会自动分开）
- 文本允许自动换行，这是正常的

### 画布尺寸

```json
"settings": {
  "size": {"width": 620, "height": 450}  // 默认值
}
```

### 背景图片

```json
"background": {
  "path": "https://images.unsplash.com/...",
  "mime": "image/jpeg"
}
```

### 不透明度（Opacity）

- `backgroundOpacity: 70` 用于元素（范围 0-100）
- Draggable 与 Dropzone 分别独立设置
