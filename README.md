# AI FAQ Assistant

使用 **Python + uv + Groq LLM** 依照小型 FAQ 知識庫產生回答，再透過 **GitHub Actions** 自動部署到 **GitHub Pages**。

## 1. 作品功能
- Python 使用 Groq 官方 SDK 呼叫 openai/gpt-oss-20b 模型。
- 向 LLM 提供 FAQ 參考答案，生成 4 題繁體中文回答。
- 輸出 `public/results.json` 及 `public/index.html`。
- 推送 `main` 分支後，GitHub Actions 自動執行 Python 並部署 Pages。
- **注意：GitHub Pages 是靜態結果展示，非即時聊天網站。**

## 2. 本機執行
1. 安裝 Python 3.12 與 [uv](https://docs.astral.sh/uv/getting-started/installation/)。
2. 在 [Groq Console](https://console.groq.com/keys) 取得 API Key。
3. 不要把金鑰提交至 GitHub；設定環境變數後執行：

   Windows PowerShell:
   ```powershell
   $env:GROQ_API_KEY="你的金鑰"
   uv run python main.py
   ```
   macOS / Linux:
   ```bash
   export GROQ_API_KEY="你的金鑰"
   uv run python main.py
   ```
4. 開啟 `public/index.html`，查看 AI 生成的回答。

> 若 API 服務調整支援的模型，請透過 `GROQ_MODEL` 設定目前可用的模型 ID。

## 3. GitHub Actions 與 GitHub Pages
1. 建立公開 repository 並上傳檔案（包含 `.github/workflows/deploy.yml`）。
2. 開啟 Repository → Settings → Secrets and variables → Actions → New repository secret。
3. Secret 名稱設為 `GROQ_API_KEY`，值貼上自己的 Key。
4. Settings → Pages → Build and deployment → Source 選 **GitHub Actions**。
5. 推送到 `main`，或在 Actions → Build and deploy AI FAQ → Run workflow 手動執行。
6. 等 Actions 顯示綠色勾勾後，至 Settings → Pages 取得網站網址。

## 4. 執行結果
- Actions 日誌會顯示四題 AI 回答（不會印出金鑰）。
- Pages 網站包含：**做了什麼、怎麼執行、執行結果、AI 使用說明**。
- 若金鑰未設定、API 失敗或達到限額，workflow 會失敗，不會假裝生成成功。

## 5. AI 使用說明
- **使用工具：**
ChatGPT：協助規劃專案架構、撰寫 Python 程式、建立 GitHub Actions workflow，以及排除執行錯誤。
Groq API：使用 openai/gpt-oss-20b 模型產生繁體中文 FAQ 回答。

- **使用位置：**
main.py：LLM API 呼叫、提示詞設計及 FAQ 回答產生。render()：將 FAQ 問答結果轉換為 HTML 網頁。
.github/workflows/deploy.yml：自動執行 Python 並部署至 GitHub Pages。

- **個人修改與個人驗證：**
1.調整 GitHub Repository 的檔案結構，讓 main.py 與 pyproject.toml 位於根目錄。
2.修正 Python 程式的縮排錯誤。
3.將原本透過 urllib 呼叫 API 的方式改為 Groq 官方 Python SDK。
4.更換無法使用的模型為 openai/gpt-oss-20b。
5.於 2026 年 10 月 29 日確認 GitHub Actions 執行成功，並驗證 GitHub Pages 正常顯示四組 FAQ 回答。
  
**驗證結果：** 測試日期：2026 年 10 月 29 日。
確認 GitHub Actions 成功執行，顯示綠色勾勾。
確認 GitHub Pages 可正常開啟。
確認網頁成功顯示四組繁體中文 FAQ 回答。
驗證 GitHub Actions 可在程式更新後自動執行與部署。



## 6. 專案檔案
```text
main.py                       # LLM 呼叫、資料產生和網頁產生
pyproject.toml                # uv 專案配置
.env.example                  # 環境變數範本（不是金鑰）
.gitignore                    # 排除 .env、產出檔案及虛擬環境
.github/workflows/deploy.yml  # GitHub Actions 自動部署
README.md                     # 功能、操作、執行與 AI 使用說明

main.py
pyproject.toml
README.md
.github/
    workflows/
        deploy.yml

```

## 7. 交作業前檢查
- [ ] GitHub Repo URL（貼到 iLearn）
- [ ] Pages URL（貼到 iLearn）
- [ ] 至少 5 次**實際** commit
- [ ] Actions 執行成功（綠勾）
- [ ] Pages 四頁內容完整（本站使用四個區塊）
- [ ] AI 使用說明已依實際操作修訂
- [ ] 沒有上傳任何真實 API Key 或 `.env`
