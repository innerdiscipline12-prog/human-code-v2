#!/usr/bin/env python3
"""Publish Human Code V3's two-slide image post to a Facebook Page."""
from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

GRAPH_VERSION = os.getenv("META_GRAPH_VERSION", "v27.0")
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_VERSION}"


def request_json(url: str, *, data=None, headers=None):
    req = urllib.request.Request(
        url,
        data=data,
        headers=headers or {},
        method="POST" if data is not None else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"error": {"message": body}}
        raise RuntimeError(
            f"Meta API HTTP {exc.code}: {json.dumps(payload, ensure_ascii=False)}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Meta API connection error: {exc}") from exc


def multipart(fields: dict[str, str], file_field: str, file_path: Path):
    boundary = "----HumanCodeBoundary7MA4YWxkTrZu0gW"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks += [
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
            value.encode(),
            b"\r\n",
        ]

    content_type = "image/png" if file_path.suffix.lower() == ".png" else "image/jpeg"
    chunks += [
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="{file_field}"; filename="{file_path.name}"\r\n'.encode(),
        f"Content-Type: {content_type}\r\n\r\n".encode(),
        file_path.read_bytes(),
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ]
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def upload_unpublished_photo(page_id: str, token: str, path: Path) -> str:
    body, content_type = multipart(
        {"access_token": token, "published": "false", "temporary": "true"},
        "source",
        path,
    )
    result = request_json(
        f"{GRAPH_BASE}/{page_id}/photos",
        data=body,
        headers={"Content-Type": content_type},
    )
    photo_id = result.get("id")
    if not photo_id:
        raise RuntimeError(f"Meta photo upload returned no id: {json.dumps(result)}")
    return str(photo_id)


def publish_multi_photo(page_id: str, token: str, caption: str, photo_ids: list[str]) -> str:
    fields = {"message": caption, "access_token": token}
    for i, photo_id in enumerate(photo_ids):
        fields[f"attached_media[{i}]"] = json.dumps(
            {"media_fbid": photo_id}, separators=(",", ":")
        )
    data = urllib.parse.urlencode(fields).encode("utf-8")
    result = request_json(
        f"{GRAPH_BASE}/{page_id}/feed",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    post_id = result.get("id")
    if not post_id:
        raise RuntimeError(
            f"Meta feed publish returned no post id: {json.dumps(result)}"
        )
    return str(post_id)


def resolve_page_token(page_id: str, page_token: str | None, system_user_token: str | None):
    if page_token:
        token = page_token
    else:
        query = urllib.parse.urlencode({
            "fields": "id,name,access_token,tasks",
            "access_token": system_user_token,
        })
        accounts = request_json(f"{GRAPH_BASE}/me/accounts?{query}")
        matches = [item for item in accounts.get("data", []) if str(item.get("id")) == str(page_id)]
        if not matches or not matches[0].get("access_token"):
            raise RuntimeError(
                f"System user token cannot access Page {page_id}. Response: {json.dumps(accounts)}"
            )
        token = matches[0]["access_token"]
        tasks = matches[0].get("tasks", [])
        if "CREATE_CONTENT" not in tasks:
            raise RuntimeError(
                f"Page token is missing CREATE_CONTENT task for Page {page_id}. Tasks: {tasks}"
            )

    query = urllib.parse.urlencode({"fields": "id,name", "access_token": token})
    result = request_json(f"{GRAPH_BASE}/{page_id}?{query}")
    if str(result.get("id")) != str(page_id):
        raise RuntimeError(
            f"Token did not resolve to expected Page: {json.dumps(result)}"
        )
    return token, result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="output")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    page_id = os.getenv("FACEBOOK_PAGE_ID")
    token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    system_user_token = os.getenv("META_SYSTEM_USER_ACCESS_TOKEN")

    if not page_id:
        raise SystemExit("FACEBOOK_PAGE_ID is required")
    if not token and not system_user_token and not args.dry_run:
        raise SystemExit("META_SYSTEM_USER_ACCESS_TOKEN is required")

    output = Path(args.output)
    slide_1 = output / "slide_1.png"
    slide_2 = output / "slide_2.png"
    caption_file = output / "caption.txt"

    for path in (slide_1, slide_2, caption_file):
        if not path.exists():
            raise SystemExit(f"Missing required artifact: {path}")

    caption = caption_file.read_text(encoding="utf-8").strip()
    if not caption:
        raise SystemExit("caption.txt is empty")

    for path in (slide_1, slide_2):
        if path.stat().st_size > 10 * 1024 * 1024:
            raise SystemExit(f"Facebook image exceeds 10 MB: {path}")

    if args.dry_run:
        print(json.dumps({
            "publisher": "Facebook Page multi-photo",
            "page_id": page_id,
            "slides": [slide_1.name, slide_2.name],
            "caption_chars": len(caption),
            "dry_run": True,
        }, indent=2))
        return

    token, page = resolve_page_token(page_id, token, system_user_token)
    print(f"Facebook token validated for Page: {page.get('name')} ({page.get('id')})")

    photo_ids = []
    for path in (slide_1, slide_2):
        photo_id = upload_unpublished_photo(page_id, token, path)
        photo_ids.append(photo_id)
        print(f"Uploaded unpublished photo: {path.name} -> {photo_id}")

    post_id = publish_multi_photo(page_id, token, caption, photo_ids)
    print(json.dumps({
        "publisher": "Facebook Page multi-photo",
        "page_id": page_id,
        "post_id": post_id,
        "photo_ids": photo_ids,
        "caption_chars": len(caption),
        "published": True,
    }, indent=2))


if __name__ == "__main__":
    main()
