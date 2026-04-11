
**总体思路**
- 这个项目把 **Skill** 和 **Tool** 分成两层：Skill 负责“教模型怎么做”，Tool 负责“真正执行动作”。
- Skill 是 `SKILL.md` 文档包，属于提示词/知识层，不直接执行代码，入口在 [skills.py](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/skills.py#L23-L35)。
- Tool 是可执行能力（读写文件、命令、搜索、网页、MCP 等），统一继承 `Tool` 抽象类，入口在 [base.py](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/tools/base.py#L117-L173)。
- 最终由执行循环把两者串起来：先给模型看 skills 摘要，再把 tools schema 传给模型，模型返回 tool calls 后执行，代码在 [runner.py](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/runner.py#L90-L157)。

**Skill 设计**
- Skill 目录结构是 `skills/<name>/SKILL.md`，加载器会先读工作区 skills，再读内置 skills，且工作区同名优先，见 [SkillsLoader.list_skills](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/skills.py#L52-L71)。
- `SKILL.md` 使用 frontmatter 元数据，支持 `name/description/metadata`，其中 `metadata.nanobot.requires` 可声明依赖（如 CLI/env），见 [get_skill_metadata](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/skills.py#L207-L229) 与 [weather 示例](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/skills/weather/SKILL.md#L1-L6)。
- 设计上是“渐进加载”：系统提示词只注入 skills 摘要 XML；真正内容让模型按需再读 `SKILL.md`，见 [build_skills_summary](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/skills.py#L109-L143) 和模板 [skills_section.md](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/templates/agent/skills_section.md#L1-L6)。
- 可以标记 `always` 技能，启动时自动注入到 system prompt，见 [get_always_skills](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/skills.py#L195-L205) 和 [ContextBuilder.build_system_prompt](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/context.py#L46-L55)。

**Tool 设计**
- 每个 Tool 统一三要素：`name`、`description`、`parameters(JSON Schema)`，并实现 `execute()`，见 [Tool 抽象](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/tools/base.py#L136-L173)。
- 参数层有两步防线：先做 schema 驱动类型转换（字符串转 int/bool 等），再做 JSON Schema 校验，见 [cast_params/validate_params](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/tools/base.py#L180-L233)。
- 提供 `@tool_parameters` 装饰器和 Schema DSL（`StringSchema/ObjectSchema` 等）来定义参数，减少重复，见 [tool_parameters](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/tools/base.py#L246-L279) 与 [schema.py](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/tools/schema.py#L20-L52)。
- 注册中心统一管理工具、导出函数定义、执行前准备/校验和错误包装，见 [ToolRegistry](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/tools/registry.py#L8-L99)。
- 并发策略由 `read_only/exclusive/concurrency_safe` 控制：只读工具可并发，`exec` 强制独占，见 [base 并发属性](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/tools/base.py#L155-L167) 和 [shell.py](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/tools/shell.py#L87-L90)。

**运行链路（简版）**
- `AgentLoop` 启动时注册默认工具（文件、搜索、exec、web、message、spawn、cron），见 [loop.py](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/loop.py#L229-L255)。
- 如配置 MCP，会动态连外部 server 并把能力包装成 `mcp_*` 工具注册进同一 registry，见 [connect_mcp_servers](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/tools/mcp.py#L309-L401)。
- 每轮请求把 `tools.get_definitions()` 发给模型，模型返回 `tool_calls` 后执行并把结果追加为 `role=tool` 消息，再进入下一轮，见 [runner 主循环](file:///d:/.zhuIvan/Desktop/edu/nanobot/nanobot/agent/runner.py#L124-L189)。
- 所以本质是：**Skill 决策增强（提示层） + Tool 执行闭环（运行层）**。