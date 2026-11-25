---
name: tiktok-studio-publish
description: "Use when the user asks to upload or schedule prepared MP4 videos in a user-confirmed TikTok Studio account, set Vietnamese captions and hashtags, add or rotate TikTok platform music at low volume while preserving original audio, or audit post rows. Do not trigger for video generation/editing, analytics-only work, deleting posts, or an unconfirmed browser/account."
metadata:
  author: Vanch / Codex
  version: 0.2.0
  maturity: production
  owner: Vanch
  review_cadence: monthly
---

# TikTok Studio Video Publisher

将已完成的竖屏 MP4 上传到已确认的 TikTok Studio，配置越南语说明/话题、低音量轮换音乐并预约发布；可选用 `tiktok-agent-publisher` API 预上传，再回 Studio 完成最终设置和核验。

## 触发与边界

适用于：批量上传、按顺序排程、设置标题/说明/话题、添加平台音乐、检查发布时间和发布状态。

不适用于：生成或剪辑视频、制作音频/音乐、仅做数据分析、删除或替换旧作品、未确认的浏览器窗口/账号。若当前窗口与用户指定会话不一致，立即停止。

## 输入与输出契约

- 输入：本地 MP4 路径或目录、发布顺序、说明/话题模板、时区和时间槽、可用音乐池、是否允许实际发布。
- 输出：每条视频的 `filename`、`caption_requested`、`caption_displayed`、`caption_input_mode`、`transport`、`api_publish_id`（如有）、`music_track`、`music_db`、`schedule_at`、`post_url_or_id`、`verification_status`。
- 不能看到作品行、排程时间或音乐音量的可审计证据时，状态必须为 `pending`，不得写 `success`。

## HSK2 音频硬门禁（2026-09-07）

- 已取消本地背景音乐方案。只允许纯教学音轨及原有答题提示音；禁止本地混入背景音乐。
- 上传前运行 `python3 "/Users/vanch/Downloads/Han 3 TV Course Pilot/scripts/verify_tiktok_clean_upload.py"`，必须 PASS；实际上传目录取队列 dir，禁止回退历史 shorts_v3/videos，其中仍有旧混音文件。
- 网页选曲记录曲名、作者及界面证据；推荐不等于热门，无热度证据不称为热门。
- 选中新增音乐轨设 -40 dB 并回车，原声不变；保存后重新打开编辑器核实同一曲名和 -40 dB，无法验证即停止提交。
- 作品的音乐关联须另行检查曲名/声音页。听见背景音、编辑器保存成功不代表关联成功；缺少证据时记录 music_linkage=pending。

## 平台音乐与音量关联硬门禁 (2026-11-13 最新标准)

- **核心原则**：现在本地视频素材均已在剪辑阶段配好完整背景音乐与人声音效（自带完整音频轨）。
- **关联热门音乐目的**：在 TikTok Studio 添加平台热门音乐**纯粹为了接入 TikTok 算法推荐流量池与音乐话题关联**。
- **音量控制铁律**：
  - **必须将 TikTok Studio 中添加的平台关联音乐声音完全关掉（调至静音 / 设为最低极值 -40 dB 或 Mute），严禁发出平台音乐声音**；
  - **100% 完整保留视频本身的原始音频（Original sound 保持 100% / 0 dB）**；
  - 彻底杜绝平台背景音乐与视频原有 BGM / 口播 / 音效叠加混响、打架或杂音问题。

## 执行流程

1. **预检会话**：确认 Chrome 窗口标题、TikTok Studio URL、账号头像/名称和语言界面都与用户指定会话一致；核对文件存在、顺序和目标时区。使用 Computer Use 时，每次 UI 操作后重新读取 `get_app_state`，不复用旧 element index。
2. **选择上传传输层**：默认走 Studio。若 `tiktok-agent-publisher` 已配置，先做只读状态/隐私审计；需要预约或平台音乐时仅用 API `MEDIA_UPLOAD` 预上传，记录 `transport=api_inbox_preupload`，完成后回 Studio。不可用则回退，不安装依赖、不打印令牌。
3. **生成计划**：用 `scripts/plan_schedule.py` 生成时间槽与不重复音乐；平台音乐默认 `-40 dB`，原声不变。API 预上传最多两个并发，并遵守每用户 6 次/分钟初始化限制。
4. **说明持久化探针**：首条用真实键盘输入并失焦提交；回“作品”页确认显示值一致。声调被键盘通道去掉时，改用 ASCII-safe 说明并记录 `caption_input_mode=ascii_fallback`。
5. **逐条上传/接收预上传**：Studio 直接上传；API 等待 `SEND_TO_USER_INBOX` 后回 Studio。探针未通过或作品行出现文件名/乱码即暂停并记录 `caption_persistence_failed`。
6. **配置音乐**：选不同曲目并核对曲名、`-40 dB` 数值后保存；API 不替代 Studio 的热门音乐和混音控件。
7. **定时提交前终检**：选择“预约发布”前，必须在同一页面复核 `caption_requested`、文件名、曲名、音量和时间；TikTok Studio 的预约作品通常不能再编辑，标题证据不完整时禁止提交。
8. **定时提交**：设置未来至少 15 分钟并经用户授权；API `DIRECT_POST` 是立即发布，不是预约，未审核客户端可能只能私密可见。
9. **发布后核验**：回“作品”页核对说明、时间和状态并记录链接/ID；API 状态只能辅助，不能替代作品行证据。错误标题按用户确认的取消/删除后重传处理；每 1–3 条设检查点，异常即停。

## 安全与回滚边界

发布是外部副作用：只有用户明确授权目标账号、内容和“发布/预约”动作时才可提交；否则仅生成计划。此技能不删除作品、不清空草稿、不修改账号设置。发现错误时只停止并保留审计记录，修复或重新上传需用户明确要求。

## 资源与验证

- 详细 UI 检查：`references/publishing-checklist.md`
- API 加速边界：`references/api-acceleration.md`
- 音乐轮换与响度策略：`references/music-rotation-policy.md`
- 字幕/说明与审计字段：`references/caption-and-audit-schema.md`
- 排程和音乐计划：`scripts/plan_schedule.py`
- 触发边界：`evals/trigger_cases.json`
- 首版验证与证据缺口：`reports/verification.md`

验证顺序：`python3 scripts/plan_schedule.py --help` → `python3 /Users/vanch/.codex/skills/yao-meta-skill/scripts/validate_skill.py .` → `python3 /Users/vanch/.codex/skills/yao-meta-skill/scripts/resource_boundary_check.py .` → `python3 /Users/vanch/.codex/skills/yao-meta-skill/scripts/trigger_eval.py --description-file SKILL.md --cases evals/trigger_cases.json`。平台真实发布证据仍需在用户确认的 TikTok Studio 会话中取得。


## 马来本地化内容优化与发布 SOP (2026-11 本地创作者建议升级)

为了彻底消除“机器直译感与生硬广告感”，全面提升完播率、点击率与评论区互动活跃度，后续视频制作与发布执行以下 6 项标准：

### 1. 封面选取准则 (吸睛度与明确视觉焦点)
- **禁止**：使用模糊、大远景无主体、或看不出具体产品部位的无意义开屏帧。
- **必须**：
  1. 画面中央必须有绝对清晰的**动作核心聚焦点**（如：双手拉扯高弹腰头特写、手指穿透轻薄面料透光实验、或口红盒抽出瞬间）；
  2. 优先选取浅色/高对比背景下高清晰度中近景，确保在 TikTok 个人主页 4:3 / 9:16 网格中一眼看懂卖点；
  3. 封面禁止遮挡商品关键结构。

### 2. 评论区双向互动与视频内动态引导 (提高账号活跃权重)
- **日常维护（提频促推流）**：每日定时检查并 **100% 回复用户评论**（尤其是问 "kat mana beli"、"beli kat mana"、"berapa harga" 等购买咨询），回复时热情互动并引导看左下角。
- **视频内视觉引导 (In-Video CTA)**：剪辑或后期贴纸中加入醒目的**动态箭头/手指微动效，直接指向左下角 TikTok Shop 小黄车**，配以马来语贴纸提示（如："Tekan beg kuning kat sini 🛒👇"），降低问询门槛，缩短进店路径。

### 3. 本地化话题标签 (拒绝纯英文，融入高热度马来文标签)
- **禁止**：仅堆砌纯英文 Hashtags（如仅放 #womensunderwear #seamlessunderwear）。
- **标准标签池（马来文 + 英文双轨驱动）**：
  - **核心品类（马来文）**：#seluardalamwanita、#seluardalamseamless、#seluardalamsejuk、#seluardalamtanpagarisan、#seluardalamlelaki（男裤）、#colitanpadawai（无钢圈文胸）
  - **痛点与场景（马来文）**：#selesasepanjanghari、#kaintakpanas、#takmelekit、#tiadagarisan、#kemasdanraya
  - **平台与大盘标签**：#shentaimalaysia、#tiktokshopmalaysia、#racuntiktok、#barangviral、#tiktokmademebuyit

### 4. 视频剪辑 Hook 升级 (砸落字/砸落画面震撼开场)
- **开场 0~1 秒**：采用**高冲击力的重力砸落字幕 (Drop/Slam Title Animation)** 或**实物重力砸落/弹跳回弹镜头**作为强力视觉 Hook，打破用户划走惯性。
- **字号放大**：手机端用户以拇指快速滑屏，字号必须放大至屏幕宽度的 40%~60%，选用高粗体（Bold 无衬线），黑底白字或高反差黄黑配色，确保不戴眼镜也能一眼辨识。

### 5. 语言口播与文案风格 (加入口语语气词，去公文化)
- **拒绝**：书面语过重、语法过分工整生硬的书面马来文（如过于严谨的报刊文体）。
- **必须融入本地马来人说话习惯**：
  - **口语语气词**：高频自然融入 wah、oh、ke、je、tau、wehh、laa（例："Wah lembut gila!", "RM49 je dapat 5 helai tau!", "Selesa sangat wehh"）；
  - **简化常用词汇**：使用口语缩略词（如 tak 代替 tidak，kat 代替 di/pada，ni 代替 ini，tu 代替 itu，nak 代替 mahu，dpt 代替 dapat）；
  - 热情、接地气、像闺蜜或本地好物推荐官一样的语气，显著拉长停留时长。

### 6. 主播与达人建联布局 (马来本土主播引流)
- 矩阵账号自营短视频负责基础产品功能演示与长尾放量；
- 对需要深度信任转化的重点大单品（2987高腰裤、8018口红裤、男士平角裤），持续配合寄样与建联**马来本土原生创作者/主播 (Malay Local Creators)** 进行真实上身实测与出镜解说，彻底打穿本土受众池。


### 创作者人员属性与考核适用边界
- **小袁、宁宁（非全职创作者）**：视频发布后**仅做常规客观数据登记**（播放、完播、时长、3s停留率、销售转化），不套用试用期达标率与预警惩处机制；
- **新入职全职内容创作者 (Full-time Content Creators)**：正式适用 3 个月试用期考核基线（M1 ≥ 40%，M2 ≥ 50%，M3 ≥ 55%~60%）及前 3 秒二剪改版联动 SOP。
