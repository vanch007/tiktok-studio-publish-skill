# Prompt Quality Profile

Skill: `tiktok-studio-publish`
Relevance: `prompt-aware`
Overall quality score: `91.0/100`

## Primary Task Family

**Execution operation**
- Matched keywords: checklist, 流程, 操作, 执行, 清单

## Complexity

- Band: `expert`
- Score: `9`
- Reason: multiple task families plus governance, evaluation, or expert-level constraints

## Need Model

- Explicit Need: Upload and schedule prepared vertical educational videos to a confirmed TikTok Studio account.
- Implicit Need: The reusable skill needs a stable role, task, and output contract rather than a one-off prompt.
- Scenario: Local MP4 files, an explicit posting order, caption/topic text, schedule slots, and optional music rotation.
- User Level: infer from examples and standards; ask only if it changes output depth
- Success Standard: Never claim success without a visible post-row or schedule confirmation.

## RTF To Skill Mapping

- Role: Use an operator role with explicit boundaries, inputs, outputs, and failure handling.
- Task: Convert the job into ordered steps with validation checks and stop conditions.
- Format: Return a runbook-like handoff with commands, checks, owners, and next actions when relevant.

## Quality Matrix

### Completeness — 95/100
- Matched signals: 输入, 输出
- Repair: Name missing inputs, outputs, constraints, or success standards before deepening the package.

### Clarity — 85/100
- Matched signals: 明确
- Repair: Replace broad verbs with observable actions and define what done means.

### Consistency — 95/100
- Matched signals: boundary, 一致, 边界
- Repair: Check that role, task, format, exclusions, and examples do not contradict each other.

### Practicality — 95/100
- Matched signals: use, 执行, 使用
- Repair: Add runnable steps, examples, or verification cues instead of abstract advice.

### Specificity — 85/100
- Matched signals: 用户
- Repair: Anchor wording in the user's audience, domain nouns, and target outcome.

## Matched Task Families

### Execution operation
- Score: `5`
- Keywords: checklist, 流程, 操作, 执行, 清单
- Role: Use an operator role with explicit boundaries, inputs, outputs, and failure handling.
- Task: Convert the job into ordered steps with validation checks and stop conditions.
- Format: Return a runbook-like handoff with commands, checks, owners, and next actions when relevant.

### Creative generation
- Score: `2`
- Keywords: 标题, 内容
- Role: Use a taste-aware creator role with clear audience, tone, and originality boundaries.
- Task: Generate variants, explain selection logic, and preserve the user's distinctive constraints.
- Format: Return options with rationale, selection criteria, and refinement paths.

### Analytical reasoning
- Score: `1`
- Keywords: 分析
- Role: Use an analyst role that separates evidence, inference, uncertainty, and recommendation.
- Task: State assumptions, compare alternatives, and make the decision path inspectable.
- Format: Return findings, evidence, tradeoffs, recommendation, and residual risks.

## Self-Repair Checks

- Check explicit need, implicit need, scenario, user level, and success standard before deepening.
- Map Role, Task, and Format into skill behavior, not decorative prompt labels.
- Ask one focused clarification only when missing information changes the package boundary.
- Add tests or examples for prompt-heavy behavior before treating it as reusable.
- Keep prompt methodology in references and reports instead of bloating SKILL.md.

## Reviewer Note

Use this profile when the package depends on prompt behavior, role design, output contracts, or conversation quality.
