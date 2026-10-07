#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pickcat 帖子信息获取工具。

获取 Pickcat 社区（https://cdsq.dao3.fun）的推荐/最新帖子列表、帖子详情、
热门评论，支持登录后携带会话 Cookie 发布评论、发布帖子并查询发布状态。
仅使用 Python 标准库，无任何第三方依赖。

长期配置（登录 Cookie、推荐流会话 Cookie 等）统一保存在 ~/.config/.pickcatskill（JSON，权限 600）。
"""

import argparse
import getpass
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from http.cookies import SimpleCookie, CookieError

BASE_URL = "https://cdsq.dao3.fun"
USER_AGENT = "pickcat-skill/1.0"
TIMEOUT = 30
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".config", ".pickcatskill")
LOGIN_KEYS = ("pickcat_session", "username", "expiresAt", "savedAt")
RECOMMENDATIONS_COOKIE_KEY = "recommendationsCookie"
# 发布帖子的固定参数（接口限制）：类型为 DISCUSSION，标签为「创作与作品」
POST_KIND = "DISCUSSION"
POST_TAG_IDS = ["01a0ab26-84a8-718b-996a-36be3dda4fa4"]


def fail(message):
    print("错误: %s" % message, file=sys.stderr)
    sys.exit(1)


# ---------- 配置读写 ----------

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError) as exc:
        print("警告: 配置文件 %s 无法读取（%s），本次请求不携带 Cookie" % (CONFIG_PATH, exc),
              file=sys.stderr)
        return {}


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    fd = os.open(CONFIG_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    os.chmod(CONFIG_PATH, 0o600)


def warn_if_expired(config):
    expires_at = config.get("expiresAt")
    if not expires_at:
        return
    try:
        expire_time = datetime.fromisoformat(str(expires_at).replace("Z", "+00:00"))
        if datetime.now(timezone.utc) >= expire_time:
            print("警告: 已保存的登录 Cookie 已于 %s 过期，请重新运行 login" % expires_at,
                  file=sys.stderr)
    except ValueError:
        pass


# ---------- HTTP ----------

def extract_cookie_value(set_cookie_headers, name):
    """从 Set-Cookie 响应头列表里取出指定 Cookie 的值，找不到返回 None。"""
    for header_value in set_cookie_headers or []:
        cookie = SimpleCookie()
        try:
            cookie.load(header_value)
        except CookieError:
            continue
        if name in cookie:
            return cookie[name].value
    return None


def build_headers(cursor=None):
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    config = load_config()
    token = config.get("pickcat_session")
    if token:
        warn_if_expired(config)
        headers["Cookie"] = "pickcat_session=%s" % token
    # 推荐流（sort=recommended）的游标与服务端下发的 pickcat_recommendations
    # Cookie 绑定，翻页请求必须携带，否则返回 RECOMMENDATION_CURSOR_INVALID
    rec_cookie = config.get(RECOMMENDATIONS_COOKIE_KEY)
    if cursor and rec_cookie:
        parts = []
        if "Cookie" in headers:
            parts.append(headers["Cookie"])
        parts.append("pickcat_recommendations=%s" % rec_cookie)
        headers["Cookie"] = "; ".join(parts)
    return headers


def store_recommendations_cookie(value):
    if not value:
        return
    config = load_config()
    if config.get(RECOMMENDATIONS_COOKIE_KEY) == value:
        return
    config[RECOMMENDATIONS_COOKIE_KEY] = value
    save_config(config)


def api_get(path, cursor=None):
    request = urllib.request.Request(
        BASE_URL + path,
        headers=build_headers(cursor),
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            rec_cookie = extract_cookie_value(
                response.headers.get_all("Set-Cookie"), "pickcat_recommendations")
            if rec_cookie:
                store_recommendations_cookie(rec_cookie)
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            fail("登录已失效（HTTP 401），服务端拒绝了已保存的 Cookie。请重新运行: "
                 "login --username <账户名> [--password <密码>]")
        detail = error_detail(exc)
        if "推荐游标" in detail or "RECOMMENDATION_CURSOR_INVALID" in detail:
            fail("推荐流游标已失效（%s）。请去掉 --cursor 重新获取第一页，"
                 "或改用 --pages 一次抓完多页。" % detail)
        fail("HTTP %s: %s（请检查帖子 ID / cursor 是否正确，或稍后重试）" % (exc.code, exc.reason))
    except urllib.error.URLError as exc:
        fail("无法连接 %s: %s" % (BASE_URL, exc.reason))
    except json.JSONDecodeError:
        fail("接口返回了无法解析的内容")


def error_detail(exc):
    try:
        data = json.loads(exc.read().decode("utf-8"))
        return data.get("message") or data.get("code") or ""
    except Exception:
        return ""


def api_post(path, payload, action):
    headers = build_headers()
    headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            fail("%s失败：登录已失效（HTTP 401），请重新运行: "
                 "login --username <账户名> [--password <密码>]" % action)
        detail = error_detail(exc)
        fail("%s失败（HTTP %s）%s" % (action, exc.code, ("：" + detail) if detail else ""))
    except urllib.error.URLError as exc:
        fail("无法连接 %s: %s" % (BASE_URL, exc.reason))
    except json.JSONDecodeError:
        fail("接口返回了无法解析的内容")


def require_login():
    config = load_config()
    if not config.get("pickcat_session"):
        fail("该操作需要登录。请先运行: login --username <账户名> [--password <密码>]")
    return config


# ---------- HTML 转纯文本 ----------

class HTMLTextExtractor(HTMLParser):
    """把帖子/评论 HTML（cookedHtml）转成纯文本。

    图片转为 [图片: 完整URL]；论坛表情图片（alt 为 [emoji:...]）直接保留 alt 文本。
    """

    BLOCK_TAGS = {"p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
                  "blockquote", "pre", "table", "ul", "ol", "hr", "section"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.parts.append("\n")
        elif tag == "img":
            attrs_dict = dict(attrs)
            alt = attrs_dict.get("alt") or ""
            src = attrs_dict.get("src") or ""
            if alt.startswith("[emoji:"):
                self.parts.append(alt)
            elif src:
                self.parts.append(" [图片: %s] " % urllib.parse.urljoin(BASE_URL, src))
        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)

    def text(self):
        lines = [line.strip() for line in "".join(self.parts).split("\n")]
        result = []
        for line in lines:
            if line or (result and result[-1]):
                result.append(line)
        return "\n".join(result).strip()


def html_to_text(html):
    extractor = HTMLTextExtractor()
    try:
        extractor.feed(html or "")
    except Exception:
        return html or ""
    return extractor.text()


# ---------- 列表 / 评论抓取 ----------

def clamp(value, low, high):
    return max(low, min(high, value))


def fetch_pages(fetch_page, pages, first_cursor=None):
    """按页抓取，自动用 pageInfo.nextCursor 接力，返回每页原始数据。"""
    data_pages = []
    cursor = first_cursor
    for _ in range(clamp(pages, 1, 20)):
        data = fetch_page(cursor)
        data_pages.append(data)
        page_info = data.get("pageInfo") or {}
        if not page_info.get("hasNextPage") or not page_info.get("nextCursor"):
            break
        cursor = page_info["nextCursor"]
    return data_pages


def print_pages_json(data_pages):
    if len(data_pages) == 1:
        print(json.dumps(data_pages[0], ensure_ascii=False, indent=2))
        return
    merged_items = []
    for page in data_pages:
        merged_items.extend(page.get("items") or [])
    merged = {
        "pages": len(data_pages),
        "items": merged_items,
        "pageInfo": data_pages[-1].get("pageInfo"),
    }
    print(json.dumps(merged, ensure_ascii=False, indent=2))


def join_tag_names(tags):
    return "、".join(tag.get("name") or "" for tag in tags or []).strip("、")


def format_count(item):
    return "回复 %s | 查看 %s | 点赞 %s | 收藏 %s" % (
        item.get("replyCount", 0),
        item.get("viewCount", 0),
        item.get("likeCount", 0),
        item.get("bookmarkCount", 0),
    )


def print_list_summary(items, page_info):
    if not items:
        print("（本页没有帖子）")
        return
    for index, item in enumerate(items, 1):
        author = (item.get("author") or {}).get("username") or "未知"
        flags = []
        if item.get("pinnedGlobally"):
            flags.append("全局置顶")
        elif item.get("pinned"):
            flags.append("置顶")
        if item.get("closedAt"):
            flags.append("已关闭")
        flag_text = (" | " + "、".join(flags)) if flags else ""
        print("%d. %s" % (index, item.get("title") or "(无标题)"))
        print("   ID: %s" % item.get("id"))
        print("   类型: %s | 作者: %s%s" % (item.get("kind") or "未知", author, flag_text))
        print("   %s" % format_count(item))
        tags = join_tag_names(item.get("tags"))
        if tags:
            print("   标签: %s" % tags)
        print("   创建: %s | 最后活动: %s" % (item.get("createdAt"), item.get("lastActivityAt")))
        excerpt = (item.get("excerpt") or "").strip()
        if excerpt:
            print("   摘要: %s" % excerpt.replace("\n", " "))
        print()
    if page_info.get("hasNextPage") and page_info.get("nextCursor"):
        print("还有下一页。取下一页: 加参数 --cursor %s" % page_info["nextCursor"])
    else:
        print("没有更多页面了。")


def print_replies_summary(items, page_info):
    if not items:
        print("（本页没有评论）")
        return
    for item in items:
        author = (item.get("author") or {}).get("username") or "未知"
        header = "#%s %s" % (item.get("postNumber"), author)
        reply_to = item.get("replyToPostNumber")
        if reply_to not in (None, 1):
            header += " → 回复 #%s" % reply_to
        flags = []
        if item.get("pinned"):
            flags.append("置顶")
        if item.get("editedAt"):
            flags.append("已编辑")
        if item.get("deleted"):
            flags.append("已删除")
        if flags:
            header += "（%s）" % "、".join(flags)
        print(header)
        print("   赞 %s | %s" % (item.get("likeCount", 0), item.get("createdAt")))
        content = html_to_text(item.get("cookedHtml"))
        if content:
            print("   %s" % content.replace("\n", "\n   "))
        print()
    if page_info.get("hasNextPage") and page_info.get("nextCursor"):
        print("还有下一页。取下一页: 加参数 --cursor %s" % page_info["nextCursor"])
    else:
        print("没有更多页面了。")


# ---------- 子命令处理 ----------

def handle_list(args, sort):
    limit = clamp(args.limit, 1, 50)

    def fetch_page(cursor):
        params = {"sort": sort, "limit": str(limit)}
        if cursor:
            params["cursor"] = cursor
        return api_get("/api/v1/topic-recommendations?" + urllib.parse.urlencode(params),
                       cursor=cursor)

    data_pages = fetch_pages(fetch_page, args.pages, args.cursor)
    if args.json:
        print_pages_json(data_pages)
    else:
        all_items = []
        for page in data_pages:
            all_items.extend(page.get("items") or [])
        print_list_summary(all_items, data_pages[-1].get("pageInfo") or {})


def handle_replies(args):
    limit = clamp(args.limit, 1, 50)
    topic_path = "/api/v1/topics/%s/posts" % urllib.parse.quote(args.id, safe="")

    def fetch_page(cursor):
        params = {"limit": str(limit), "sort": "hot"}
        if cursor:
            params["cursor"] = cursor
        return api_get(topic_path + "?" + urllib.parse.urlencode(params), cursor=cursor)

    data_pages = fetch_pages(fetch_page, args.pages, args.cursor)
    if args.json:
        print_pages_json(data_pages)
    else:
        all_items = []
        for page in data_pages:
            all_items.extend(page.get("items") or [])
        print_replies_summary(all_items, data_pages[-1].get("pageInfo") or {})


def handle_topic(args):
    data = api_get("/api/v1/topics/" + urllib.parse.quote(args.id, safe=""))
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    author = (data.get("author") or {}).get("username") or "未知"
    first_post = data.get("firstPost") or {}
    collection = (data.get("collection") or {}).get("name")
    print("标题: %s" % (data.get("title") or "(无标题)"))
    print("ID: %s" % data.get("id"))
    print("类型: %s | 作者: %s" % (data.get("kind") or "未知", author))
    if collection:
        print("合集: %s" % collection)
    tags = join_tag_names(data.get("tags"))
    if tags:
        print("标签: %s" % tags)
    print("回复 %s | 查看 %s | 首帖点赞 %s" % (
        data.get("replyCount", 0),
        data.get("viewCount", 0),
        first_post.get("likeCount", 0),
    ))
    print("创建: %s | 最后活动: %s" % (data.get("createdAt"), data.get("lastActivityAt")))
    if data.get("closedAt"):
        print("状态: 已关闭")
    print()
    print("========== 正文 ==========")
    content = html_to_text(first_post.get("cookedHtml"))
    print(content if content else "（无正文）")
    if data.get("repliesTruncated"):
        print()
        print("（回复不在本接口返回中。获取热门评论: replies %s，回复总数: %s）"
              % (data.get("id"), data.get("replyCount", 0)))


def handle_login(args):
    password = args.password
    if password is None:
        password = getpass.getpass("密码: ")
    payload = json.dumps({"username": args.username, "password": password}).encode("utf-8")
    request = urllib.request.Request(
        BASE_URL + "/api/v1/session",
        data=payload,
        method="POST",
        headers={"User-Agent": USER_AGENT, "Content-Type": "application/json",
                 "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            data = json.loads(response.read().decode("utf-8"))
            set_cookies = response.headers.get_all("Set-Cookie") or []
    except urllib.error.HTTPError as exc:
        detail = error_detail(exc)
        fail("登录失败（HTTP %s）%s" % (exc.code, ("：" + detail) if detail else ""))
    except urllib.error.URLError as exc:
        fail("无法连接 %s: %s" % (BASE_URL, exc.reason))
    except json.JSONDecodeError:
        fail("接口返回了无法解析的内容")

    token = extract_cookie_value(set_cookies, "pickcat_session")
    if not token:
        fail("登录响应中没有找到 pickcat_session Cookie")

    config = load_config()
    config.update({
        "pickcat_session": token,
        "username": args.username,
        "expiresAt": data.get("expiresAt"),
        "savedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    save_config(config)

    user = data.get("user") or {}
    print("登录成功：%s（等级 %s）" % (
        user.get("username") or args.username,
        (user.get("level") or {}).get("current", "?"),
    ))
    print("Token 到期时间: %s" % data.get("expiresAt"))
    print("登录 Cookie 已保存到 %s（权限 600），后续请求将自动携带" % CONFIG_PATH)


def handle_logout(_args):
    config = load_config()
    if not any(key in config for key in LOGIN_KEYS):
        print("当前没有已保存的登录配置。")
        return
    for key in LOGIN_KEYS:
        config.pop(key, None)
    if config:
        save_config(config)
        print("已清除登录信息，其余配置保留在 %s。" % CONFIG_PATH)
    else:
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)
        print("已清除登录信息（%s）。" % CONFIG_PATH)


def resolve_markdown(value, label):
    markdown = value
    if markdown == "-":
        markdown = sys.stdin.read().strip()
    if not markdown:
        fail("%s内容不能为空（--markdown）" % label)
    return markdown


def handle_comment(args):
    require_login()
    markdown = resolve_markdown(args.markdown, "评论")
    data = api_post("/api/v1/posts", {
        "topicId": args.id,
        "markdown": markdown,
        "replyToPostNumber": args.reply_to,
    }, action="发布评论")

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    print("已提交，当前状态: %s" % data.get("status"))
    print("submissionId: %s" % data.get("submissionId"))
    print("commentId: %s" % data.get("postId"))
    print("topicId: %s" % data.get("topicId"))
    print("查询发布状态: comment-status %s（可加 --wait N 自动等待完成）" % data.get("submissionId"))


def handle_comment_status(args):
    require_login()
    path = "/api/v1/post-submissions/" + urllib.parse.quote(args.id, safe="")
    wait_seconds = clamp(args.wait, 0, 120)
    deadline = time.monotonic() + wait_seconds
    polled = False
    while True:
        data = api_get(path)
        status = str(data.get("status") or "")
        if wait_seconds == 0 or not status.startswith("PENDING"):
            break
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        polled = True
        time.sleep(min(2, remaining))
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    status = str(data.get("status") or "未知")
    request_info = data.get("request") or {}
    print("状态: %s" % status)
    print("submissionId: %s" % data.get("id"))
    print("commentId: %s" % data.get("postId"))
    print("楼层号: %s" % data.get("postNumber"))
    print("topicId: %s" % data.get("topicId"))
    markdown = (request_info.get("markdown") or "").strip()
    if markdown:
        print("内容: %s" % markdown.replace("\n", " "))
    print("创建: %s | 更新: %s" % (data.get("createdAt"), data.get("updatedAt")))
    if status.startswith("PENDING"):
        waited = ("，已轮询等待 %s 秒" % wait_seconds) if polled else ""
        print("（评论仍在处理中%s，可稍后重查）" % waited)


def handle_post(args):
    require_login()
    markdown = resolve_markdown(args.markdown, "帖子")
    data = api_post("/api/v1/posts", {
        "title": args.title,
        "kind": POST_KIND,
        "tagIds": POST_TAG_IDS,
        "markdown": markdown,
    }, action="发布帖子")

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    print("已提交，当前状态: %s" % data.get("status"))
    print("submissionId: %s" % data.get("submissionId"))
    print("postId: %s" % data.get("postId"))
    print("topicId: %s" % data.get("topicId"))
    print("查询发布状态: post-status %s（可加 --wait N 自动等待完成）" % data.get("postId"))


def handle_post_status(args):
    require_login()
    path = "/api/v1/posts/" + urllib.parse.quote(args.id, safe="")
    wait_seconds = clamp(args.wait, 0, 120)
    deadline = time.monotonic() + wait_seconds
    polled = False
    while True:
        data = api_get(path)
        status = str(data.get("latestSubmissionStatus") or "")
        if wait_seconds == 0 or not status.startswith("PENDING"):
            break
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        polled = True
        time.sleep(min(2, remaining))
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    status = str(data.get("latestSubmissionStatus") or "未知")
    request_info = data.get("request") or {}
    print("状态: %s" % status)
    print("postId: %s" % data.get("postId"))
    print("topicId: %s" % data.get("topicId"))
    print("标题: %s" % (request_info.get("title") or "(无标题)"))
    markdown = (request_info.get("markdown") or "").strip()
    if markdown:
        print("内容: %s" % markdown.replace("\n", " "))
    print("发布时间: %s" % (data.get("publishedAt") or "（尚未发布）"))
    print("编辑次数: %s | 可编辑: %s" % (data.get("editAttemptsUsed", 0), data.get("canEdit")))
    if data.get("editBlockedReason"):
        print("编辑被阻止原因: %s" % data.get("editBlockedReason"))
    if status.startswith("PENDING"):
        waited = ("，已轮询等待 %s 秒" % wait_seconds) if polled else ""
        print("（帖子仍在处理中%s，可稍后重查）" % waited)
    elif data.get("topicId"):
        print("查看公开详情: topic %s" % data.get("topicId"))


# ---------- 命令行入口 ----------

def add_list_args(parser, default_limit):
    parser.add_argument("--limit", type=int, default=default_limit,
                        help="每页条数，默认 %d，范围 1-50" % default_limit)
    parser.add_argument("--cursor", default=None, help="上一页返回的 pageInfo.nextCursor")
    parser.add_argument("--pages", type=int, default=1, help="连续抓取的页数，默认 1，范围 1-20")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON 而不是精简摘要")


def main():
    parser = argparse.ArgumentParser(
        description="获取 Pickcat 社区（cdsq.dao3.fun）帖子信息",
        prog="pickcat.py",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_recommended = subparsers.add_parser("recommended", help="获取推荐内容列表")
    add_list_args(p_recommended, 20)
    p_recommended.set_defaults(func=lambda a: handle_list(a, "recommended"))

    p_latest = subparsers.add_parser("latest", help="获取最新内容列表")
    add_list_args(p_latest, 20)
    p_latest.set_defaults(func=lambda a: handle_list(a, "latest"))

    p_topic = subparsers.add_parser("topic", help="获取指定帖子的完整详情与正文")
    p_topic.add_argument("id", help="帖子 ID（从列表结果的 ID 字段获取）")
    p_topic.add_argument("--json", action="store_true", help="输出原始 JSON")
    p_topic.set_defaults(func=handle_topic)

    p_replies = subparsers.add_parser("replies", help="获取帖子热门评论（sort=hot，按热度排序）")
    p_replies.add_argument("id", help="帖子 ID（从列表结果的 ID 字段获取）")
    add_list_args(p_replies, 50)
    p_replies.set_defaults(func=handle_replies)

    p_login = subparsers.add_parser("login", help="登录账户，Cookie 保存到 ~/.config/.pickcatskill")
    p_login.add_argument("--username", required=True, help="账户名")
    p_login.add_argument("--password", default=None, help="密码（省略则交互式输入）")
    p_login.set_defaults(func=handle_login)

    p_logout = subparsers.add_parser("logout", help="清除已保存的登录 Cookie")
    p_logout.set_defaults(func=handle_logout)

    p_comment = subparsers.add_parser("comment", help="发布评论（需先登录）")
    p_comment.add_argument("id", help="帖子 ID")
    p_comment.add_argument("--markdown", required=True,
                           help="Markdown 格式评论内容；值为 - 时从 stdin 读取")
    p_comment.add_argument("--reply-to", type=int, default=1,
                           help="回复目标楼层号，默认 1 表示直接回复主帖")
    p_comment.add_argument("--json", action="store_true", help="输出原始 JSON")
    p_comment.set_defaults(func=handle_comment)

    p_status = subparsers.add_parser("comment-status", help="查询评论发布状态（需先登录）")
    p_status.add_argument("id", help="发布评论时返回的 submissionId")
    p_status.add_argument("--wait", type=int, default=0,
                          help="评论仍在处理中时自动轮询（间隔 2 秒），最多等待 N 秒，"
                               "默认 0 表示只查一次，范围 0-120")
    p_status.add_argument("--json", action="store_true", help="输出原始 JSON")
    p_status.set_defaults(func=handle_comment_status)

    p_post = subparsers.add_parser(
        "post", help="发布帖子（需先登录；类型固定 DISCUSSION，标签固定「创作与作品」）")
    p_post.add_argument("--title", required=True, help="帖子标题")
    p_post.add_argument("--markdown", required=True,
                        help="Markdown 格式帖子正文；值为 - 时从 stdin 读取")
    p_post.add_argument("--json", action="store_true", help="输出原始 JSON")
    p_post.set_defaults(func=handle_post)

    p_post_status = subparsers.add_parser(
        "post-status", help="查询已发布帖子的详情与发布状态（需先登录）")
    p_post_status.add_argument("id", help="发布帖子时返回的 postId")
    p_post_status.add_argument("--wait", type=int, default=0,
                               help="帖子仍在处理中时自动轮询（间隔 2 秒），最多等待 N 秒，"
                                    "默认 0 表示只查一次，范围 0-120")
    p_post_status.add_argument("--json", action="store_true", help="输出原始 JSON")
    p_post_status.set_defaults(func=handle_post_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
