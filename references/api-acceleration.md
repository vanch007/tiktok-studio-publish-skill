# API 加速边界

## 目的

可选使用 `tiktok-agent-publisher` 作为 TikTok 官方 Content Posting API 的传输层，把多个本地 MP4 先送到 TikTok 处理，减少逐个打开系统文件选择器和等待上传的时间。它不是 TikTok Studio 的替代品。

## 路由

| 场景 | 传输层 | 原因 |
|---|---|---|
| 需要预约、平台热门音乐、音乐混音 | API `MEDIA_UPLOAD` 预上传 → Studio | API 上传接口不提供 Studio 的音乐/音量/预约控件；最终作品仍需页面核验 |
| 立即发布、已有 API OAuth 和审核通过的客户端 | API `DIRECT_POST`（仅用户明确选择） | 可直接设置标题/话题并轮询状态，但不是预约 |
| 没有 API 凭据、URL 前缀未验证或 API 不稳定 | Studio | 不安装依赖、不把令牌写进日志，保持现有可靠兜底 |

## API 预上传合同

1. 只在外部技能已安装且 `tiktok_connection_status`、`tiktok_privacy_audit` 通过后使用。
2. 先记录本地文件、文件大小、批次 ID；调用 `tiktok_publish_video` 时显式使用 `post_mode=MEDIA_UPLOAD`。
3. API 上传接口只负责把媒体放入 TikTok Inbox；标题/说明、热门音乐、音量和预约时间在 Studio 完成。
4. 每个用户的初始化请求遵守 TikTok 6 次/分钟限制；默认最多两个媒体上传并发，失败时单任务重试一次后回退 Studio。
5. 保存 `api_publish_id` 和 `tiktok_publish_status` 的结果；只有作品页出现对应标题/预约时间时才写 `verification_status=pass`。

## 不允许的误用

- 不把 API `DIRECT_POST` 当成预约发布。
- 不声称 API 能选择 TikTok 热门音乐或把音乐压到 5% / `-40 dB`。
- 不把 dry-run 的 `dryrun_*` ID 当真实作品 ID。
- 不为提速绕过用户确认、OAuth、TikTok 审核或账号/窗口核验。
