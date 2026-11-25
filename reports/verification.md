# 首版验证记录

日期：2026-08-06

## Pass

- `validate_skill.py`: pass，0 failures，0 warnings。
- `resource_boundary_check.py --max-initial-tokens 1000`: pass；入口约 864 tokens，Skill body 624 tokens，未发现未引用资源目录。
- `trigger_eval.py`: pass；9 个触发/非触发样例，precision 1.0，recall 1.0，false positives 0，false negatives 0。
- `plan_schedule.py --help`: pass。
- 排程计划 smoke：pass；支持 `00:30 13:30 20:30`，相邻曲目不重复，默认 `-40 dB`。
- `trust_check.py`: pass；1 个脚本通过 help smoke，0 个 secret，0 个网络脚本。
- `compile_skill.py`: pass；OpenAI、Claude、generic、Agent Skills、VS Code 五个目标均 pass。

## Pending / missing evidence

- 真实回归发现说明持久化失败：第 26 课第 3 条作品行显示 `xSK2_Bai26_Part03_MicroV3`，而非请求的越南语说明；后续批次已暂停，Skill 已加入“说明持久化探针”和 ASCII fallback 记录要求。
- 真实回归发现预约作品无法编辑：TikTok Studio 返回“无法编辑预约发布的作品”；预约前必须完成标题终检，修复已排程标题需要用户确认取消/删除并重传。
- 尚未在真实 TikTok Studio 会话中执行一整批发布回归；作品行、说明持久化、音乐库可用性和平台响度证据必须由实际会话补齐。
- 尚未生成 provider-backed output eval、盲审或人工 adjudication；不能据此宣称生产质量已完全证明。
- trust check 提示没有依赖/锁文件；当前脚本只使用 Python 标准库，仍保留该 warning。

## Boundary

技能只负责已准备好的 MP4 的上传/排程/核验，不负责视频生成、剪辑、音频制作、数据分析、删除作品或切换未确认会话。
