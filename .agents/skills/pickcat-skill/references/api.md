# PickcatAPI

## 获取推荐内容第1页

```text
GET https://cdsq.dao3.fun/api/v1/topic-recommendations?sort=recommended&limit=20
```

响应表头:

| 键         | 意思                        |
| ---------- | --------------------------- |
| set-cookie | Cookie,用于获取下一页时使用 |

返回内容示例:

```json
{
  "strategy": "PERSONALIZED",
  "items": [
    {
      "id": "01a0eb91-5d11-7fb0-b998-179add93620f", //帖子ID
      "title": "【共琢一轮月】PickCat 中秋创作分享活动第一阶段获奖名单公示", //帖子标题
      "kind": "ANNOUNCEMENT", //帖子类型
      "excerpt": "Hello，各位训练师们！ 伴随着中秋假期的欢声笑语，我们的 【共琢一轮月】pickCat中秋创作分享活动 也行至中途啦！ 在《酉阳杂俎》的典故里，月亮由无数人共同修治。在活动的前期阶段，我们看到了各位训练师在新社区里齐心“修月”的热情——无论是硬核的代码漏洞反馈、自制编程语言与 UI，还是惊艳的光栅化文本印刷方案、3D 与技术教程，每一份作品都让人眼前一亮，也让新社区变得无比热闹！ 经过认真的评", //帖子内容预览
      "author": {
        "id": "03829981-0c9c-458d-a2df-1f30b78bc35a", //发帖人ID
        "username": "hajimes", //发帖人用户名
        "avatar": {
          "type": "PRESET", //发帖人头像类型
          "id": 5, //发帖人头像ID
          "url": "/api/v1/avatars/5?v=1f18ac5ef64a88ff5e8e6758dfbc121123b6c13e408b28dccbd4fc7982797948" //发帖人头像链接(baseurl:https://cdsq.dao3.fun/)
        }
      },
      "tags": [
        {
          "id": "01a0ab26-84a8-718b-996a-42a29388f3fa", //该标签ID
          "slug": "events-competitions", //该标签类型
          "name": "活动与赛事" //该标签中文名
        }
      ], //帖子标签
      "replyCount": 26, //帖子回复数
      "viewCount": 140, //帖子查看数
      "likeCount": 5, //帖子点赞数
      "bookmarkCount": 1, //帖子收藏数
      "closedAt": null, //帖子关闭时间
      "pinned": true, //帖子是否置顶
      "pinnedGlobally": true, //帖子是否置顶
      "pinnedTagId": null, //帖子是否全局置顶
      "pinnedAt": "2026-09-29T08:33:47.233Z", //帖子置顶时间
      "pinnedUntil": null, //帖子置顶截止时间
      "createdAt": "2026-09-29T05:09:27.428Z", //帖子创建时间
      "editedAt": "2026-09-29T09:59:19.985Z", //帖子最新编辑时间
      "lastActivityAt": "2026-10-04T11:31:14.419Z", //帖子最后活动时间
      "reason": "PINNED" //帖子类型
    }
  ],
  "pageInfo": {
    "hasNextPage": true, //是否还有下一页
    "nextCursor": "01a10b69-ffa0-71b4-a46a-8ad4b394f377.19.brvr6lpa5_69zneLkRz5yxLLcaUE_nVD3TugurijlWE" //下一页ID
  }
}
```

## 获取推荐内容第n页

```text
GET https://cdsq.dao3.fun/api/v1/topic-recommendations?sort=recommended&limit=20&cursor={ID}
```

查询参数:

- `ID`: 从上一页中的pageInfo.nextCursor获取

返回内容示例:

```json
{
  "strategy": "PERSONALIZED",
  "items": [
    {
      "id": "01a0eb91-5d11-7fb0-b998-179add93620f", //帖子ID
      "title": "【共琢一轮月】PickCat 中秋创作分享活动第一阶段获奖名单公示", //帖子标题
      "kind": "ANNOUNCEMENT", //帖子类型
      "excerpt": "Hello，各位训练师们！ 伴随着中秋假期的欢声笑语，我们的 【共琢一轮月】pickCat中秋创作分享活动 也行至中途啦！ 在《酉阳杂俎》的典故里，月亮由无数人共同修治。在活动的前期阶段，我们看到了各位训练师在新社区里齐心“修月”的热情——无论是硬核的代码漏洞反馈、自制编程语言与 UI，还是惊艳的光栅化文本印刷方案、3D 与技术教程，每一份作品都让人眼前一亮，也让新社区变得无比热闹！ 经过认真的评", //帖子内容预览
      "author": {
        "id": "03829981-0c9c-458d-a2df-1f30b78bc35a", //发帖人ID
        "username": "hajimes", //发帖人用户名
        "avatar": {
          "type": "PRESET", //发帖人头像类型
          "id": 5, //发帖人头像ID
          "url": "/api/v1/avatars/5?v=1f18ac5ef64a88ff5e8e6758dfbc121123b6c13e408b28dccbd4fc7982797948" //发帖人头像链接(baseurl:https://cdsq.dao3.fun/)
        }
      },
      "tags": [
        {
          "id": "01a0ab26-84a8-718b-996a-42a29388f3fa", //该标签ID
          "slug": "events-competitions", //该标签类型
          "name": "活动与赛事" //该标签中文名
        }
      ], //帖子标签
      "replyCount": 26, //帖子回复数
      "viewCount": 140, //帖子查看数
      "likeCount": 5, //帖子点赞数
      "bookmarkCount": 1, //帖子收藏数
      "closedAt": null, //帖子关闭时间
      "pinned": true, //帖子是否置顶
      "pinnedGlobally": true, //帖子是否置顶
      "pinnedTagId": null, //帖子是否全局置顶
      "pinnedAt": "2026-09-29T08:33:47.233Z", //帖子置顶时间
      "pinnedUntil": null, //帖子置顶截止时间
      "createdAt": "2026-09-29T05:09:27.428Z", //帖子创建时间
      "editedAt": "2026-09-29T09:59:19.985Z", //帖子最新编辑时间
      "lastActivityAt": "2026-10-04T11:31:14.419Z", //帖子最后活动时间
      "reason": "PINNED" //帖子类型
    }
  ],
  "pageInfo": {
    "hasNextPage": true, //是否还有下一页
    "nextCursor": "01a10b69-ffa0-71b4-a46a-8ad4b394f377.19.brvr6lpa5_69zneLkRz5yxLLcaUE_nVD3TugurijlWE" //下一页ID
  }
}
```

## 获取最新内容第1页

```text
GET https://cdsq.dao3.fun/api/v1/topic-recommendations?sort=latest&limit=20
```

响应表头:

| 键         | 意思                        |
| ---------- | --------------------------- |
| set-cookie | Cookie,用于获取下一页时使用 |

返回内容示例:

```json
{
  "strategy": "LATEST",
  "items": [
    {
      "id": "01a0eb91-5d11-7fb0-b998-179add93620f", //帖子ID
      "title": "【共琢一轮月】PickCat 中秋创作分享活动第一阶段获奖名单公示", //帖子标题
      "kind": "ANNOUNCEMENT", //帖子类型
      "excerpt": "Hello，各位训练师们！ 伴随着中秋假期的欢声笑语，我们的 【共琢一轮月】pickCat中秋创作分享活动 也行至中途啦！ 在《酉阳杂俎》的典故里，月亮由无数人共同修治。在活动的前期阶段，我们看到了各位训练师在新社区里齐心“修月”的热情——无论是硬核的代码漏洞反馈、自制编程语言与 UI，还是惊艳的光栅化文本印刷方案、3D 与技术教程，每一份作品都让人眼前一亮，也让新社区变得无比热闹！ 经过认真的评", //帖子内容预览
      "author": {
        "id": "03829981-0c9c-458d-a2df-1f30b78bc35a", //发帖人ID
        "username": "hajimes", //发帖人用户名
        "avatar": {
          "type": "PRESET", //发帖人头像类型
          "id": 5, //发帖人头像ID
          "url": "/api/v1/avatars/5?v=1f18ac5ef64a88ff5e8e6758dfbc121123b6c13e408b28dccbd4fc7982797948" //发帖人头像链接(baseurl:https://cdsq.dao3.fun/)
        }
      },
      "tags": [
        {
          "id": "01a0ab26-84a8-718b-996a-42a29388f3fa", //该标签ID
          "slug": "events-competitions", //该标签类型
          "name": "活动与赛事" //该标签中文名
        }
      ], //帖子标签
      "replyCount": 26, //帖子回复数
      "viewCount": 140, //帖子查看数
      "likeCount": 5, //帖子点赞数
      "bookmarkCount": 1, //帖子收藏数
      "closedAt": null, //帖子关闭时间
      "pinned": true, //帖子是否置顶
      "pinnedGlobally": true, //帖子是否置顶
      "pinnedTagId": null, //帖子是否全局置顶
      "pinnedAt": "2026-09-29T08:33:47.233Z", //帖子置顶时间
      "pinnedUntil": null, //帖子置顶截止时间
      "createdAt": "2026-09-29T05:09:27.428Z", //帖子创建时间
      "editedAt": "2026-09-29T09:59:19.985Z", //帖子最新编辑时间
      "lastActivityAt": "2026-10-04T11:31:14.419Z", //帖子最后活动时间
      "reason": "PINNED" //帖子类型
    }
  ],
  "pageInfo": {
    "hasNextPage": true, //是否还有下一页
    "nextCursor": "01a10b69-ffa0-71b4-a46a-8ad4b394f377.19.brvr6lpa5_69zneLkRz5yxLLcaUE_nVD3TugurijlWE" //下一页ID
  }
}
```

## 获取最新内容第n页

```text
GET https://cdsq.dao3.fun/api/v1/topic-recommendations?sort=latest&limit=20&cursor={ID}
```

查询参数:

- `ID`: 从上一页中的pageInfo.nextCursor获取

返回内容示例:

```json
{
  "strategy": "LATEST",
  "items": [
    {
      "id": "01a0eb91-5d11-7fb0-b998-179add93620f", //帖子ID
      "title": "【共琢一轮月】PickCat 中秋创作分享活动第一阶段获奖名单公示", //帖子标题
      "kind": "ANNOUNCEMENT", //帖子类型
      "excerpt": "Hello，各位训练师们！ 伴随着中秋假期的欢声笑语，我们的 【共琢一轮月】pickCat中秋创作分享活动 也行至中途啦！ 在《酉阳杂俎》的典故里，月亮由无数人共同修治。在活动的前期阶段，我们看到了各位训练师在新社区里齐心“修月”的热情——无论是硬核的代码漏洞反馈、自制编程语言与 UI，还是惊艳的光栅化文本印刷方案、3D 与技术教程，每一份作品都让人眼前一亮，也让新社区变得无比热闹！ 经过认真的评", //帖子内容预览
      "author": {
        "id": "03829981-0c9c-458d-a2df-1f30b78bc35a", //发帖人ID
        "username": "hajimes", //发帖人用户名
        "avatar": {
          "type": "PRESET", //发帖人头像类型
          "id": 5, //发帖人头像ID
          "url": "/api/v1/avatars/5?v=1f18ac5ef64a88ff5e8e6758dfbc121123b6c13e408b28dccbd4fc7982797948" //发帖人头像链接(baseurl:https://cdsq.dao3.fun/)
        }
      },
      "tags": [
        {
          "id": "01a0ab26-84a8-718b-996a-42a29388f3fa", //该标签ID
          "slug": "events-competitions", //该标签类型
          "name": "活动与赛事" //该标签中文名
        }
      ], //帖子标签
      "replyCount": 26, //帖子回复数
      "viewCount": 140, //帖子查看数
      "likeCount": 5, //帖子点赞数
      "bookmarkCount": 1, //帖子收藏数
      "closedAt": null, //帖子关闭时间
      "pinned": true, //帖子是否置顶
      "pinnedGlobally": true, //帖子是否置顶
      "pinnedTagId": null, //帖子是否全局置顶
      "pinnedAt": "2026-09-29T08:33:47.233Z", //帖子置顶时间
      "pinnedUntil": null, //帖子置顶截止时间
      "createdAt": "2026-09-29T05:09:27.428Z", //帖子创建时间
      "editedAt": "2026-09-29T09:59:19.985Z", //帖子最新编辑时间
      "lastActivityAt": "2026-10-04T11:31:14.419Z", //帖子最后活动时间
      "reason": "PINNED" //帖子类型
    }
  ],
  "pageInfo": {
    "hasNextPage": true, //是否还有下一页
    "nextCursor": "01a10b69-ffa0-71b4-a46a-8ad4b394f377.19.brvr6lpa5_69zneLkRz5yxLLcaUE_nVD3TugurijlWE" //下一页ID
  }
}
```

## 获取指定帖子内容

```text
GET https://cdsq.dao3.fun/api/v1/topics/{ID}
```

查询参数:

- `ID`: 帖子ID

返回内容示例:

```json
{
  "collection": {
    "id": "01a0e0bd-372f-7f15-af0c-52a18a21ef07", //帖子对应合集ID
    "name": "作品投稿" //帖子对应合集名称
  },
  "id": "01a10a6c-4c14-7411-81a5-939f91730a4a", //帖子ID
  "title": "新作预告？", //帖子标题
  "kind": "DISCUSSION", //帖子类型
  "author": {
    "id": "01a0c996-8ade-7d43-8314-9ebf4031922f", //帖子作者ID
    "username": "bluudude", //发帖人名称
    "avatar": {
      "type": "CUSTOM", //发帖人头像类型
      "id": "01a10208-9747-76b7-8524-f415ea4ec917", //发帖人头像ID
      "url": "/api/v1/avatars/01a10208-9747-76b7-8524-f415ea4ec917" //发帖人头像链接(baseurl:https://cdsq.dao3.fun/)
    },
    "displayedBadge": {
      "id": "badge_pioneer", //发帖人佩戴称号ID
      "name": "开拓者", //发帖人佩戴称号名
      "description": "参与Pickcat社区第一次内测", //发帖人佩戴称号详情
      "image": {
        "fileId": "01a0b34f-c685-7777-b60d-fe2a6adb6f52", //发帖人佩戴称号图片文件ID
        "url": "/api/v1/files/01a0b34f-c685-7777-b60d-fe2a6adb6f52", //发帖人佩戴称号图片链接(baseurl:https://cdsq.dao3.fun/)
        "width": 512, //发帖人佩戴称号图片宽
        "height": 512 //发帖人佩戴称号图片高
      }
    }
  },
  "tags": [
    {
      "id": "01a0ab26-84a8-718b-996a-36be3dda4fa4", //该标签类型ID
      "slug": "creative-works", //该标签类型
      "name": "创作与作品" //该标签名称
    },
    {
      "id": "01a0ab26-84a8-718b-996a-4536506db3ba", //该标签类型ID
      "slug": "interest-plaza", //该标签类型
      "name": "兴趣广场" //该标签名称
    }
  ],
  "replyCount": 1, //帖子回复数
  "viewCount": 4, //帖子观看数
  "closedAt": null, //帖子关闭时间
  "closedBy": null, //帖子关闭原因
  "pinned": false, //帖子是否置顶
  "pinnedGlobally": false, //帖子是否全局置顶
  "pinnedTagId": null, //帖子置顶标签ID
  "pinnedAt": null, //帖子置顶时间
  "pinnedUntil": null, //帖子置顶截止时间
  "lastActivityAt": "2026-10-05T05:12:14.816Z", //帖子最后活动时间
  "createdAt": "2026-10-05T04:57:11.947Z", //帖子创建时间
  "editedAt": null, //帖子最后编辑时间
  "updatedAt": "2026-10-05T05:12:14.816Z", //帖子最后更新时间
  "firstPost": {
    "id": "01a10a6c-4c16-7b63-b8b5-87ba7956ba60",
    "topicId": "01a10a6c-4c14-7411-81a5-939f91730a4a", //帖子ID
    "postNumber": 1, //帖子序号
    "replyToPostNumber": null, //帖子
    "deleted": false, //帖子是否被删除
    "children": [], //帖子内子帖子
    "currentRevision": 1, //帖子版本
    "likeCount": 1, //帖子点赞数
    "pinned": false, //帖子是否置顶
    "cookedHtml": "<p><img src=\"/api/v1/files/01a10a6c-47c0-7648-8dd1-91b2f3cd3833\" alt=\"\" decoding=\"async\" />\n这只是一个过渡作</p>\n", //帖子内容
    "author": {
      "id": "01a0c996-8ade-7d43-8314-9ebf4031922f", //帖子作者ID
      "username": "bluudude", //发帖人名称
      "avatar": {
        "type": "CUSTOM", //发帖人头像类型
        "id": "01a10208-9747-76b7-8524-f415ea4ec917", //发帖人头像ID
        "url": "/api/v1/avatars/01a10208-9747-76b7-8524-f415ea4ec917" //发帖人头像链接(baseurl:https://cdsq.dao3.fun/)
      },
      "displayedBadge": {
        "id": "badge_pioneer", //发帖人佩戴称号ID
        "name": "开拓者", //发帖人佩戴称号名
        "description": "参与Pickcat社区第一次内测", //发帖人佩戴称号详情
        "image": {
          "fileId": "01a0b34f-c685-7777-b60d-fe2a6adb6f52", //发帖人佩戴称号图片文件ID
          "url": "/api/v1/files/01a0b34f-c685-7777-b60d-fe2a6adb6f52", //发帖人佩戴称号图片链接(baseurl:https://cdsq.dao3.fun/)
          "width": 512, //发帖人佩戴称号图片宽
          "height": 512 //发帖人佩戴称号图片高
        }
      }
    },
    "createdAt": "2026-10-05T04:57:11.947Z", //帖子创建时间
    "editedAt": null, //帖子最后编辑时间
    "viewerCapabilities": {
      "canPin": false, //访问用户是否可以置顶
      "canEdit": false, //访问用户是否可以编辑
      "canDelete": false, //访问用户是否可以删除
      "canLike": true, //访问用户是否可以点赞
      "canBookmark": true, //访问用户是否可以收藏
      "canReport": true, //访问用户是否可以举报
      "canSelectAnswer": false //访问用户是否可以选择答案
    },
    "viewerState": {
      "liked": false, //访问用户是否点赞
      "bookmarkId": null, //访问用户收藏ID
      "selectedAnswer": false //访问用户是否选择答案
    }
  },
  "repliesTruncated": true, //返回是否包含回复
  "events": [], //帖子参加的活动
  "eventsTruncated": false, //返回是否包含活动
  "viewerCapabilities": {
    "canEdit": false, //访问用户是否可以编辑
    "canReply": true, //访问用户是否可以回复
    "canDelete": false, //访问用户是否可以删除
    "canBookmark": true, //访问用户是否可以收藏
    "canClose": false, //访问用户是否可以关闭
    "canReopen": false, //访问用户是否可以打开已关闭的帖子
    "canUnselectAnswer": false, //访问用户是否可以取消选中答案
    "canClearDuplicate": false, //访问用户是否可以取消已被选中的回复
    "canMarkDuplicate": false, //访问用户是否可以标记为重复
    "pinnableTagIds": [], //访问用户可置顶标签的ID
    "canPinGlobally": false, //访问用户是否可以设置全局置顶
    "canUnpin": false //访问用户是否可以取消置顶
  },
  "viewerState": {
    "bookmarkId": null //访问用户收藏ID
  }
}
```

## 登录账户

```text
POST https://cdsq.dao3.fun/api/v1/session
```

请求负载:

| 键       | 意思   |
| -------- | ------ |
| password | 密码   |
| username | 账户名 |

响应标头:

| 键         | 意思   |
| ---------- | ------ |
| set-cookie | Cookie |

Cookie:

| 键              | 意思      |
| --------------- | --------- |
| pickcat_session | 登录Token |

返回内容示例:

```json
{
  "user": {
    "id": "e3e94d88-0a25-46f0-8a2a-4935f545f9e4", //用户ID
    "username": "hhcl233", //用户名
    "createdAt": "2026-09-12T22:11:30.295Z", //用户创建时间
    "avatar": {
      "type": "CUSTOM", //头像类型
      "id": "01a0e68f-5923-73ea-bf38-4256cc49cb40", //头像ID
      "url": "/api/v1/avatars/01a0e68f-5923-73ea-bf38-4256cc49cb40" //头像链接(baseurl:https://cdsq.dao3.fun/)
    },
    "level": {
      "current": 1 //用户当前等级
    },
    "effectivePermissions": [] //用户权限
  },
  "createdAt": "2026-10-06T06:27:48.231Z", //登录时间
  "expiresAt": "2026-10-13T06:27:48.231Z", //Token到期时间
  "silence": null //未知
}
```

## 获取帖子热门评论第1页

```text
GET https://cdsq.dao3.fun/api/v1/topics/{ID}/posts?limit=50&sort=hot
```

响应表头:

| 键         | 意思                        |
| ---------- | --------------------------- |
| set-cookie | Cookie,用于获取下一页时使用 |

查询参数:

- `ID`: 帖子ID

返回内容示例:

```json
{
  "items": [
    {
      "id": "01a0ebf0-c78d-7b06-9b23-8a71ae634d20", //评论ID
      "topicId": "01a0ebdd-87c5-7c4d-a511-d5e0e08de1d8", //帖子ID
      "postNumber": 3, //评论序号
      "replyToPostNumber": 1, //回复评论(若非回复则为1,否则为回复评论的序号)
      "deleted": false, //评论是否删除
      "children": [], //未知
      "currentRevision": 1, //评论版本
      "likeCount": 6, //评论点赞数
      "pinned": false, //评论是否置顶
      "cookedHtml": "<p>谢谢，我相信3D代码岛（神奇代码岛）会永远存在我们心中<img src=\"/api/v1/emojis/gif_expression_bianchenmao_call/image\" alt=\"[emoji:gif_expression_bianchenmao_call]\" class=\"markdown-emoji\" decoding=\"async\" /><img src=\"/api/v1/emojis/gif_expression_bianchenmao_great/image\" alt=\"[emoji:gif_expression_bianchenmao_great]\" class=\"markdown-emoji\" decoding=\"async\" /></p>\n", //评论内容
      "author": {
        "id": "03829981-0c9c-458d-a2df-1f30b78bc35a", //评论者ID
        "username": "hajimes", //评论者用户名
        "avatar": {
          "type": "PRESET", //评论者头像类型
          "id": 5, //评论者头像ID
          "url": "/api/v1/avatars/5?v=1f18ac5ef64a88ff5e8e6758dfbc121123b6c13e408b28dccbd4fc7982797948" //评论者头像链接(baseurl:https://cdsq.dao3.fun/)
        }，
        "displayedBadge": null //评论者称号
      },
      "createdAt": "2026-09-29T06:53:40.604Z", //评论时间
      "editedAt": null, //编辑时间
      "viewerCapabilities": {
      "canPin": false, //访问用户是否可以置顶
      "canEdit": false, //访问用户是否可以编辑
      "canDelete": false, //访问用户是否可以删除
      "canLike": true, //访问用户是否可以点赞
      "canBookmark": true, //访问用户是否可以收藏
      "canReport": true, //访问用户是否可以举报
      "canSelectAnswer": false //访问用户是否可以选择答案
    },
      "viewerState": {
        "liked": false, //访问用户是否点赞
        "bookmarkId": null, //访问用户收藏ID
        "selectedAnswer": false //访问用户是否选择答案
      }
    }
  ],
  "pageInfo": {
    "hasNextPage": true, //是否还有下一页
    "nextCursor": "01a10b69-ffa0-71b4-a46a-8ad4b394f377.19.brvr6lpa5_69zneLkRz5yxLLcaUE_nVD3TugurijlWE" //下一页ID
  }
}
```

## 获取帖子热门评论第n页

```text
GET https://cdsq.dao3.fun/api/v1/topics/{ID}/posts?limit=50&sort=hot&cursor={cursorID}
```

查询参数:

- `ID`: 帖子ID
- `cursorID`: 从上一页中的pageInfo.nextCursor获取

返回内容示例:

```json
{
  "items": [
    {
      "id": "01a0ebf0-c78d-7b06-9b23-8a71ae634d20", //评论ID
      "topicId": "01a0ebdd-87c5-7c4d-a511-d5e0e08de1d8", //帖子ID
      "postNumber": 3, //评论序号
      "replyToPostNumber": 1, //回复评论(若非回复则为1,否则为回复评论的序号)
      "deleted": false, //评论是否删除
      "children": [], //未知
      "currentRevision": 1, //评论版本
      "likeCount": 6, //评论点赞数
      "pinned": false, //评论是否置顶
      "cookedHtml": "<p>谢谢，我相信3D代码岛（神奇代码岛）会永远存在我们心中<img src=\"/api/v1/emojis/gif_expression_bianchenmao_call/image\" alt=\"[emoji:gif_expression_bianchenmao_call]\" class=\"markdown-emoji\" decoding=\"async\" /><img src=\"/api/v1/emojis/gif_expression_bianchenmao_great/image\" alt=\"[emoji:gif_expression_bianchenmao_great]\" class=\"markdown-emoji\" decoding=\"async\" /></p>\n", //评论内容
      "author": {
        "id": "03829981-0c9c-458d-a2df-1f30b78bc35a", //评论者ID
        "username": "hajimes", //评论者用户名
        "avatar": {
          "type": "PRESET", //评论者头像类型
          "id": 5, //评论者头像ID
          "url": "/api/v1/avatars/5?v=1f18ac5ef64a88ff5e8e6758dfbc121123b6c13e408b28dccbd4fc7982797948" //评论者头像链接(baseurl:https://cdsq.dao3.fun/)
        }，
        "displayedBadge": null //评论者称号
      },
      "createdAt": "2026-09-29T06:53:40.604Z", //评论时间
      "editedAt": null, //编辑时间
      "viewerCapabilities": {
      "canPin": false, //访问用户是否可以置顶
      "canEdit": false, //访问用户是否可以编辑
      "canDelete": false, //访问用户是否可以删除
      "canLike": true, //访问用户是否可以点赞
      "canBookmark": true, //访问用户是否可以收藏
      "canReport": true, //访问用户是否可以举报
      "canSelectAnswer": false //访问用户是否可以选择答案
    },
      "viewerState": {
        "liked": false, //访问用户是否点赞
        "bookmarkId": null, //访问用户收藏ID
        "selectedAnswer": false //访问用户是否选择答案
      }
    }
  ],
  "pageInfo": {
    "hasNextPage": true, //是否还有下一页
    "nextCursor": "01a10b69-ffa0-71b4-a46a-8ad4b394f377.19.brvr6lpa5_69zneLkRz5yxLLcaUE_nVD3TugurijlWE" //下一页ID
  }
}
```

## 发布评论

```text
POST https://cdsq.dao3.fun/api/v1/posts
```

请求标头:

| 键     | 意思                    |
| ------ | ----------------------- |
| cookie | Cookie(需包含登录Token) |

请求负荷:

| 键                | 意思                                         |
| ----------------- | -------------------------------------------- |
| markdown          | Markdown格式评论内容                         |
| replyToPostNumber | 回复评论(若非回复则为1,否则为回复评论的序号) |
| topicId           | 评论对应帖子ID                               |

响应表头:

| 键         | 意思                      |
| ---------- | ------------------------- |
| set-cookie | Cookie,用于获取状态时使用 |

返回内容示例:

```json
{
  "submissionId": "01a1102a-ce8f-72ce-8346-f7b709f1b3ea", //获取状态ID
  "topicId": "01a0eb91-5d11-7fb0-b998-179add93620f", //帖子ID
  "postId": "01a1102a-ce91-7e65-85d7-a76573232021", //评论ID
  "status": "PENDING_PROVIDER" //评论当前状态
}
```

## 获取评论状态

```text
GET https://cdsq.dao3.fun/api/v1/post-submissions/{ID}
```

查询参数:

- `ID`: 帖子ID
- `cursorID`: 从发布评论的submissionId获取

请求标头:

| 键     | 意思                    |
| ------ | ----------------------- |
| cookie | Cookie(需包含登录Token) |

返回内容示例:

```json
{
  "id": "01a1102a-ce8f-72ce-8346-f7b709f1b3ea", //获取状态ID
  "status": "PENDING_PROVIDER", //评论状态
  "contentRole": "TOPIC_REPLY", //评论类型
  "request": {
    "topicId": "01a0eb91-5d11-7fb0-b998-179add93620f", //帖子ID
    "markdown": "测试评论", //评论内容
    "replyToPostNumber": 1 //回复评论(若非回复则为1,否则为回复评论的序号)
  },
  "riskLevel": null, //评论风险等级
  "topicId": "01a0eb91-5d11-7fb0-b998-179add93620f", //帖子ID
  "postId": "01a1102a-ce91-7e65-85d7-a76573232021", //评论ID
  "postNumber": 33, //评论序号
  "baseRevision": null, //评论上一个版本
  "createdAt": "2026-10-06T07:43:23.268Z", //评论创建时间
  "updatedAt": "2026-10-06T07:43:23.268Z" //评论更新时间
}
```

## 发布帖子

```text
POST https://cdsq.dao3.fun/api/v1/posts
```

请求标头:

| 键     | 意思                    |
| ------ | ----------------------- |
| cookie | Cookie(需包含登录Token) |

请求负荷:

| 键       | 意思                                                  |
| -------- | ----------------------------------------------------- |
| markdown | Markdown格式帖子内容                                  |
| tagIds   | 标签ID,固定为["01a0ab26-84a8-718b-996a-36be3dda4fa4"] |
| title    | 帖子标题                                              |
| kind     | 固定为"DISCUSSION"                                    |

响应表头:

| 键         | 意思                      |
| ---------- | ------------------------- |
| set-cookie | Cookie,用于获取详情时使用 |

返回内容示例:

```json
{
  "submissionId": "01a1102a-ce8f-72ce-8346-f7b709f1b3ea", //帖子提交ID
  "topicId": "01a0eb91-5d11-7fb0-b998-179add93620f", //帖子ID
  "postId": "01a1102a-ce91-7e65-85d7-a76573232021", //获取帖子详情ID
  "status": "PENDING_PROVIDER" //帖子当前状态
}
```

## 获取帖子详情

```text
GET https://cdsq.dao3.fun/api/v1/posts/{ID}
```

查询参数:

- `ID`: 获取帖子详情ID（发布帖子返回的postId）

请求标头:

| 键     | 意思                    |
| ------ | ----------------------- |
| cookie | Cookie(需包含登录Token) |

返回内容示例:

```json
{
  "postId": "01a113f4-4054-7f92-b407-c653cfef5275", //获取帖子详情ID
  "topicId": "01a113f4-4051-7dcb-a5b4-cea6b7f98cfb", //帖子ID
  "contentRole": "TOPIC_FIRST_POST", //帖子身份
  "request": {
    "title": "test", //帖子标题
    "kind": "DISCUSSION", //帖子类型
    "tagIds": ["01a0ab26-84a8-718b-996a-36be3dda4fa4"], //帖子标签ID
    "markdown": "test" //帖子内容
  },
  "currentRevision": 1,
  "latestSubmissionId": "01a113f4-4050-743b-b033-e82f60dc145b", //帖子提交ID
  "latestSubmissionStatus": "PUBLISHED", //帖子当前状态
  "publishedAt": "2026-10-07T01:22:26.835Z", //帖子发布时间
  "editAttemptsUsed": 0, //帖子编辑次数
  "editAttemptsRemaining": null, //帖子剩余编辑次数
  "canEdit": true, //帖子是否能编辑
  "editBlockedReason": null //帖子编辑被阻止原因
}
```
