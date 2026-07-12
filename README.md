<h1 align="center">KeRo-Seedance2.0</h1>

<p align="center"><strong>先建立可执行的导演控制，再生成稳定、连贯、可剪辑的 Seedance 视频</strong></p>

<p align="center">角色一致性 · 多模态参考 · 镜头因果 · 长视频接力 · 音画协同</p>

<p align="center">
  <a href="./SKILL.md">查看 Skill</a> ·
  <a href="./references/prompt-patterns.md">提示词模板</a> ·
  <a href="./references/evaluation-rubric.md">故障诊断</a> ·
  <a href="./references/sources-and-maintenance.md">来源与维护</a>
</p>

---

## 这是什么

KeRo-Seedance2.0 是一个面向 **Seedance 与即梦 AI 视频生产** 的 Codex Skill。

它不把视频提示词理解成风格词堆叠，而是把视频任务拆成可控制的生产流程：

```text
创意、脚本或参考素材
   ↓
识别目标、时长、比例和交付平台
   ↓
给每张图片、视频、音频分配唯一职责
   ↓
建立角色、产品、场景与摄影连续性锚点
   ↓
设计动作因果、镜头路径、声音和稳定尾帧
   ↓
输出可复制提示词、负面约束与迭代顺序
```

当前公开仓库是 **精简核心版**：保留完整执行流程和常用参考，适合公开安装、快速调用和日常维护。

## 核心能力

| 能力 | 主要职责 |
|---|---|
| 需求解析 | 识别叙事目的、主体、时长、平台、声音和交付规格 |
| 素材职责 | 为 `@图片N`、`@视频N`、`@音频N` 指定明确控制层 |
| 角色一致性 | 分离身份、服装、道具、表演和镜头动作 |
| 镜头设计 | 用景别、机位、运动、光学、构图和光色建立镜头 |
| 动作因果 | 按起点、触发、发展、结果和尾帧组织动作 |
| 长视频接力 | 为多段生成保存入点、出点和连续性锚点 |
| 视频延长与编辑 | 明确保留项、替换项和不得改变项 |
| 音画控制 | 规划对白、环境声、拟音、音乐和同步节点 |
| 失败诊断 | 排查换脸、肢体融合、镜头失控、跳变和文字不可读 |

## 适合谁使用

- AI 视频创作者：需要稳定、可复制的 Seedance 提示词。
- 短剧和广告团队：需要角色、产品和场景连续性。
- 导演与分镜师：需要把脚本转成时间轴和镜头方案。
- 电商与品牌团队：需要产品结构保护、包装文字和品牌收束。
- AIGC 工作流维护者：需要可校验、可迭代的 Skill 仓库。

## 你想做什么，直接看这里

| 你的需求 | 建议入口 |
|---|---|
| 了解 Skill 如何触发和工作 | [SKILL.md](./SKILL.md) |
| 查询当前平台和版本处理 | [platform-and-versioning.md](./references/platform-and-versioning.md) |
| 保持角色、产品和场景一致 | [directing-workflow.md](./references/directing-workflow.md) |
| 查景别、运镜、构图和光线 | [cinematic-language.md](./references/cinematic-language.md) |
| 套用文生视频、延长或编辑模板 | [prompt-patterns.md](./references/prompt-patterns.md) |
| 做长视频、广告、短剧和后期 | [story-and-production.md](./references/story-and-production.md) |
| 借鉴经典电影的摄影原则 | [film-pattern-index.md](./references/film-pattern-index.md) |
| 诊断生成失败 | [evaluation-rubric.md](./references/evaluation-rubric.md) |

## 三种工作模式

### 快速模式

适合单镜头、单主体或只需要一条提示词的任务。输出可复制提示词、必要默认值和关键注意事项。

### 制作模式

适合广告、短片、短剧、MV、多素材参考和角色一致性任务。输出创作简报、素材职责、视觉锚点、分镜、提示词、负面约束和生成顺序。

### 长片段模式

适合超过单次生成限制、跨场景叙事或需要拼接的项目。每段都包含入点、动作、摄影、声音、出点和下一段接力锚点。

## 快速安装

### 方法一：直接克隆到 Codex Skills 目录

Windows PowerShell：

```powershell
git clone https://github.com/Youks7/KeRo-Seedance2.0.git "$env:USERPROFILE\.codex\skills\seedance-video-production"
```

### 方法二：手动复制

将仓库目录复制到：

```text
~/.codex/skills/seedance-video-production/
```

确认目录中直接存在：

```text
SKILL.md
agents/openai.yaml
references/
```

## 第一次使用

简单任务：

```text
请使用 $seedance-video-production，把“雨夜便利店门口的重逢”写成一条9:16、10秒、可直接复制的 Seedance 中文提示词。
```

多素材任务：

```text
请使用 $seedance-video-production：
@图片1控制角色身份，@图片2控制服装，@图片3控制场景，@视频1只参考运镜。
先输出素材职责表，再给15秒分镜和可复制提示词。
```

长视频任务：

```text
请使用 $seedance-video-production，把这段45秒广告拆成可生成片段。
每段写入点、出点、声音接力和下一段必须继承的连续性锚点。
```

## 不可违反的规则

1. 不虚构用户没有提供的 `@图片N`、`@视频N` 或 `@音频N`。
2. 不把历史版本参数当作永久平台限制。
3. 不把“4K、8K、RAW、HDR”等风格词冒充真实输出规格。
4. 不默认禁止所有文字和 Logo；根据品牌与交付目标决定。
5. 使用真人人像参考时，确认本人验证或合法授权要求。
6. 复杂任务一次只修改一个控制层，保留可追溯迭代记录。

## 项目结构

```text
KeRo-Seedance2.0/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── platform-and-versioning.md
    ├── directing-workflow.md
    ├── cinematic-language.md
    ├── prompt-patterns.md
    ├── story-and-production.md
    ├── film-pattern-index.md
    ├── evaluation-rubric.md
    └── sources-and-maintenance.md
```

## 精简版与完整版

- 本仓库：公开精简核心版，适合安装、分享和快速使用。
- 完整版：私有维护仓库，包含全章节教程、完整手册索引、23部电影和138个分镜节点。
- 两个版本共享同一核心 `SKILL.md` 设计；完整版通过 references 按需加载，不要求 Agent 一次读取全部内容。

## 来源与版本

本项目融合并重写了用户提供的 Seedance Skill 草案、实战教程、镜头与剧本手册和电影分镜资料。详细来源、官方核实链接和维护规则见 [sources-and-maintenance.md](./references/sources-and-maintenance.md)。

当前仓库不把课程中的“Seedance 2.5”直接声明为官方统一型号；模型名称与平台能力以当前官方页面和实际界面为准。

## 关于作者

**秋水 Kero**，AIGC 创作者，持续分享 AI、图片、电商视觉与视频生产工作流。

X（推特）：[@Isonlyonenice](https://x.com/Isonlyonenice)
