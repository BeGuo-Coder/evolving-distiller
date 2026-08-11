[中文](README.md) | [English](README_EN.md)

# Evolving Distiller

一个面向长期使用的、证据驱动的自进化 Skill 蒸馏系统。

它不是简单地把资料总结成提示词，也不是把几个 Skill 拼接在一起，而是把持续流入的知识编译成可追溯、可测试、可回滚、可持续进化的 Skill。

核心流程：

```text
Raw Knowledge
    ↓
Structured Evidence
    ↓
Claims
    ↓
Mental / Operating Models
    ↓
Executable Skill
    ↓
Regression / Challenge / Shadow Tests
    ↓
Runtime Feedback & New Evidence
    ↓
Controlled Evolution
    ↓
New Stable Version
```

## 项目定位

Evolving Distiller 解决的是一个比“一次性生成 Skill”更长期的问题：

> 当新的资料、真实使用反馈、失败案例持续出现时，如何让一个 Skill 变得更好，同时避免知识漂移、过拟合、无证据扩张和自我优化失控？

因此系统被拆成两个闭环：

```text
Distillation Loop
Sources → Evidence → Claims → Models → Instructions → Tests → Stable Skill

Evolution Loop
Delta / Failure → Mutation → Candidate → Gates → Tests → Paired Judges
                                              ↓
                                      Keep or Revert
                                              ↓
                                      Evolution Memory
```

默认进化的是蒸馏后生成的子 Skill。只有在用户明确要求时，才允许进入 Meta Evolution，修改 Evolving Distiller 自身。

## 核心能力

### 1. Evidence-grounded Distillation

将人物、团队、公司、领域知识、访谈、文档、课程、研究资料或已有 Skill 转换为可执行 Skill。

重点不是提取“说过什么”，而是提取：

- 信念是如何形成的；
- 真实决策是如何做出的；
- 哪些失败改变了后续判断；
- 哪些方法在不同场景中反复出现；
- 哪些观点存在真实矛盾；
- 哪些场景属于认知边界；
- 哪些机制值得变成可执行规则。

### 2. Claim–Evidence Graph

系统维护一条完整的可追溯链路：

```text
Evidence E → Claim C → Model M → Instruction I → Test T
```

例如：

```text
E023 → C014 → M03 → I018 → T07
```

当新资料改变 `E023` 时，可以沿图谱找到受影响的 Claim、Model、Instruction 和 Test，而不是重新蒸馏整个 Skill。

这使知识更新从“全文重写”变成类似编译系统的“增量更新”。

相关文件：

- `references/claim-evidence-graph.md`
- `scripts/graph_audit.py`

## 3. Delta Distillation

新资料进入系统后，默认不修改稳定 Skill。

系统先判断新信息属于：

- `reinforce`：增强已有结论；
- `weaken`：降低已有结论的置信度或适用范围；
- `contradict`：出现无法直接调和的反证；
- `new_candidate`：可能形成新的 Claim / Model；
- `no_action`：重复、装饰性或不足以影响执行行为的信息。

核心原则：

> 没有认知变化，就没有 Skill 变化。

相关文件：

- `references/delta-distillation.md`
- `scripts/detect_delta.py`

## 4. Regression / Challenge / Shadow 三层测试

每个长期进化的 Skill 维护三套测试。

### Regression

固定的核心能力测试。

作用：防止新版本修好了一个问题，却破坏旧能力。

### Challenge

来自真实失败、用户纠正和困难场景。

作用：确保本次进化真正解决了触发问题。

### Shadow

候选 Skill 在生成和优化阶段不可见的保留测试。

作用：判断候选是否只是针对已知测试“刷题”。

典型 Promotion Gate：

```text
Hard Gates = PASS
Regression(candidate) >= Regression(incumbent)
Challenge(candidate)  > Challenge(incumbent)
Shadow(candidate)     >= Shadow(incumbent)
Paired Judges: better > worse
```

任何一项失败，都保留 incumbent，不把 candidate 升级成稳定版本。

相关文件：

- `references/evaluation-rubric.md`
- `references/regression-suite.md`
- `scripts/suite_gate.py`
- `scripts/pairwise_vote.py`

## 5. Evolution Memory + Mutation Operators

Evolving Distiller 不只记住成功升级，也保留失败实验。

```text
evolution/
├── history.jsonl
├── failures.jsonl
├── patterns.json
└── state.json
```

系统支持受控的 Mutation Operators：

| Operator | 含义 |
|---|---|
| PROMOTE | 将有充分证据的弱规则提升为核心模型 |
| DEMOTE | 将证据不足的核心模型降级为启发式 |
| SPLIT | 将过大的模型拆成上下文相关模型 |
| MERGE | 合并高度重复的模型 |
| WEAKEN | 将绝对规则改为条件规则 |
| BOUND | 增加明确适用边界 |
| CONTRADICT | 将冲突显式建模为张力 |
| DELETE | 删除无价值或无证据规则 |
| COMPRESS | 保留能力的同时减少冗余 |
| RESTRUCTURE | 改结构，不改变核心知识 |

历史统计会用于降低高失败率 mutation 的优先级，避免重复踩同一种坑。

相关文件：

- `references/mutation-operators.md`
- `references/evolution-protocol.md`
- `scripts/evolution_log.py`
- `scripts/evolution_memory.py`

## 6. Immutable Evolution Constitution

自进化系统最危险的问题之一，是优化器最终“优化掉自己的约束”。

因此 Evolving Distiller 把部分规则定义成 Meta Evolution 不可自主修改的 Constitution，例如：

1. 不得删除 provenance 要求；
2. 不得取消 keep / revert；
3. 不得让 candidate 自己成为唯一 judge；
4. 不得降低 promotion hard gates；
5. 不得直接覆盖 stable version；
6. 不得为了提高测试分数偷偷修改测试标准；
7. 不得把 weak inference 自动升级为事实；
8. 不得删除失败历史；
9. 不得把 Shadow Tests 暴露给 candidate author；
10. Meta Evolution 最终升级必须有人类确认。

相关文件：

- `references/evolution-constitution.md`
- `references/constitution.json`
- `scripts/constitution_guard.py`

## 适合蒸馏什么

Evolving Distiller 不局限于“人物思维 Skill”。

```text
Person
→ Cognitive Skill

Team / Company
→ Operating Skill

Books / Interviews / Course Corpus
→ Framework Skill

Research Field
→ Research Skill

Successful Cases
→ Pattern Skill

Failed Cases
→ Anti-pattern Skill

Existing Skill + Feedback
→ Evolved Skill
```

它更接近一个：

> Evidence-to-Skill Compiler + Skill Evolution Engine

## 使用方式

### 场景 A：从资料创建 Skill

可以直接提供：

- PDF、Markdown、TXT、访谈稿、课程稿；
- 笔记或知识库导出；
- 一组 URL 或公开资料；
- 某个人、团队、公司或领域主题。

示例：

```text
把这些访谈和文章蒸馏成一个可以长期使用的决策 Skill。
```

系统会依次处理：

```text
素材
→ 证据提取
→ Claim-Evidence Graph
→ 模型合成
→ Child Skill
→ 三层测试
→ 稳定版本
```

### 场景 B：用新资料更新已有 Skill

```text
这是最近新增的三篇访谈，检查它们是否需要更新现有 Skill。
```

系统不会默认重写 Skill，而是执行：

```text
Old Evidence vs New Evidence
→ Delta
→ Impact Graph
→ Candidate Mutation
→ Regression / Challenge / Shadow
→ Keep / Revert
```

### 场景 C：从真实失败中进化

```text
刚才这个回答明显违背了这个 Skill 的方法，把它作为失败案例修复。
```

真实失败可以进入 Challenge Set，并参与后续进化。

### 场景 D：进化 Evolving Distiller 自身

需要明确提出类似：

```text
进化 evolving-distiller 本身。
```

Meta Evolution 会额外启用 Constitution Guard，并要求最终人工确认。

## 目录结构

```text
evolving-distiller/
├── README.md
├── README_EN.md
├── NOTICE.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── attribution.md
│   ├── child-skill-template.md
│   ├── claim-evidence-graph.md
│   ├── constitution.json
│   ├── delta-distillation.md
│   ├── distillation-protocol.md
│   ├── evaluation-rubric.md
│   ├── evolution-constitution.md
│   ├── evolution-protocol.md
│   ├── mutation-operators.md
│   ├── regression-suite.md
│   └── schemas.md
└── scripts/
    ├── constitution_guard.py
    ├── detect_delta.py
    ├── evidence_audit.py
    ├── evolution_log.py
    ├── evolution_memory.py
    ├── graph_audit.py
    ├── pairwise_vote.py
    ├── self_test.py
    └── suite_gate.py
```

## 安装

### ChatGPT Skills

将完整 Skill 文件夹打包为 `skill.zip` 后，在支持 Skills 的环境中上传。

本项目已经包含标准 Skill 入口：

```text
SKILL.md
agents/openai.yaml
```

### 其他兼容 Runtime

本 Skill 的核心流程尽量保持 runtime-neutral。对于支持 Skill / Agent Skill 目录的运行环境，可将完整目录放入该 Runtime 规定的 Skill 位置。

如果某个运行环境不支持独立子 Agent、文件执行或 Git，按 `SKILL.md` 中的 fallback 规则降级运行，不应伪装已经执行了不可用能力。

## 本地自测

项目自带机械层 smoke test：

```bash
python scripts/self_test.py
```

当前自测覆盖：

- Claim–Evidence Graph；
- Delta Distillation；
- Layered Test Gate；
- Evolution Memory + Mutation；
- Evolution Constitution。

单独使用各工具时可参考对应 `references/` 文档和脚本参数。

## 设计原则

这个项目遵循几个长期约束：

- Evidence first，而不是 Prompt first；
- Model first，而不是金句 first；
- Delta first，而不是全文重写；
- Test before promotion；
- Pairwise comparison，而不是依赖单一绝对评分；
- Keep / Revert，而不是只允许前进；
- Failed experiments are memory；
- Stable version 与 Candidate version 严格分离；
- Meta optimizer 不得自主修改自己的宪法。

## 设计来源与 Attribution

本项目是独立重新设计和组合的实现，受到以下公开开源项目的设计启发：

- [alchaincyf/darwin-skill](https://github.com/alchaincyf/darwin-skill)
- [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill)
- [zjjoe2025/cangjie-skill-](https://github.com/zjjoe2025/cangjie-skill-) / upstream [Yeadon8888/cangjie-skill](https://github.com/Yeadon8888/cangjie-skill)

主要吸收的设计方向包括验证驱动优化、paired keep/revert、多源认知蒸馏、思维模型提取、证据化研究记录、失败/矛盾/边界提取等。

本项目没有直接复制上述项目的 `SKILL.md` 文本，而是重新组织为 Evidence-grounded Distillation + Validation-gated Evolution 双循环架构。

具体说明见：`references/attribution.md`。

## 版权说明

本 `evolving-distiller` 分发包中的原创整合工作、工作流设计、维护说明、后续迭代及社区维护版本，由维护者保留相应权利，另有说明的内容除外。

上游开源项目及其代码、文档、设计内容仍分别遵循各自原始许可证和版权条款。本项目的版权声明不会覆盖或限制任何上游开源许可证已经授予的权利。

完整说明见：`NOTICE.md`。

## 内容工厂 Skills 社群

本人搭建了「内容工厂 Skills 社群」，每周持续补充和筛选实用 Skills，包括：

- 自用并持续迭代的 Skills；
- 已验证公开、效果较好的 Skills；
- 内容生产、研究、知识库、自动化和 Agent 工作流相关实践版本。

感兴趣可以联系：`deepgpt911`

当前早期加入价格：**299 元 / 年**。

定价规则：**每增加 50 人，年费增加 100 元。**

价格、权益与更新节奏以后续公布的信息为准。

## 当前状态

Evolving Distiller 已实现并通过本地 smoke test 的核心模块：

```text
Claim–Evidence Graph
Delta Distillation
Regression / Challenge / Shadow
Evolution Memory + Mutation Operators
Immutable Evolution Constitution
```

下一阶段最重要的方向不是继续增加规则，而是接入真实长期使用反馈：

```text
User Correction
Runtime Failure
Human Revision
New Evidence
        ↓
Challenge / Evidence Stream
        ↓
Controlled Evolution
```

最终目标是让 Skill 不只是“生成一次”，而是在长期使用过程中有证据地持续变强。
