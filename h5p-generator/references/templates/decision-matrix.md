# H5P Content-Type 决策矩阵

## Agent 决策逻辑

```python
def select_h5p_type(lernziel: str, operator: str, komplexität: str) -> str:
    """
    根据教学设计原则选择合适的 H5P 类型。

    Args:
        lernziel: 学习目标是什么？
        operator: 采用哪种认知操作？（如：列举、解释、分析、评价……）
        komplexität: 简单 | 中等 | 高

    Returns:
        H5P Content-Type 名称
    """

    # Level 1：知识再现（列举、描述）
    if operator in ["nennen", "beschreiben", "auflisten"]:
        if komplexität == "einfach":
            return "Flashcards"  # 学习术语
        else:
            return "Fill-in-Blanks"  # 填空题

    # Level 2：知识重组（解释、分类、配对）
    if operator in ["erklären", "zuordnen", "ordnen", "klassifizieren"]:
        return "Drag-and-Drop"  # 配对与分类练习

    # Level 3：迁移应用（应用、计算）
    if operator in ["anwenden", "berechnen", "durchführen"]:
        return "Course-Presentation"  # 分步骤学习

    # Level 4：分析（分析、比较、研究）
    if operator in ["analysieren", "vergleichen", "untersuchen"]:
        return "Interactive-Video"  # 理解过程

    # Level 5：评价（评价、论证、判断）
    if operator in ["bewerten", "begründen", "beurteilen", "entscheiden"]:
        return "Branching-Scenario"  # 决策模拟

    # Level 6：创造（设计、规划、开发）
    if operator in ["entwickeln", "konzipieren", "planen", "gestalten"]:
        return "Interactive-Book"  # 综合学习单元

    # 默认：知识测验
    return "Question-Set"
```

## 快速参考表

| 学习目标 | 认知操作 | H5P 类型 | 示例 |
|----------|----------|---------|----------|
| 学习术语 | 列举 | Flashcards | 专业术语、词汇 |
| 检查事实 | 描述 | True-False | 判断题（对/错） |
| 理解定义 | 补全 | Fill-in-Blanks | 专业术语填空 |
| 分类整理 | 配对 | Drag-and-Drop | 元素分组、分类 |
| 理解关系 | 解释 | Accordion | 可折叠说明 |
| 掌握步骤 | 应用 | Course-Presentation | 计算过程、操作流程 |
| 分析过程 | 分析 | Interactive-Video | 带暂停点的案例分析 |
| 评价方案 | 评价 | Branching-Scenario | 决策树模拟 |
| 系统学习 | 组织 | Interactive-Book | 完整学习单元 |

## Content-Type 详细说明

### 简单类型（支持生成器自动生成）

| 类型 | 文件名 | 适用场景 | 不适用场景 |
|-----|-----------|----------------|----------------------|
| **True-False** | `create_true_false()` | 检查事实知识 | 复杂概念或推理 |
| **Multiple-Choice** | `create_multi_choice()` | 多个选项，一项或多项正确 | 开放式问题 |
| **Single-Choice** | `create_single_choice()` | 快速测验，仅一个正确答案 | 需要说明理由时 |
| **Fill-in-Blanks** | `create_fill_blanks()` | 填写准确术语 | 创造性回答 |
| **Drag-and-Drop** | `create_drag_drop()` | 分类、配对 | 超过 5 个分类 |
| **Flashcards** | `create_flashcards()` | 词汇、定义 | 复杂概念 |
| **Mark-the-Words** | `create_mark_words()` | 在文本中标记关键词 | 长篇文本 |
| **Summary** | `create_summary()` | 找出核心观点 | 初次介绍知识 |
| **Accordion** | `create_accordion()` | 展示结构化信息 | 互动练习 |

### 复杂类型（需在 H5P 编辑器中手工制作）

| 类型 | 适用场景 | 工作量 |
|-----|----------------|---------|
| **Interactive-Video** | 流程分析、案例教学 | 高（需要视频） |
| **Branching-Scenario** | 决策训练、IHK 模拟考试 | 很高 |
| **Course-Presentation** | 解题步骤、分步教学 | 中 |
| **Interactive-Book** | 完整课程或学习单元 | 很高 |

## 教学设计原则

1. **适度使用游戏化**
   - Flashcards、Drag & Drop、Fill-in-Blanks：作为辅助学习工具
   - **不要**在 IHK / 德国高中毕业考试（Abitur）级别课程中作为主要学习方式

2. **测验必须配有解释**
   - Feedback 应解释思维错误，而不仅仅是告诉学生“对”或“错”
   - 建议为 `feedback_correct` 与 `feedback_wrong` 提供详细解释

3. **遵循学习进阶**
   - 导入：Accordion（知识介绍）→ Flashcards（术语学习）
   - 练习：Fill-in-Blanks → Drag-and-Drop
   - 测评：Multiple-Choice（附解释）→ Summary

4. **融入 4K 核心能力**
   - **创造力（Creativity）**：开放式任务（不限于 H5P）
   - **批判性思维（Critical Thinking）**：评价类问题、Branching Scenario
   - **沟通能力（Communication）**：设计讨论活动
   - **协作能力（Collaboration）**：在 H5P 外组织小组合作任务

## 示例工作流

```text
主题："敏捷开发方法"

1. Accordion："什么是敏捷开发？"（知识导入）
2. Flashcards：学习术语（Scrum、Sprint、Backlog）
3. Drag-and-Drop：Scrum 角色配对
4. True-False：辨别神话与事实
5. Summary：识别核心原则
6. 【手工制作】Branching-Scenario：模拟 Sprint 规划
```
