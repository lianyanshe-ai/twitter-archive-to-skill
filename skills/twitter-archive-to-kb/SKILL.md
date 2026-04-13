---
name: twitter-archive-to-kb
description: 将Twitter官方导出的存档数据处理成Obsidian/Logseq友好的Markdown个人知识库，筛选排除回复和转发，只保留原创内容
type: tool
trigger: 处理Twitter存档、导出Twitter推文、整理Twitter知识库、twitter archive to markdown kb
version: 1.0
last_updated: 2026-04-13
---

# Twitter Archive to Markdown Knowledge Base

工具类Skill：将Twitter官方导出的存档数据，整理成按年月分类、每个推文一条文件、带完整Frontmatter元数据的Markdown知识库，可直接导入Obsidian/Logseq等个人笔记软件。

## 功能概述

输入：Twitter官方导出的压缩包解压后的 `data/` 目录，包含：
- `tweets.js` - 所有普通推文
- `note-tweet.js` - Twitter Notes 长文本笔记（超过280字）
- `article.js` - Twitter Articles 长文功能文章

输出：`twitter-notes-kb/` 目录，包含：
- 按 `YYYY/MM/` 分层目录结构
- 每个推文/笔记/article 一个独立 `.md` 文件
- 完整Frontmatter元数据（标题、日期、tweet_id、url、来源类型、标签）
- 自动提取内容中的 `#hashtag` 作为标签

**默认筛选规则**：排除 tweets.js 中所有**@开头的回复**和**RT开头的转发**，只保留原创推文。Notes 和 Articles 全部保留。

## 使用流程

### Step 1: 准备数据
1. 从Twitter请求账号数据导出：Settings → Your account → Download an archive of your data
2. 等待Twitter邮件通知，下载压缩包并解压
3. 找到解压后的 `data/` 目录，确认包含 `tweets.js`、`note-tweet.js`、`article.js`

### Step 2: 运行提取
调用这个Skill后，会自动生成Python提取脚本，执行后输出知识库。

**提取脚本会自动处理**：
1. 解析Twitter JavaScript格式的数据文件（`window.YTD.*` 格式）
2. 筛选排除回复和转发
3. 合并三种数据源（tweets + notes + articles）
4. 按年月创建目录
5. 为每个文件生成Frontmatter
6. 自动提取hashtags

### Step 3: 导入知识库
提取完成后，将整个 `twitter-notes-kb/` 目录复制到你的Obsidian/Logseq vault即可使用。

## 数据格式说明

### 输出文件示例

```markdown
---
title: "人生几个重要公式"
date: 2023-08-12
tweet_id: 1690385515848376320
url: https://twitter.com/i/web/status/1690385515848376320
source: note
tags: [`投资`, `思考`]
---

人生几个重要公式
自由=能力-欲望
不管是财富自由还是人的精神自由，都满足这个公式，只要能力大于欲望，人就是自由的。
...
```

### Frontmatter字段说明

| 字段 | 说明 |
|------|------|
| `title` | 文章标题（取自第一行内容） |
| `date` | 创建日期（ISO格式） |
| `tweet_id` | 原始推文ID |
| `url` | 原始推文链接 |
| `source` | 数据来源：`tweet`/`note`/`article` |
| `tags` | 从内容中提取的hashtag列表 |

## 核心处理规则

### 筛选规则（tweets.js）
- ✅ 保留：不以 `@` 开头，不以 `RT ` 开头的原创推文
- ❌ 排除：以 `@` 开头的回复、以 `RT ` 开头的转发

### 文件名生成规则
`YYYY-MM-DD-[title-slug]-[tweet_id].md`
- title slug：从标题生成，只保留字母数字，空格换短横
- 加上 tweet_id 避免重名

### 目录结构
```
twitter-notes-kb/
├── 2022/
│   ├── 03/
│   │   ├── 2022-03-01-title-slug-123456.md
│   │   └── ...
│   └── ...
├── 2023/
└── ...
```

## 处理不同数据源

### 1. tweets.js（普通推文）
- 使用 `full_text` 字段作为内容
- 解析 `created_at` 日期格式
- 应用筛选规则

### 2. note-tweet.js（Twitter Notes长文）
- 使用 `core.text` 字段作为完整内容
- 解析 `createdAt` ISO日期
- 全部保留，不筛选
- 每条单独一个文件

### 3. article.js（Twitter Articles长文）
- 从 `content.blocks` 拼接完整内容
- 保留封面图片链接放在文末
- 解析 `createdAt` 时间戳
- 全部保留，不筛选
- 每条单独一个文件

## 最佳实践

1. **先完整提取，后按需筛选**：先提取所有原创，再在Obsidian中用搜索筛选
2. **利用标签**：Twitter上的hashtag会自动提取为Obsidian标签，方便聚合
3. **链接笔记**：可以在Obsidian中为相关话题添加双向链接，构建知识网络
4. **检查完整性**：提取后检查总条数确认完整

## 已知局限

- Twitter官方导出时，长文已经切割为notes/articles，本工具合并后完整保留
- 推文中带链接时，原始数据中链接已经被Twitter缩短，无法还原原始链接（Twitter存档本身限制）
- 媒体文件（图片/视频）需要单独处理，本工具只保留链接

## 核心步骤代码骨架

```python
1. 解析window.YTD格式JS文件 → JSON数组
2. 对tweets：过滤掉回复和转发
3. 对每个条目：提取内容、解析日期、提取标签
4. 按年月创建目录
5. 生成带Frontmatter的markdown文件
6. 写入对应路径
```

## 触发词

- "处理Twitter存档"
- "导出Twitter推文到Markdown"
- "整理Twitter知识库"
- "twitter archive to kb"
- "将推特数据整理成Obsidian库"

## 调研来源

- 基于实际处理Twitter存档数据的一手经验
- Twitter官方导出数据格式分析
- Obsidian知识库最佳实践

## 诚实边界

- 这是一个数据处理工具Skill，不提供思维框架或决策建议
- 只能处理Twitter官方导出格式的数据，其他格式需要适配
- 依赖原始导出数据的完整性，无法恢复Twitter存档中不存在的内容

调研完成：2026-04-13
