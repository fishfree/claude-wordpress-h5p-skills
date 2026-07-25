# 经验总结：H5P Interactive Book 兼容性

**日期：** 2025-01-25  
**背景：** H5P Generator 多智能体系统  
**测试环境：** Lumi Desktop

## 兼容性矩阵

### 可在 Interactive Book 中正常运行 ✅

| H5P 类型 | Library | 说明 |
|---------|---------|-----------|
| **AdvancedText** | H5P.AdvancedText 1.1 | 文本、标题 |
| **Dialogcards** | H5P.Dialogcards 1.9 | 闪卡/学习卡片 |
| **TrueFalse** | H5P.TrueFalse 1.8 | 判断题 |
| **MultiChoice** | H5P.MultiChoice 1.16 | 选择题 |
| **DragText** | H5P.DragText 1.10 | 将单词拖入填空 |

### 无法正常运行 ❌

| H5P 类型 | Library | 问题 |
|---------|---------|---------|
| **Blanks** | H5P.Blanks 1.14 | 预览无法加载 |
| **DragQuestion** | H5P.DragQuestion 1.14 | 预览无法加载 |

## 建议

### 不兼容类型的替代方案

| 替代对象 | 建议使用 | 原因 |
|-------|-------|-------|
| Blanks（输入式填空） | **DragText** | 功能相同，但采用拖拽而非输入 |
| DragQuestion（图片拖拽） | **MultiChoice** | 功能较简单，但能够正常运行 |

### Interactive Book 的推荐结构

```python
# 最小可运行结构
content = {
    "showCoverPage": False,  # 或 True，并配合 bookCover
    "bookCover": {"coverDescription": "", "coverImage": {}, "coverMedium": {}},
    "title": "<p>标题</p>",
    "chapters": [
        {
            "title": "第 1 章",
            "params": {
                "content": [
                    {
                        "content": {
                            "library": "H5P.AdvancedText 1.1",
                            "params": {"text": "<p>内容</p>"},
                            "subContentId": "unique-id",
                            "metadata": {"contentType": "Text", "license": "U", "title": "标题"}
                        },
                        "useSeparator": "auto"
                    }
                ]
            }
        }
    ],
    "behaviour": {"defaultTableOfContents": True, "progressIndicators": True, "displaySummary": True},
    "l10n": { ... }  # 本地化
}

h5p = {
    "title": "标题",
    "language": "de",
    "mainLibrary": "H5P.InteractiveBook",
    "embedTypes": ["iframe"],
    "license": "U",
    "preloadedDependencies": [
        {"machineName": "H5P.InteractiveBook", "majorVersion": 1, "minorVersion": 7},
        {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 16},
        # + 所有使用到的内容类型
    ]
}
```

## 调试技巧

1. **预览无法加载？** → 很可能是使用了不兼容的 Library。
2. **逐步测试：** 先仅添加文本，再逐个加入其他元素。
3. **多个章节：** 可以正常工作，没有兼容性问题。
4. **Dependencies：** 所有使用到的 Library 都必须加入 `preloadedDependencies`。

## 解包 QuestionSet Wrapper

**问题：** H5P Generator 会将 MultiChoice / TrueFalse 生成为带有 `questions[]` 数组的 QuestionSet。  
如果直接嵌入，则答案会丢失。

**解决方案：** 对于测验类型，提取 `questions[0].params`：

```python
def _unwrap_questionset_content(self, content: dict) -> dict:
    if 'questions' in content and isinstance(content['questions'], list):
        questions = content['questions']
        if len(questions) > 0 and 'params' in questions[0]:
            return questions[0]['params']
    return content
```

## 已验证可正常工作的组合

- Flashcards + TrueFalse（2 个章节）
- Flashcards + MultiChoice（2 个章节）
- Flashcards + DragText（2 个章节）
- 文本 + Flashcards + TrueFalse + MultiChoice（4 个章节）
