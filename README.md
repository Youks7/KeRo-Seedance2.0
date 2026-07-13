<h1 align="center">KeRo-Seedance2.0</h1>

<p align="center"><strong>先给可复制成品，再按需展开制作控制</strong></p>

<p align="center">短提示词 · 视觉导演 · 多模态参考 · 分镜生产 · 结果诊断 · 连续性接力</p>

<p align="center">作者：<a href="https://x.com/Isonlyonenice"><strong>秋水 Kero</strong></a></p>

---

## 这是什么

KeRo-Seedance2.0 是一个面向 Seedance 2.0 与即梦 AI 的 Codex 插件。它默认先把创意、参考素材或失败结果转成可直接复制的成品提示词；只有复杂项目才展开视觉圣经、素材职责、分镜接力和诊断依据。

主要能力：

- 文生视频、图生视频、延长与编辑提示词；
- 图片、视频和音频参考的职责隔离；
- 角色、产品、场景和摄影连续性；
- 电影视觉语法、分镜、转场和长项目接力；
- 提示词与实际结果核对后的单变量修复；
- 当前平台事实与提示词语义锚点分离。

## 推荐安装：Codex 插件

Windows PowerShell：

```powershell
$repo = "$env:USERPROFILE\plugins\KeRo-Seedance2.0"
git clone https://github.com/Youks7/KeRo-Seedance2.0.git $repo
codex plugin marketplace add $repo
codex plugin add kero-seedance2@kero-seedance2-marketplace
```

安装或更新插件后，请开始一个新的 Codex 任务，让 Codex 重新发现插件中的 Skill。

### 只安装 Skill

不需要插件界面时，可以只安装运行时 Skill：

```powershell
$installer = "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py"
python $installer --repo Youks7/KeRo-Seedance2.0 --path plugins/kero-seedance2/skills/seedance-video-production
```

不要把整个仓库直接克隆到 `~/.codex/skills/`。仓库根目录还包含研究、评测和 CI，它们不属于运行时 Skill。

## 直接使用

简单提示词：

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

明确提到 Seedance、即梦或已经确认目标入口时可以隐式触发；显式调用更适合测试和复现。其他视频模型不会因为只出现“分镜、运镜、文生视频”等通用词而自动调用本 Skill。

## 输出原则

1. 先给可复制成品；
2. 一个短镜头只保留一个主动作和一个主镜头意图；
3. 10 秒任务通常控制在一至三个镜头；
4. 保留用户明确要求或实际结果已验证有效的 `国家地理`、`IMAX`、`4K`、`240fps` 等语义引导锚点；
5. 这些词用于描述期望观感，不冒充真实导出分辨率或帧率，也不推断模型内部启用了特定训练模块；
6. 没有真实素材时不输出空的素材职责章节；
7. 评审视频前先确认哪条提示词生成了哪段结果。

## 仓库结构

```text
KeRo-Seedance2.0/
├── .agents/plugins/marketplace.json        # 仓库 marketplace
├── plugins/kero-seedance2/                 # 可发布插件包
│   ├── .codex-plugin/plugin.json
│   └── skills/seedance-video-production/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/
├── docs/sources-and-maintenance.md         # 来源与维护规则
├── research/feishu-content-integration.md  # 历史整合审计
├── evals/cases.json                        # 行为验收合同
├── scripts/validate-repository.py          # 仓库与发行包校验
└── LICENSE                                 # MIT
```

运行时插件包只包含插件清单、Skill、界面元数据和按需参考；研究、评测和维护材料不会进入 Skill 上下文。

## 维护与验证

```powershell
python -m pip install -r requirements-dev.txt
python scripts/validate-repository.py
```

静态校验负责检查插件与 marketplace 清单、真实 YAML、Skill frontmatter、运行包边界、按需参考路由、内部链接和 eval 合同结构。行为改动仍需在全新 Codex 任务中运行相关案例；CI 不会冒充模型输出语义评审器。

当前官方来源与维护方法见 [sources-and-maintenance.md](./docs/sources-and-maintenance.md)。飞书教程、5 份手册和 23 部电影分镜资料的取舍过程见 [飞书内容整合研究](./research/feishu-content-integration.md)。

## 关于作者与许可证

**秋水 Kero**，AIGC 创作者，持续分享 AI、图片、电商视觉与视频生产工作流。

X（推特）：[@Isonlyonenice](https://x.com/Isonlyonenice)

本项目采用 [MIT License](./LICENSE)。
