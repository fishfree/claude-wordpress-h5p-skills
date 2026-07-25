# H5P Agent Workflow

## 概述

H5P Agent 是一个用于自动生成 H5P 内容的自我改进工作流，具有以下特性：

- **自动选择内容类型**，基于学习目标/认知操作词
- **质量验证**，针对已知问题进行检查
- **预览系统**，用于快速测试
- **模板库**，能够从反馈中持续学习

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                     H5P Education Agent                      │
├─────────────────────────────────────────────────────────────┤
│  1. ANALYSE                                                  │
│     - 分析学习目标                                           │
│     - 识别认知操作词（列举、匹配、解释……）                  │
│     - 根据置信度选择内容类型                                │
├─────────────────────────────────────────────────────────────┤
│  2. GENERIERUNG                                              │
│     - 从模板库加载模板                                      │
│     - 填充内容                                               │
│     - 创建 H5P 文件                                          │
├─────────────────────────────────────────────────────────────┤
│  3. VALIDIERUNG                                              │
│     - 检查已知问题                                           │
│     - 输出警告                                               │
│     - 必要时自动修正                                         │
├─────────────────────────────────────────────────────────────┤
│  4. PREVIEW & FEEDBACK                                       │
│     - 启动本地预览服务器                                     │
│     - 收集用户反馈（1-5 星）                                 │
│     - 将优秀结果保存为模板                                   │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from agent_workflow import H5PAgent

agent = H5PAgent()

# 1. 自动选择内容类型
decision = agent.decide_content_type("Ordne die Scrum-Rollen zu")
print(f"Empfehlung: {decision.content_type}")  # → drag_drop

# 2. 生成并进行验证
result, issues = agent.generate_with_validation(
    'drag_drop',
    title="Scrum-Rollen",
    dropzones=["Product Owner", "Scrum Master", "Dev Team"],
    draggables=[
        {"text": "Priorisiert Backlog", "dropzone": 0},
        {"text": "Entfernt Hindernisse", "dropzone": 1},
        {"text": "Entwickelt Features", "dropzone": 2},
    ]
)

# 3. 启动预览
if result.success:
    agent.preview(result.path)

# 4. 保存反馈（成功时）
agent.save_as_template(result, "scrum-rollen-zuordnung", "适用于入门教学")
```

## 决策逻辑

Agent 会识别学习目标中的认知操作词，并自动选择：

| 操作词 | 内容类型 | 示例学习目标 |
|----------|--------------|-------------------|
| 列举 | Flashcards | "列举 Scrum 角色" |
| 描述 | True-False、Summary | "描述敏捷价值观" |
| 解释 | Accordion | "解释 Sprint 流程" |
| 匹配 | Drag-Drop | "将任务匹配到角色" |
| 排序 | Timeline | "按时间顺序排列" |
| 补全 | Fill-in-Blanks、Drag-Text | "补全空白" |
| 标记 | Mark-Words | "标记动词" |

## 验证

Agent 会自动检查以下已知问题：

### Drag & Drop

- Dropzone y > 70 → 警告（可能位于画布之外）
- Dropzone height < 20 → 警告（区域过小）
- 超过 5 个 Dropzone → 提示（界面可能过于复杂）

### Timeline

- 少于 2 个事件 → 错误
- 没有日期信息 → 错误

### 通用

- 标题为空 → 错误
- 没有内容 → 错误

## 预览系统

```bash
# 手动启动
cd viewer
python serve.py ../test-output/meine-datei.h5p

# 自动打开：http://localhost:8080/preview.html
```

预览系统使用 h5p-standalone，在无需 WordPress/Moodle 的情况下进行本地渲染。

## 模板库

成功生成的内容可以保存为模板：

```python
# 测试成功后
agent.save_as_template(result, "name", "备注")
# → 保存到 references/templates/saved/name.json
```

### 目录结构

```
references/templates/
├── OVERVIEW.md              # 分类概览
├── decision-matrix.md       # 决策逻辑
├── dragdrop-working.json    # 已验证的 Drag&Drop 参数
├── all-types.json           # 手工参考
├── all-examples.json        # 提取出的 24 个模板
└── saved/                   # Agent 保存的模板
    └── *.json
```

## 反馈日志

所有生成过程都会连同反馈一起记录：

```json
{
  "timestamp": "2026-01-24T...",
  "content_type": "drag_drop",
  "title": "Scrum-Rollen",
  "success": true,
  "rating": 5,
  "issues": [],
  "notes": "运行完美"
}
```

该日志将用于未来的持续改进。

## 与 Claude Code 集成

Agent 可以直接在 Claude Code Skill Prompt 中使用：

```
创建一个关于 Scrum 角色的 H5P 匹配题。
- Product Owner：负责 Backlog 优先级排序、定义 User Story
- Scrum Master：消除障碍、主持回顾会议
- Dev Team：开发功能、估算工作量
```

Claude Code：

1. 识别“匹配” → `drag_drop`
2. 使用正确坐标（v13 模板）生成内容
3. 自动进行验证
4. 成功后保存为模板

## 下一步

1. **基于截图的反馈**：自动生成截图用于质量检查
2. **A/B 测试**：比较不同布局方案
3. **自适应模板**：根据反馈评分自动调整模板优先级
4. **多步骤工作流**：自动生成复杂学习路径

