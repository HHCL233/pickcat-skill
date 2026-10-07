---
name: pickcat-skill
description: 获取 Pickcat 社区（PickCat，cdsq.dao3.fun）的帖子信息：推荐内容列表、最新帖子列表、多页翻页浏览、指定帖子的完整详情与正文、帖子热门评论，并可登录账户（Cookie 持久化）、发布评论与帖子、查询评论与帖子的发布状态。当用户提到 pickcat / Pickcat / dao3.fun，或想查看、浏览、汇总、分析该社区的帖子、评论与动态，或想在该社区发帖、评论时使用本技能——即使用户没有明确说"用 Pickcat API"。
---

# Pickcat-Skill

获取 [Pickcat 社区](https://cdsq.dao3.fun)的帖子信息。API 为公开接口，浏览与读评论无需登录；发布评论、发布帖子需要先登录。

## 工具

使用本技能目录下的 `scripts/pickcat.py`（仅用 Python 标准库，无需安装任何依赖）。下文命令均省略前缀，实际执行时替换为 `python3 <技能目录>/scripts/pickcat.py`。

### 1. 推荐内容列表

```bash
pickcat.py recommended                  # 第 1 页，默认 20 条
pickcat.py recommended --limit 10       # 每页 10 条
pickcat.py recommended --cursor "..."   # 翻到下一页
pickcat.py recommended --pages 3        # 连续取 3 页
```

### 2. 最新内容列表

```bash
pickcat.py latest --limit 20
```

参数与 `recommended` 完全一致。

### 3. 指定帖子详情

```bash
pickcat.py topic 01a10a6c-4c14-7411-81a5-939f91730a4a
```

输出帖子标题、作者、标签、统计数据与正文纯文本（HTML 已转为文本，图片位置标注为 `[图片: <完整URL>]`，论坛表情保留为 `[emoji:xxx]`）。加 `--json` 可输出接口原始完整 JSON（含 `cookedHtml` 等全部字段）。

### 4. 帖子热门评论

```bash
pickcat.py replies 01a0ebdd-87c5-7c4d-a511-d5e0e08de1d8            # 第 1 页，默认 50 条
pickcat.py replies <帖子ID> --pages 2                              # 连续取 2 页
pickcat.py replies <帖子ID> --cursor "..."                         # 翻到下一页
```

按热度（`sort=hot`）返回评论，含楼层号（`postNumber`）、作者、点赞数、回复目标（`→ 回复 #N`）与正文纯文本。评论接口公开，未登录也可使用。

### 5. 登录 / 登出

```bash
pickcat.py login --username <账户名> --password <密码>   # 也可省略 --password 交互式输入
pickcat.py logout                                       # 清除已保存的登录信息
```

登录成功后，`pickcat_session` Cookie 自动保存到 `~/.config/.pickcatskill`（JSON，权限 600），之后脚本的所有请求都会自动携带该 Cookie；Cookie 过期或被服务端失效时（请求返回 HTTP 401），脚本会在 stderr 给出提示，重新 `login` 即可。

### 6. 发布评论与评论状态（需登录）

```bash
pickcat.py comment <帖子ID> --markdown "评论内容"        # 直接回复主帖
pickcat.py comment <帖子ID> --markdown "..." --reply-to 3 # 回复 #3 楼
echo "长内容" | pickcat.py comment <帖子ID> --markdown -  # 从 stdin 读取
pickcat.py comment-status <submissionId>                 # 查询发布状态
pickcat.py comment-status <submissionId> --wait 30       # 仍在处理中时自动轮询（间隔 2 秒）最多 30 秒
```

发布是异步的：`comment` 返回 `submissionId` 和初始状态（如 `PENDING_PROVIDER`），需用 `comment-status` 确认最终是否成功（成功时含 `postId` 与楼层号）。

### 7. 发布帖子与帖子状态（需登录）

```bash
pickcat.py post --title "帖子标题" --markdown "帖子正文（Markdown）"
echo "长正文" | pickcat.py post --title "标题" --markdown -  # 从 stdin 读取正文
pickcat.py post-status <postId>                 # 查询发布状态与详情
pickcat.py post-status <postId> --wait 60       # 仍在处理中时自动轮询（间隔 2 秒）最多 60 秒
```

`post` 固定以 `DISCUSSION` 类型、`创作与作品` 标签发布（接口限制，暂不能指定其他标签/类型）。发布是异步的：`post` 返回 `postId` 与初始状态（如 `PENDING_PROVIDER`），需用 `post-status` 确认最终是否发布成功（`PUBLISHED`，响应中含 `topicId`、发布时间与编辑额度）；成功后可用 `topic <topicId>` 查看公开页面详情。

**发布纪律（必须遵守）**：

- 发布评论、发布帖子都是**以用户账户对外公开的写操作**——只有当用户明确要求发布评论或帖子时才可运行 `comment` / `post`。
- 发布内容必须是用户提供或经用户明确确认的文本（标题与正文都算）；不要擅自改写、扩写后直接发布，不要为了测试而发布。
- 不得批量、重复或连续发布；一次任务只发布用户要求的内容。
- 发布后务必用 `comment-status` / `post-status` 确认结果，把最终状态与楼层号（评论）或 `topicId`（帖子）报告给用户。
- 若未登录，脚本会报错提示先 `login`，此时引导用户提供账户或自行登录，不要替用户编造凭证。

### 8. 通用参数

| 参数 | 说明 |
|---|---|
| `--limit N` | 每页条数，列表默认 20、评论默认 50，范围 1-50 |
| `--cursor <ID>` | 上一页返回的 `pageInfo.nextCursor` |
| `--pages N` | 连续抓取 N 页（自动接力 cursor），范围 1-20 |
| `--json` | 输出原始 JSON 而不是精简摘要 |

默认输出为精简摘要（省 token、便于阅读）；需要完整字段做二次处理时加 `--json`。

## 长期存储配置

所有需要跨会话长期保存的 Pickcat 配置（登录 Cookie、账户名、Token 到期时间等）**必须统一存放在 `~/.config/.pickcatskill`**，不要写到其他任何位置（不要放进项目目录、会话文件或代码里）。脚本的 `login`/`logout` 已自动读写该文件，文件格式：

```json
{
  "pickcat_session": "<登录Token>",
  "username": "<账户名>",
  "expiresAt": "<Token到期时间，ISO 8601>",
  "savedAt": "<保存时间>",
  "recommendationsCookie": "<推荐流会话Cookie，脚本自动读写维护>"
}
```

注意事项：

- 该文件包含凭证，脚本以 0600 权限保存；不要在回复中明文展示完整的 Cookie 或密码。
- 如果需要自行扩展保存其他长期配置，读入现有 JSON、合并新键后写回（保持 0600 权限），不要覆盖掉 `pickcat_session` 等已有键。
- Cookie 由登录接口的 `Set-Cookie` 响应头下发（键名 `pickcat_session`），有效期见 `expiresAt`，过期后重新 `login`。
- 推荐流（`recommended`）翻页依赖站点下发的 `pickcat_recommendations` Cookie（游标与浏览会话绑定）：脚本会自动捕获并保存到 `recommendationsCookie` 键、翻页时自动携带，因此 `--pages` 和跨进程 `--cursor` 都可用；若服务端会话状态失效，脚本会提示重新获取第一页。

## 典型流程

1. 用户想看"最新/推荐帖子"→ 跑 `latest` 或 `recommended`，把摘要整理后回复。
2. 用户想读某帖全文 → 先从列表拿到帖子 `ID`，再跑 `topic <ID>`。
3. 用户想看某帖的评论 → 跑 `replies <帖子ID>`。
4. 用户想浏览更多 → 按返回提示追加 `--cursor <nextCursor>` 翻页。
5. 用户要求登录操作（或提供账户密码）→ 跑 `login`，凭证只用于该命令，之后不再复述。
6. 用户要求发布评论 → 与用户确认内容后跑 `comment`，再跑 `comment-status`（可加 `--wait`）确认发布成功并报告楼层号。
7. 用户要求发布帖子 → 与用户确认标题与正文后跑 `post`，再跑 `post-status`（可加 `--wait`）确认发布成功并报告 `topicId`。

列表里的 `excerpt` 只是内容预览（已截断），不要把它当成帖子全文；全文必须用 `topic` 获取。

## 分页方式

列表和评论接口都返回 `pageInfo`：`hasNextPage` 表示是否还有下一页，`nextCursor` 是下一页游标，把它作为 `--cursor` 传入即可。`--pages N` 会自动完成接力。推荐流翻页所需的会话 Cookie 由脚本自动管理（见"长期存储配置"），无需手动处理。

## 返回字段速查

列表项核心字段：`id`（帖子 ID）、`title`（标题）、`kind`（帖子类型，如 `ANNOUNCEMENT`/`DISCUSSION`）、`excerpt`（内容预览）、`author.username`（作者）、`tags[].name`（标签中文名）、`replyCount`/`viewCount`/`likeCount`/`bookmarkCount`（回复/查看/点赞/收藏数）、`createdAt`/`lastActivityAt`（ISO 8601 时间）、`pinned`/`pinnedGlobally`（置顶状态）。

帖子详情核心字段：`firstPost.cookedHtml`（正文 HTML）、`collection`（所属合集）、`repliesTruncated`（回复是否未包含在返回中）、`author.displayedBadge`（作者佩戴称号）。

评论项核心字段：`postNumber`（楼层号）、`replyToPostNumber`（回复目标楼层，为 1 表示直接回复主帖）、`likeCount`（点赞数）、`cookedHtml`（评论 HTML）、`deleted`（是否已删除）、`pinned`（是否置顶）、`author.username`（评论者）。

登录响应核心字段：`user.username`（用户名）、`user.level.current`（等级）、`expiresAt`（Token 到期时间）。

发布评论响应核心字段：`submissionId`（状态查询 ID）、`postId`（评论 ID）、`status`（当前状态，如 `PENDING_PROVIDER`）。

评论状态响应核心字段：`status`（发布状态）、`postNumber`（发布成功后的楼层号）、`postId`（评论 ID）、`request.markdown`（提交的内容）、`riskLevel`（评论风险等级）。

发布帖子响应核心字段：`submissionId`（提交 ID）、`postId`（查询发布状态用的 ID）、`topicId`（主题 ID，发布成功后可用 `topic` 查看）、`status`（当前状态，如 `PENDING_PROVIDER`）。

帖子发布状态响应核心字段：`latestSubmissionStatus`（发布状态，`PUBLISHED` 表示已发布）、`postId`/`topicId`、`request.title`/`request.markdown`（提交的标题与正文）、`publishedAt`（发布时间）、`canEdit`/`editAttemptsUsed`/`editAttemptsRemaining`（编辑额度）、`editBlockedReason`（编辑被阻止原因）。

需要确认某个字段的确切含义时，再读完整 API 文档：[references/api.md](references/api.md)。

## 注意事项

- 所有 `avatar`、图片、文件的 `url` 都是相对路径，需拼接 base URL 使用：`https://cdsq.dao3.fun` + 路径。
- 除 `comment` / `post`（须遵守"发布纪律"）外，其余功能均为只读获取；请勿对站点发起高频或并发请求，请求失败（如 HTTP 403/429）时稍后重试，不要暴力重试。`comment-status` / `post-status` 的 `--wait` 已内置 2 秒轮询间隔，不要额外加密轮询。
- 如需绕过脚本自行写代码，同样只使用 Python 标准库（`urllib.request`、`json`、`argparse` 等），不引入任何第三方库。
