# 说明与发布审计字段

说明应面向越南学习者，包含课程/课次、简短越南语提示和相关话题。不要在封面说明中泄露答题选项或翻译答案。

建议每条记录使用以下字段：

```json
{
  "filename": "HSK2_Bai26_Part03_MicroV3.mp4",
  "caption": "Bài 26 · Từ vựng HSK2",
  "hashtags": ["#họctiếngtrung", "#HSK2", "#từvựngtiếngTrung"],
  "music_track": "Future",
  "music_db": -40,
  "schedule_at": "2026-08-07T13:30:00+08:00",
  "post_url_or_id": null,
  "verification_status": "pending",
  "evidence": "作品行截图或可读取的作品行文本",
  "notes": []
}
```

说明提交失败时保留原始字段、界面显示值和作品行显示值，标记 `caption_persistence_failed`；不要用“看起来正确”替代作品行证据。若作品行出现文件名、随机前缀（如 `xSK2_...`）或乱码，也按失败处理。

预约作品的标题/说明通常不可编辑；如果作品行在预约后不匹配，记录 `scheduled_caption_immutable`，只进入取消/删除并重传的用户确认流程。

追加字段：

```json
{
  "caption_requested": "Bài 26 · Từ vựng HSK2",
  "caption_displayed": "xSK2_Bai26_Part03_MicroV3",
  "caption_input_mode": "keyboard|ascii_fallback|set_value_only",
  "caption_persistence": "pass|caption_persistence_failed|pending"
}
```
