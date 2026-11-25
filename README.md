# TikTok Studio Video Publisher

这是一个面向已确认 TikTok Studio 会话的发布流程 Skill：上传准备好的 MP4、写入越南语说明与话题、轮换平台音乐、把平台音乐压到低音量、设置预约时间，并核对作品行。可选接入 `tiktok-agent-publisher` 做 API 预上传，随后回到 Studio 完成音乐、混音和预约。

## 使用方式

1. 读取 `SKILL.md`，确认目标窗口、账号、文件顺序和实际发布授权。
2. 用 `scripts/plan_schedule.py` 生成时间槽与音乐轮换计划。
3. 按 `references/publishing-checklist.md` 逐条执行并在每个检查点重新读取界面状态。
4. 按 `references/caption-and-audit-schema.md` 保存发布审计记录。
5. 若已配置外部 API 技能，先读 `references/api-acceleration.md`；API 只负责预上传/状态轮询，不替代 Studio 的热门音乐、音量或预约步骤。

## 包结构

- `SKILL.md`：触发边界、执行流程和安全门禁。
- `agents/interface.yaml`：跨运行时接口与外部发布信任声明。
- `manifest.json`：生命周期、所有者和回滚边界。
- `references/`：发布检查、音乐策略、说明与审计字段，以及 API 混合路由边界。
- `references/api-acceleration.md`：官方 API 预上传与 Studio 混合路由边界。
- `scripts/plan_schedule.py`：无网络、无浏览器副作用的计划生成器。
- `evals/trigger_cases.json`：触发与近邻边界样例。
- `reports/`：YAO Meta Skill 生成的评估与审查证据。

## 已知限制

TikTok 页面会改变界面文本和音乐库；真实发布状态、说明持久化、曲名和音量必须在用户确认的窗口中实时核验。缺少作品行证据时，Skill 只能返回 `pending`，不能声称发布成功。
