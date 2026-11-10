#!/usr/bin/env python3
"""Create one source-backed Japanese draft. Never publish automatically."""
import datetime
import html
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
KEY = os.getenv("GEMINI_API_KEY", "")
DISCLAIMER = "当サイトに掲載される情報は、正確性・完全性を保証するものではなく、内容を利用することで生じた損害について、当サイト運営者は故意または重過失がある場合を除き責任を負いません。"


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript", "svg"}:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript", "svg"} and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if not self.depth and data.strip():
            self.text.append(data)


def normalized(value):
    return re.sub(r"\s+", "", html.unescape(value))


def retry_transient_http(operation, stage, attempts=3):
    """Retry temporary upstream HTTP errors; never bypass evidence checks."""
    transient = {429, 500, 502, 503, 504}
    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except urllib.error.HTTPError as error:
            if error.code not in transient or attempt == attempts:
                print(
                    f"Failed at {stage}: HTTP {error.code} after {attempt} attempt(s)",
                    file=sys.stderr,
                )
                raise
            print(
                f"Temporary HTTP {error.code} at {stage}: retrying "
                f"({attempt}/{attempts})",
                file=sys.stderr,
            )
            time.sleep(2 ** (attempt - 1))


def fetch_official(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("Source must be an HTTPS URL")
    request = urllib.request.Request(
        url, headers={"User-Agent": "AffiliateAutopilot/0.1 (source verification)"}
    )
    with urllib.request.urlopen(request, timeout=25) as response:
        final = urllib.parse.urlparse(response.url)
        if final.scheme != "https":
            raise ValueError("Non-HTTPS redirect blocked")
        ctype = response.headers.get_content_type()
        if ctype != "text/html":
            raise ValueError("Only HTML sources are supported")
        raw = response.read(1_000_001)
        if len(raw) > 1_000_000:
            raise ValueError("Source too large")
        charset = response.headers.get_content_charset() or "utf-8"
    parser = VisibleText()
    parser.feed(raw.decode(charset, errors="replace"))
    value = re.sub(r"\s+", " ", " ".join(parser.text)).strip()
    if len(value) < 200:
        raise ValueError("Source has insufficient readable content")
    return {"url": url, "text": value[:18000]}


def generate(topic, sources, repair_note=None):
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": (
                "あなたは日本語の記事編集者です。以下の一次情報だけを材料に、"
                "読者に役立つ記事の下書きを作成してください。誇張、憶測、虚偽、"
                "出典にない企業比較、数字、料金、割引、報酬、資格条件、推薦順位、"
                "法律・制度の解釈を新しく作らないでください。広告リンクや体験談を捏造しないでください。"
                "リンク先の文章を大量に引用・転載しないでください。"
                "出力はJSONのみ。形式は"
                '{"title":"...","lead":"...","sections":[{"heading":"...","text":"..."}],'
                '"claims":[{"claim":"短い事実","source_id":"S1","quote":"一次情報から短い原文の一部"}]}'
                "。claimsは2件以上、各quoteは文字数15～100文字で原文と一致するもの。"
                "出典のない事実は一切書かず、判断や助言は根拠と区別してください。"
                f"\n題材：{topic['title']}\n読者：{topic['audience']}\n"
                "参考資料：\n" +
                "\n".join(f"S{i+1} URL:{s['url']}\n{s['text'][:11000]}"
                          for i, s in enumerate(sources)) +
                (("\n前の生成結果は検証で拒否されました: " + repair_note +
                  "。記事全体を最初からJSONで作り直してください。"
                  "quoteは必ず原文から連続した15～100文字をそのまま抜き出し、"
                  "短すぎる・長すぎる引用は出力しないでください。")
                 if repair_note else "")
            )}]
        }],
        "generationConfig": {"responseMimeType": "application/json", "maxOutputTokens": 3600}
    }
    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        + urllib.parse.quote(MODEL, safe="-_.") + ":generateContent"
    )
    req = urllib.request.Request(
        endpoint, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST", headers={"Content-Type": "application/json",
                                "x-goog-api-key": KEY},
    )
    with urllib.request.urlopen(req, timeout=100) as response:
        result = json.load(response)
    pieces = result["candidates"][0]["content"]["parts"]
    response_text = "".join(p.get("text", "") for p in pieces)
    return json.loads(response_text)


def validate(article, sources):
    if not isinstance(article, dict):
        raise ValueError("Invalid response type")
    if not isinstance(article.get("title"), str) or not article["title"].strip():
        raise ValueError("Missing title")
    if not isinstance(article.get("lead"), str) or len(article["lead"]) < 20:
        raise ValueError("Missing lead")
    sections = article.get("sections")
    if not isinstance(sections, list) or len(sections) < 2:
        raise ValueError("Too few sections")
    for section in sections:
        if not isinstance(section, dict) or not all(
            isinstance(section.get(k), str) and section[k].strip()
            for k in ("heading", "text")
        ):
            raise ValueError("Invalid section")
    claims = article.get("claims")
    if not isinstance(claims, list) or len(claims) < 2:
        raise ValueError("Insufficient evidence claims")
    for claim in claims:
        if not isinstance(claim, dict):
            raise ValueError("Invalid claim")
        sid, excerpt = claim.get("source_id"), claim.get("quote")
        if not isinstance(sid, str) or not re.fullmatch(r"S[1-9][0-9]*", sid):
            raise ValueError("Unknown source reference")
        idx = int(sid[1:]) - 1
        if idx >= len(sources) or not isinstance(excerpt, str):
            raise ValueError("Invalid evidence")
        if not (15 <= len(excerpt) <= 100):
            raise ValueError("Evidence quote length invalid")
        if normalized(excerpt) not in normalized(sources[idx]["text"]):
            raise ValueError(f"Evidence quote cannot be located in {sid}")
        if not isinstance(claim.get("claim"), str) or not claim["claim"].strip():
            raise ValueError("Missing claim")
    # Evidence-excerpt matching is not semantic verification.
    # Keep all generated drafts unpublished pending human review.
    return True


def main():
    if not KEY:
        print("GEMINI_API_KEY not configured. No draft created.")
        return
    topics = json.loads((ROOT / "topics.json").read_text(encoding="utf-8"))
    for topic in topics:
        slug = topic["slug"]
        if not re.fullmatch(r"[a-z0-9-]{3,64}", slug):
            raise ValueError("Invalid slug")
        destination = ROOT / "drafts" / (slug + ".md")
        if destination.exists():
            continue
        urls = topic.get("source_urls", [])
        if not (1 <= len(urls) <= 3):
            raise ValueError("Each topic needs 1-3 source URLs")
        sources = [
            retry_transient_http(
                lambda source_url=url: fetch_official(source_url),
                f"official source: {url}",
            )
            for url in urls
        ]
        # Retry a small number of times when model output fails strict evidence checks.
        # Every attempt is validated. Nothing is stored when all attempts fail.
        article = None
        repair_note = None
        for attempt in range(3):
            article = retry_transient_http(
                lambda: generate(topic, sources, repair_note=repair_note),
                "Gemini draft API",
            )
            try:
                validate(article, sources)
                break
            except ValueError as error:
                repair_note = str(error)
                print(f"Validation failed (attempt {attempt + 1}/3): {repair_note}")
                if attempt == 2:
                    raise

        today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
        lines = [
            "<!-- DRAFT: REVIEW REQUIRED. NOT FOR AUTOMATIC PUBLICATION. -->",
            "# " + article["title"], "",
            "**公開状態：未公開・人による確認待ち**", "",
            article["lead"], "",
        ]
        for section in article["sections"]:
            lines += ["## " + section["heading"], "", section["text"], ""]
        lines += ["## 参照した一次情報", ""]
        for i, source in enumerate(sources):
            lines.append(f"- [S{i+1}] {source['url']} （取得日：{today}）")
        lines += ["", "## 確認が必要な点", "",
                  "- 出典文面と記事本文の意味が正しく対応しているか",
                  "- 制度・提供条件・日付・数値が最新か",
                  "- 広告表記、ASP規約、リンク先が適切か",
                  "- 独自の価値があり、著作権・各社規約に抵触しないか", ""]
        ledger = {
            "status": "manual_review_required",
            "source_retrieved_utc": today,
            "model": MODEL, "topic": slug,
            "sources": [s["url"] for s in sources],
            "claims": article["claims"],
            "warning": "Quote presence is checked mechanically; claim entailment is NOT verified.",
        }
        lines += ["", "## 免責事項", "", DISCLAIMER, ""]
        destination.parent.mkdir(parents=True, exist_ok=True)
        proof = ROOT / "evidence" / (slug + ".json")
        proof.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("\n".join(lines), encoding="utf-8")
        proof.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
        print(f"Created REVIEW-REQUIRED draft: {slug}")
        return
    print("All configured topics already have drafts. No changes.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, IndexError, urllib.error.URLError, TimeoutError,
            json.JSONDecodeError) as error:
        print(f"Blocked: draft generation or evidence validation failed: {error}", file=sys.stderr)
        sys.exit(1)
