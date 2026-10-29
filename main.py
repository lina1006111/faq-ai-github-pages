"""Generate a static FAQ page using an LLM via Groq's API."""
import html
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "public"
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
FAQ = [
    ("忘記密碼怎麼辦？", "請點選登入頁面的「忘記密碼」，輸入註冊信箱，並依照收到的郵件重設密碼。"),
    ("如何修改會員資料？", "登入後前往「會員中心」與「個人資料」，修改後記得儲存。"),
    ("訂單取消後多久退款？", "退款時間依付款方式與商家政策而異，請至訂單紀錄查看狀態，或聯繫客服。"),
    ("沒有收到驗證信怎麼辦？", "先檢查垃圾郵件與信箱地址，稍後重新寄送；若仍未收到，請聯絡客服。"),
]


def ask_llm(question: str) -> str:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError("Missing GROQ_API_KEY. Set it locally or in GitHub Actions secrets.")
    prompt = "\n".join(f"問：{q}\n參考回答：{a}" for q, a in FAQ)
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "你是繁體中文 FAQ 客服助理。請根據以下 FAQ 回答問題，答案不超過 100 字。如果資訊不足，請明確表示無法確認，不要編造政策。\n" + prompt},
            {"role": "user", "content": question},
        ],
        "temperature": 0.2,
    }
    req = Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    
    req.add_header("User-Agent", "FAQ-AI-Homework/1.0")

    try:
        with urlopen(req, timeout=45) as response:
            result = json.load(response)
    except HTTPError as exc:
         error_body = exc.read().decode("utf-8", errors="replace")
         raise RuntimeError(
             f"Groq API returned HTTP {exc.code}: {error_body}"
         ) from exc
    except URLError as exc:
        raise RuntimeError("Unable to reach Groq API") from exc
    return result["choices"][0]["message"]["content"].strip()


def render(results: list[dict]) -> str:
    cards = "\n".join(
        f'<article class="card"><p class="q">Q. {html.escape(item["question"])}</p>'
        f'<p class="answer">{html.escape(item["answer"])}</p></article>'
        for item in results
    )
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI FAQ Assistant | Python × LLM</title>
<style>
:root{{color-scheme:light;font-family:system-ui,-apple-system,"Noto Sans TC",sans-serif}}
*{{box-sizing:border-box}}body{{margin:0;background:#f5f7fb;color:#213049;line-height:1.7}}
main{{max-width:850px;margin:auto;padding:36px 20px 72px}}header{{background:linear-gradient(120deg,#153f74,#2564a9);color:white;padding:40px 24px;border-radius:20px}}
h1{{font-size:clamp(28px,5vw,40px);margin:0}}header p{{margin:8px 0 0;color:#e3efff}}section{{margin-top:35px}}h2{{font-size:22px;margin-bottom:12px}}
.card{{background:#fff;border:1px solid #dfe6f1;padding:18px 22px;border-radius:13px;margin:12px 0;box-shadow:0 3px 9px #2037550a}}
.q{{font-weight:700;color:#1b4f88;margin:0 0 8px}}.answer{{margin:0;white-space:pre-wrap}}
small,.muted{{color:#627086}}code{{background:#e7edf8;padding:2px 6px;border-radius:4px}}a{{color:#1455a2}}
</style></head><body><main>
<header><h1>AI FAQ Assistant</h1><p>Python × Groq LLM × GitHub Actions × GitHub Pages</p></header>
<section><h2>1. 做了什麼</h2><p>使用 Python 呼叫雲端大型語言模型，根據常見問題知識庫，生成客服問題的繁體中文回答。下列回答在部署時由 AI 自動產生。</p></section>
<section><h2>2. 怎麼執行</h2><p>設定 <code>GROQ_API_KEY</code> 環境變數，再執行 <code>uv run python main.py</code>。每次推送到 GitHub main 分支，GitHub Actions 會重新執行並部署網站。</p></section>
<section><h2>3. 執行結果</h2>{cards}<p class="muted">生成時間：{date} ｜ 模型：{html.escape(MODEL)}</p></section>
<section><h2>4. AI 使用說明</h2><p>使用 AI 協助規劃程式架構、撰寫 Python 與網頁初稿、解釋 GitHub Actions。專案使用 Groq 的 LLM API 生成 FAQ 答案，並以自訂 FAQ 資料、提示詞和錯誤處理限制回答內容。實際修改與驗證方式請參閱 GitHub README。</p></section>
<footer><small>本頁為課程示範作品，內容非真實商家的正式客服政策。網頁為靜態展示，不提供即時 AI 問答。</small></footer>
</main></body></html>'''


def main() -> None:
    OUT.mkdir(exist_ok=True)
    results = []
    for question, _ in FAQ:
        answer = ask_llm(question)
        results.append({"question": question, "answer": answer})
        print(f"Q: {question}\nA: {answer}\n")
    (OUT / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "index.html").write_text(render(results), encoding="utf-8")
    print("Generated public/index.html and public/results.json")


if __name__ == "__main__":
    main()
