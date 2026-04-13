---
name: twitter-archive-to-skill
description: 端到端工具：从Twitter官方存档，一键提取整理成Markdown知识库，再蒸馏出你的个人写作/思维风格Skill
type: tool-pipeline
trigger: twitter存档生成skill、从推特蒸馏个人skill、twitter archive to personal skill、一键生成个人写作skill
version: 1.0
last_updated: 2026-04-13
---

# Twitter Archive to Personal Skill

**端到端流水线工具**：从你的Twitter官方存档数据，一键生成你的个人写作风格/思维框架Skill。

整个流程自动完成，不需要手动干预：

```
Twitter官方导出压缩包
    ↓
解压 → data/ 目录
    ↓
Step 1: 提取整理 → 按年月分类的Markdown知识库 (twitter-notes-kb/)
    ↓
Step 2: 分析内容 → 调用 huashu-nuwa 蒸馏个人写作/思维风格Skill
    ↓
输出：你的专属Perspective Skill，可以随时用你的思维方式分析问题
```

## 功能概述

输入：Twitter官方导出的存档 `data/` 目录

输出：
1. `twitter-notes-kb/` - 完整Markdown知识库，可导入Obsidian
2. `~/.claude/skills/[yourname]-perspective/` - 你的个人风格Skill，包含提炼好的心智模型、表达DNA、决策启发式

## 完整流程

### Phase 1: 数据提取阶段（调用 twitter-archive-to-kb）

1. **解析**：`tweets.js` + `note-tweet.js` + `article.js` 三种数据源
2. **筛选**：从 `tweets.js` 排除所有@开头的回复和RT开头的转发，只保留原创内容
3. **结构化**：每条内容一个Markdown文件，按 `YYYY/MM/` 组织，带完整Frontmatter
4. **结果**：得到结构化知识库，可用于笔记软件或进一步分析

### Phase 2: Skill蒸馏阶段（调用 huashu-nuwa 女娲造人）

基于提取出的所有原创推文，自动分析并蒸馏：

1. **心智模型**：提取你反复表达的核心观点和思考框架（3-7个）
2. **决策启发式**：你做判断时用的快速规则（5-10条）
3. **表达DNA**：你的写作风格、句式偏好、用词习惯
4. **价值观**：你的核心价值排序
5. **反模式**：你明确反对的思维方式

最终生成一个完整的 `[yourname]-perspective` Skill，可以随时用你的视角分析问题。

## 使用方法

### 前置准备

1. 从Twitter请求数据导出：`Settings → Your account → Download an archive of your data`
2. 下载解压后，确认项目根目录下有 `data/` 文件夹，包含：
   - `data/tweets.js`
   - `data/note-tweet.js` (可选)
   - `data/article.js` (可选)

### 调用方式

触发这个Skill后，会自动：

```
1. 确认你的Skill名称（通常是你的名字/ID）
2. 运行提取脚本生成知识库
3. 扫描所有提取出的Markdown文件，分析内容特征
4. 调用 huashu-nuwa 蒸馏个人视角Skill
5. 完成后即可使用
```

### 输出结果

| 产物 | 位置 | 用途 |
|------|------|------|
| Markdown知识库 | `./twitter-notes-kb/` | 导入Obsidian/Logseq做个人知识库 |
| 个人Skill | `~/.claude/skills/[name]-perspective/` | 调用 `[name]-perspective` Skill用你的视角分析问题 |

## 处理规则

### 筛选规则
- ✅ **保留**：原创推文、Notes长文、Articles文章
- ❌ **排除**：@开头回复他人、RT开头转发、已删除推文不处理

### 提炼规则
- **跨域验证**：只有在多个不同话题反复出现的观点才会被提炼为心智模型
- **宁少勿多**：保留最独特的3-7个模型，不堆砌通用道理
- **诚实边界**：明确标注信息局限，不编造

## 依赖

本Skill是流水线工具，依赖：
- `twitter-archive-to-kb` - 数据提取整理
- `huashu-nuwa` - Skill蒸馏造人

## 最佳实践

1. **完整导出**：等待Twitter完整导出所有数据再开始，不要中途截断
2. **确认名称**：提前想好你要生成的Skill名称（通常是你的ID或名字）
3. **耐心等待**：几千条推文分析蒸馏需要一点时间
4. **后续更新**：如果有新推文，可以重新运行更新Skill

## 完整示例流程

```bash
# 1. 解压Twitter下载到当前目录
unzip twitter-*.zip -d ./

# 2. 确认data目录存在
ls -la data/

# 3. 调用skill
/skill twitter-archive-to-skill

# 4. 等待完成，得到：
#    - ./twitter-notes-kb/ (知识库)
#    - ~/.claude/skills/yourname-perspective/ (个人Skill)

# 5. 使用生成的Skill
/skill yourname-perspective
"帮我用我的视角分析这个问题：..."
```

## 触发词

- "从Twitter存档生成个人skill"
- "蒸馏我的推特写作风格"
- "twitter archive to personal skill"
- "一键生成个人写作skill"
- "twitter-archive-to-skill"

## 调研来源

- 基于实际处理Twitter存档并蒸馏个人Skill的一手经验
- huashu-nuwa女娲造人方法论
- Obsidian知识库组织最佳实践

## 诚实边界

- 蒸馏质量取决于原始推文数量和质量，推文越多提炼越准确
- 只能提炼公开表达过的思维框架，无法读心
- 无法预测你对全新问题的真实反应，只能基于已有表达推断
- 需要Python环境运行提取脚本

调研完成：2026-04-13
