# OpenSkills 安装与使用（CLI）

> **OpenSkills** 指社区工具 **[numman-ali/openskills](https://github.com/numman-ali/openskills)**：用 `npx openskills` 从 Git 安装技能包、同步生成 `AGENTS.md`，让 **Cursor、Claude Code、Aider、Windsurf、Codex** 等能读同一份「技能注册表」。

下面说的「技能源」以官方技能仓库 **[anthropics/skills](https://github.com/anthropics/skills)** 为主（技能本体在 `skills/*`，每个子目录一个 skill）。

> **易混名称**：另有 Python 包 **`openskills-sdk`**（另一套 Agent Skill 框架，偏 SDK/运行时），与本文的 **npm `openskills` CLI** 不是同一个项目。接 CLI 时搜仓库 **numman-ali/openskills** 即可。

## 1. 环境要求

- **Node.js** ≥ **20.6**（`npx openskills` 需要）
- **Git**（从 GitHub 克隆/更新技能包时用）
- 已登录或能拉取的 GitHub 访问方式（公网/SSH/私有仓库按你的环境配置）

## 2. 安装方式

### 2.1 推荐：不全局安装，直接用 npx

在任意项目根目录执行即可，**无需**先 `npm i -g`：

```bash
npx openskills@latest --help
```

### 2.2 可选：全局安装

```bash
npm i -g openskills
openskills --help
```

适合频繁使用、不想每次打 `npx` 的情况。

## 3. 一分钟上手

在项目根目录（建议与代码仓库根一致）执行：

```bash
# 从 Anthropic 官方技能仓库安装（GitHub: anthropics/skills）
npx openskills install anthropics/skills

# 根据已安装技能，生成/更新 AGENTS.md（给各类 agent 读「有哪些 skill、何时用」）
npx openskills sync
```

若仓库里还没有 `AGENTS.md`，`sync` 会生成；**若已有** `AGENTS.md`，会**更新**其内容（注意提前备份或提交 git，再执行）。

`AGENTS.md` 的作用：让 **任何能读该文件的 agent**（或你在 Cursor 里 @ 它）知道当前项目装了哪些 skill、各 skill 的 `description` 与触发方式。

## 4. 常用命令

| 命令 | 作用 |
|------|------|
| `npx openskills install <来源>` | 安装技能包：GitHub `org/repo`、本地路径、`git@...` 私有库等 |
| `npx openskills sync` | 据已安装 skill 更新 `AGENTS.md`（默认可用 `-o` 指定输出文件） |
| `npx openskills list` | 列出已安装 skill |
| `npx openskills read <name>` | 在终端里输出某个 skill 内容（调试用/给脚本管道） |
| `npx openskills update [name...]` | 从来源更新已安装 skill（默认全部） |
| `npx openskills manage` | 交互式管理（含移除） |
| `npx openskills remove <name>` | 删除指定 skill |

### 4.1 常用参数

| 参数 | 含义 |
|------|------|
| `--global` | 装到用户目录，例如 `~/.claude/skills`（跨项目复用） |
| `--universal` | 装到 `.agent/skills/`，和 Claude 插件/市场路径区分，**多工具混用时**常用 |
| `-y, --yes` | 非交互、适合 CI |
| `-o, --output <path>` | 指定 `sync` 写出的文件，默认 `AGENTS.md` |

**多工具并存时的搜索优先级**（`--universal` 时，高优先在前）：

1. `./.agent/skills/`
2. `~/.agent/skills/`
3. `./.claude/skills/`
4. `~/.claude/skills/`

## 5. 安装来源示例

### 5.1 从 GitHub 仓库

```bash
npx openskills install anthropics/skills
npx openskills install your-org/your-skills
```

### 5.2 从本地目录（你自己写的 skill）

```bash
npx openskills install ./my-skill
```

目录里应有 `SKILL.md`（与 Cursor/Claude 技能规范一致）。

### 5.3 从私有 Git

```bash
npx openskills install git@github.com:your-org/private-skills.git
```

需本机已配置好 SSH 密钥或 HTTPS 凭据。

### 5.4 多 agent 共用一个 `AGENTS.md`（universal）

```bash
npx openskills install anthropics/skills --universal
npx openskills sync
```

## 6. 装完之后在各工具里怎么用

### 6.1 Cursor

1. 打开项目，确认已存在 `.claude/skills` 或 `.agent/skills`（及 `AGENTS.md` 若你 sync 了）。
2. 在对话里**明确引用**：例如「按 `AGENTS.md` 里列出的 pdf skill 流程处理 `x.pdf`」；或直接 **@ 文件** `AGENTS.md` / 某个 `SKILL.md`。
3. 团队规范：把 `AGENTS.md` + skills **提交进 git**，全员一致。

### 6.2 Claude Code

- 技能目录与 Anthropic 生态一致时，和 **Claude Code 插件/市场** 路径协调：若和官方插件装目录冲突，**优先用 `--universal`** 装到 `.agent/skills`。
- 项目级长期说明可放在 `CLAUDE.md`；`AGENTS.md` 用于「可发现技能清单」，二者可并用。

### 6.3 Aider / 其它只认文本的工具

- 无原生 skill 时：把 `npx openskills read <name>` 的输出 **附加进会话**，或 `aider --read AGENTS.md --read .claude/skills/xxx/SKILL.md`。

## 7. 维护与排错

| 现象 | 处理 |
|------|------|
| `sync` 覆盖了你改过的 `AGENTS.md` | 先 `git commit` 或改 `-o` 到备份路径 |
| 装了很多 skill 但 agent 不「自动用」 | 依赖各客户端是否实现「按 description 自动选 skill」；**显式 @ SKILL.md 最稳** |
| 私有仓库 clone 失败 | 检查 Git SSH/HTTPS、网络、权限 |
| Node 版本过低 | 升级到 Node 20.6+ |

## 8. 与「手写 `.cursor/skills`」的关系

- **OpenSkills 安装** → 把远程/本地的 skill 目录放到 `.claude/skills` 或 `.agent/skills`。
- **Cursor 自己放 skill** → 也是 `SKILL.md` 结构，可手工维护。
- 二者可以**并存**；`sync` 只负责**汇总成 `AGENTS.md`**，不替代你在 Cursor 里点选模型或 Rule。

---

# 附录 · `anthropics/skills` 里各 skill 是做什么的

以下对应仓库 **[github.com/anthropics/skills](https://github.com/anthropics/skills)** 中 `skills/<name>/` 目录。每个 skill 都是 **指令 + 可选脚本/资源**，供 Claude / 支持 Agent Skills 的客户端按需加载。简介按 **官方仓库用途分类** 与 `SKILL.md` 的 `description` 概括。

> 以官方仓库为准；下表为学习用速览，**不替代**各目录内完整 `SKILL.md` 与许可证说明。

| 目录名 | 功能一句话 |
|--------|------------|
| **algorithmic-art** | 用 **p5.js** 做生成式/算法艺术（种子随机、可交互参数），输出哲学说明 + 单文件 HTML 等。 |
| **brand-guidelines** | 按 **Anthropic 品牌** 色板与字体，统一文档/画布的视觉风格。 |
| **canvas-design** | 用设计流程产出 **`.png` / PDF** 等静态视觉作品（版式与审美约束在 skill 内）。 |
| **claude-api** | **Anthropic / Claude API** 应用：SDK、缓存、工具调用、模型迁移、常见排错。 |
| **doc-coauthoring** | **协作文档**工作流：收集上下文、迭代大纲与段落、适合提案/技术规格/决策文。 |
| **docx** | **Word（.docx）** 创建/编辑：目录、样式、页眉页脚、表格、模板化排版等。 |
| **frontend-design** | **前端界面** 设计：强调审美与产品级 UI，而非「默认 AI 风」样式。 |
| **internal-comms** | **内部沟通** 文案：状态汇报、3P、领导更新、FAQ、事故/项目通报等格式。 |
| **mcp-builder** | 编写 **MCP（Model Context Protocol）server** 的工程指南（Python/TS 等）。 |
| **pdf** | **PDF** 读、拆、合、转文字/表格、表单、OCR 等（偏文档工程）。 |
| **pptx** | **PowerPoint（.pptx）** 的创建/编辑/版式/演讲者备注等。 |
| **skill-creator** | **设计、评估、优化** Agent Skill 本身：触发词、可维护性、评测与迭代。 |
| **slack-gif-creator** | 做适合 **Slack 尺寸/时长** 的动图 GIF 的思路与约束。 |
| **theme-factory** | 为 deck/文档/网页等生成 **可复用主题**（色板与字体搭配）。 |
| **web-artifacts-builder** | 用 **React + Tailwind + shadcn/ui** 等构建较复杂的 **多组件 Web artifact**（偏 claude 生态里的 artifact 场景）。 |
| **webapp-testing** | 用 **Playwright** 等做本地 **Web 应用** 的交互/截图/回归与调试流程。 |
| **xlsx** | **电子表格**（.xlsx/.csv 等）读写、公式、表、图、数据清洗。 |

**文档类说明**（来自官方 `README`）：`docx` / `pdf` / `pptx` / `xlsx` 中部分实现与 **Claude 产品内文档能力** 相关，**源码可见程度与许可**以仓库内 `LICENSE` 与 `THIRD_PARTY_NOTICES` 为准。

## 9. 延伸阅读

- [Agent Skills 标准与规范](https://github.com/anthropics/skills)（`spec/`、`agentskills.io`）
- [OpenSkills CLI 仓库](https://github.com/numman-ali/openskills)
- 本仓库同目录：[`skill_openskill_guide.md`](./skill_openskill_guide.md)（通用编写与迁移思路）
