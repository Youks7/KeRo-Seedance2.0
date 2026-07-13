<h1 align="center">KeRo-Seedance2.0</h1>

<p align="center"><strong>先给可复制成品，再按需展开制作控制</strong></p>

<p align="center">短提示词 · 视觉导演 · 多模态参考 · 分镜生产 · 结果诊断 · 连续性接力</p>

<p align="center">作者：<a href="https://x.com/Isonlyonenice"><strong>秋水 Kero</strong></a></p>

---

## 这是什么

KeRo-Seedance2.0 是一个面向 Seedance 2.0 与即梦 AI 的 Codex Skill。它把用户的创意、参考素材或失败结果转成可直接复制的提示词。

这个 Skill 的设计重点是：

- 简单任务不展开成创作简报、空表格和教程；
- 专业知识必须服务于“如何产出一条好用提示词”；
- 用可重复的前向测试案例判断每次修改有没有让 Skill 退化。

默认先输出成品提示词，只有复杂任务才展示素材职责、分段接力或诊断依据。

## 主要能力

| 任务 | 默认行为 |
|---|---|
| 文生视频 | 输出一条短而完整的成品提示词 |
| 视觉开发 | 建立色彩、光线、构图、光学、材质、运动和情绪系统 |
| 图片、视频、音频参考 | 只使用真实 `@引用`，为素材分配明确职责 |
| 表演与多角色 | 隔离身份、空间和动作层，迁移需要的表演维度 |
| 视频延长与编辑 | 分开“必须继承”和“只允许改变”的内容 |
| 分镜与长项目 | 设计镜头功能、核心测试镜头、转场、接力和后期闭环 |
| 电影视觉语法 | 从经典案例提取可观察摄影原则，不只堆片名 |
| 结果诊断 | 先核对提示词与结果，再做单变量修复 |
| 平台规格 | 查当前官方资料或界面，不沿用过期参数 |

## 安装

Windows PowerShell：

```powershell
git clone https://github.com/Youks7/KeRo-Seedance2.0.git "$env:USERPROFILE\.codex\skills\seedance-video-production"
```

也可以把仓库复制到：

```text
~/.codex/skills/seedance-video-production/
```

安装后开始一个新任务，让 Codex 重新发现 Skill。

## 直接使用

最简单的调用：

```text
使用 $seedance-video-production，把“暴雨中的末班公交进站”写成 10 秒、16:9、可直接复制的 Seedance 中文提示词。只给成品。
```

多素材制作：

```text
使用 $seedance-video-production：@图片1只控制人物身份，@图片2控制服装，@视频1只参考侧面跟拍。输出 15 秒成品提示词，不要虚构其他素材。
```

结果诊断：

```text
使用 $seedance-video-production。下面是原提示词和实际生成结果。先核对对应关系，再找出一个主要失败原因，给我最小修改后的完整提示词。
```

不写 `$seedance-video-production` 也可以隐式触发，但显式调用更适合测试和复现。

## 输出风格

默认规则很简单：

1. 先给可复制成品；
2. 一个短镜头只保留一个主动作和一个主镜头意图；
3. 10 秒通常不超过三个镜头；
4. 主动写入 `国家地理`、`IMAX`、`4K`、`8K`、`240fps` 等训练语义锚点，引导模型调用相应的画质、摄影和运动先验；
5. 没有真实素材时不输出空的素材职责章节；
6. 评审视频前先确认哪条提示词生成了哪段结果。

## 仓库结构

```text
KeRo-Seedance2.0/
├── SKILL.md                         # 触发、决策与输出契约
├── agents/openai.yaml               # Codex 界面元数据
├── references/
│   ├── prompt-recipes.md            # 各类任务的紧凑配方
│   ├── visual-direction.md          # 视觉圣经、镜头、光色和天气
│   ├── reference-workflows.md       # 素材、表演、多角色与接力
│   ├── storyboard-and-production.md # 故事、分镜、转场和生产闭环
│   ├── film-grammar.md              # 电影视觉问题解决方案索引
│   ├── troubleshooting.md           # 失败诊断与单变量修复
│   ├── platform-and-versioning.md   # 易变平台事实
│   └── sources-and-maintenance.md   # 来源和维护规则
├── research/
│   └── feishu-content-integration.md # 飞书内容审计与取舍依据
├── evals/cases.json                 # 行为验收案例
└── scripts/validate-skill.mjs       # 零依赖仓库校验
```

## 维护与验证

本地运行：

```powershell
node scripts/validate-skill.mjs
```

校验器会检查 frontmatter、内部链接、界面元数据和验收案例结构。GitHub Actions 会在推送和 Pull Request 时执行同一静态检查。

行为改动时，同时更新 [evals/cases.json](./evals/cases.json)，再用独立 Codex 任务运行相关案例。CI 只验证案例文件的结构，不会自动判断模型输出语义。案例不是提示词模板，而是用来发现以下退化：无素材却虚构 `@引用`、简单任务输出空表格、没有核对因果就批评提示词、错误删除训练语义锚点、复杂项目缺少视觉和生产控制。

## 平台事实

截至仓库内标注的核实日期，字节跳动 Seed 官方资料确认 Seedance 2.0 支持文字、图片、视频和音频输入，可同时输入最多 9 张图片、3 段视频和 3 段音频，并支持 15 秒高质量多镜头音视频输出。不同产品入口可能不同，实际生成前以当前界面为准。

来源和更新方法见 [sources-and-maintenance.md](./references/sources-and-maintenance.md)。

飞书教程、5 份手册和 23 部电影分镜资料没有被整篇复制进 Skill；仓库只保存重新抽象的控制方法。完整取舍依据见 [飞书内容整合研究](./research/feishu-content-integration.md)。

## 关于作者

**秋水 Kero**，AIGC 创作者，持续分享 AI、图片、电商视觉与视频生产工作流。

X（推特）：[@Isonlyonenice](https://x.com/Isonlyonenice)
