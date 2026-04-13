# twitter-archive-to-skill

> 从你的 Twitter 存档一键生成个人写作/思维风格 Skill，用于 Claude Code / OpenClaw / CodeX

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 简介

这是一个端到端的工具流水线，可以：

1. **第一步**：把你从 Twitter 官方导出的存档，提取整理成 Obsidian/Logseq 友好的 Markdown 知识库
   - 自动排除回复和转发，只保留原创内容
   - 按 `YYYY/MM/` 分类存储，每个内容一个文件
   - 带完整 Frontmatter 元数据，自动提取 hashtags 标签

2. **第二步**：基于你的所有原创推文，自动蒸馏出你的个人思维/写作风格 Skill
   - 提炼你的核心心智模型
   - 总结你的决策启发式
   - 分析你的表达 DNA
   - 生成可直接调用的 Skill，随时可以用**你的视角**来分析问题

## 🚀 快速开始

### 前置要求

- Claude Code / OpenClaw / CodeX 已安装
- Python 3.6+ 环境

> `huashu-nuwa` (女娲造人) 已经包含在这个包里，安装脚本会一起安装，不需要提前准备。

### 安装

```bash
# 克隆仓库
git clone https://github.com/lianyanshe-ai/twitter-archive-to-skill.git
cd twitter-archive-to-skill

# 安装到 ~/.claude/skills/
./install.sh
```

手动安装：把 `skills/` 目录下的两个文件夹复制到 `~/.claude/skills/` 即可。

### 使用流程

#### 1. 导出你的 Twitter 数据

1. 打开 Twitter → Settings → Your account → Download an archive of your data
2. 等待 Twitter 发邮件给你（可能需要几小时到几天）
3. 下载压缩包并解压到你的工作目录，确认有 `data/` 文件夹

#### 2. 调用 Skill 处理

在 Claude Code 中：
```
/skill twitter-archive-to-skill
```

按照提示操作即可，整个流程自动完成：
- 提取数据生成 Markdown 知识库 → `./twitter-notes-kb/`
- 蒸馏你的个人 Skill → `~/.claude/skills/yourname-perspective/`

#### 3. 使用生成的 Skill

处理完成后，就可以直接调用你的个人Skill：
```
/skill yourname-perspective
帮我用我的视角分析一下这个问题...
```

## 📦 包含两个 Skill

| Skill | 功能 |
|-------|------|
| `twitter-archive-to-kb` | 仅做数据提取：Twitter存档 → Markdown知识库 |
| `twitter-archive-to-skill` | 端到端：Twitter存档 → Markdown知识库 → 个人Skill |

## 🗂️ 输出格式

### Markdown 知识库结构

```
twitter-notes-kb/
├── 2022/
│   ├── 03/
│   │   ├── 2022-03-01-title-slug-123456.md
│   │   └── ...
│   └── ...
└── ...
```

每个文件包含完整 Frontmatter：

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
...
```

### 生成的个人 Skill

输出到 `~/.claude/skills/yourname-perspective/`，包含：
- `SKILL.md` - 提炼好的心智模型、决策启发式、表达DNA
- `references/` - 调研资料

可以直接通过 `/skill yourname-perspective` 调用。

## ✨ 特性

- ✅ 支持三种数据源：`tweets.js` + `note-tweet.js` + `article.js`
- ✅ 自动筛选：排除@回复和RT转发，只保留原创
- ✅ Obsidian 原生支持：Frontmatter + 标签自动提取
- ✅ 端到端自动化：从存档到Skill一键完成
- ✅ 兼容 Claude Code / OpenClaw / CodeX

## 📋 筛选规则

| 内容类型 | 处理方式 |
|---------|----------|
| 原创推文 | ✅ 保留 |
| @开头回复 | ❌ 排除 |
| RT开头转发 | ❌ 排除 |
| Twitter Notes 长文 | ✅ 全部保留 |
| Twitter Articles | ✅ 全部保留 |

## 🎯 适用场景

- 把你多年的 Twitter 内容整理成个人知识库
- 让 AI 学会你的写作风格和思维方式
- 生成个人助理，用你的视角分析问题
- 备份你的 Twitter 内容

## 📝 依赖

所有依赖已经打包在本仓库中，安装脚本会一键安装完成，不需要额外准备。

## ⚠️ 限制

- 只能处理 Twitter 官方导出格式
- 蒸馏质量取决于你推文数量和内容质量
- 媒体文件（图片/视频）只保留链接，需要单独处理

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 👤 Credits

Built with [huashu-nuwa](https://github.com/...) 女娲造人Skill framework.
