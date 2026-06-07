# GenUI `generative_ui` 

本仓库是 **一个可视化子 Skill**（两工具 + 编排 + 规范文件）。当前 LLM 实现是 **Gemini** 模型为gemini-3.5-flash；不要轻易更换模型除非你测好了（gemini-3.1-flash-lite-preview很炸裂）。
！！！思考模型比如gemini-3.1-pro-preview等可能需要单独准备provider（而且消耗的时间会长很多）

---

## 1. 你要挂进主系统的四样东西

1. **`agent/skills/generative_ui/SKILL.md`** → 并进全局 system（至少：先 `visualize_read_me` 再 `show_widget`、`widget_code` 规则）。
！！！部分可能要重写，比如skill的description，模型如何知道他和是要调用这个skill，本地测试时默认都要调用这个skill所以这部分写的不是很好
2. **`agent/guidelines/fragments/` + `agent/skills/generative_ui/directions.py`** → 规范的唯一真相源，按正交维度拆分（core 哲学/工艺/布局/技术契约、aesthetic direction 库、各模块技术指南、planning 阶段措辞、few-shot 示例）。`bundler.py` 在运行时按 `_MODULE_PLAN` 组合成完整文档；`visualize_read_me` 与 `prompts._guideline_bundle` 都走组合器。顶层 `agent/guidelines/<模块>.md` 是 **生成产物**（供人工查阅/外部按文件消费），改 fragments 后用 `python -m agent.skills.generative_ui.bundler` 重新生成，**不要直接编辑**。一致性测试：`python -m tests.test_guidelines_bundler`。
3. **两个 tool 定义** → 与 `VisualizeReadMeTool` / `ShowWidgetTool` 的 `to_definition()` **同名、同 JSON Schema**（实现见 `agent/skills/generative_ui/tools/*.py`）。
4. **编排** →  **`GenerativeUIOrchestrator`** + **`AgentLoop`**（`orchestrator.py`、`agent/core/agent.py`）。（感觉有点过度设计）

视觉是否走这套流程，要和 **`agent/skills/generative_ui/visual_triggers.py`**（本地测试用的，感觉不是很必要） 与 `loader.build_system_prompt` 里对模型的说明 **一致**；否则 `get_tool_choice` 和模型判断会对不上。

---

## 2. 编排可能要对齐的行为

每轮调模型前：`orchestrator.get_tool_choice()` → 映射到你们 `tool_choice` 等价物。  
执行工具前：`before_tool_call`（未读规范禁止真执行 `show_widget`，要注入占位 + user 句）。  
工具返回后：`after_tool_execution`（处理 `READ_ME_REQUIRED`、`INVALID_WIDGET_CODE`、是否 skip + 注入纠正）。  
模型本轮 **无 tool_calls** 且仍在可视化流程：`on_no_tool_calls` → **加纠正消息并重试**，不要当普通收束。  
`show_widget` 成功后打标，防重复 `show_widget`。

细节以代码为准：`agent/skills/generative_ui/orchestrator.py`、`agent/core/agent.py`。

---

## 3. 两个工具（字段与特殊返回值）

- **`visualize_read_me`**：`modules` 为 **长度 1** 的数组；模块枚举见 `GenUIAgentService.__init__` 里 `read_me_module_names`。成功返回包在 `<module name="…">` 里的 md 正文；失败文案含 **`No guidelines found`**。
- **`show_widget`**：必填 `i_have_seen_read_me`, `widget_type`, `title`, `widget_code` 等（见 `show_widget.py`）。`i_have_seen_read_me` 为 false → 工具结果 **`READ_ME_REQUIRED`**；代码不合法 → **`INVALID_WIDGET_CODE`**。前端要渲染的最终 HTML 在 **`widget_code`**；主系统消息里建议落到 **`blocks` 里 type=widget** 一类结构，否则历史无法还原（加载历史会话时保证这部分可以持久存储和加载）。

---

## 4. 配置

`GEMINI_API_KEY` 或 `GOOGLE_API_KEY`；可选 `GEMINI_MODEL`（默认见 `agent/core/config.py`）。调试全量模型日志：`GENUI_LOG_MODEL_FULL=1`（见 `agent/core/agent.py`）。

---

## 5. 可选：用本仓库当 HTTP 适配层

`python main.py` → `POST /chat/stream`，body `message` + 可选 `session_id`，响应 SSE。事件名与 `data` 字段看 **`main.py`**（`session` / `message_start` / `assistant_delta` / `toolcall_*` / `message_end`）。**Skill 已进主系统时可忽略本节。**

---

## 6. 会话目录（用本仓库 `GenUIAgentService` 时）

默认把会话 JSON 写到 **`backend/frontend/sessions`**（`agent/service.py` 里 `SessionStore` 路径）。目录不存在会挂；改路径或自建目录即可。主系统自管会话则替换 `SessionStore` 或不用本 `service`。

---

## 7. 依赖

`requirements.txt`：`flask`、`flask-cors`、`google-genai`、`python-dotenv`。建议 Python **3.11+**。

---

**对照代码入口**：编排 `orchestrator.py` + `agent.py`；组装消息与流 `agent/service.py`；HTTP `main.py`。
