# Affiliate Autopilot

初期構築中のアフィリエイトサイト自動運用プロジェクト。

## 現在の進捗
- GitHub リポジトリ: 作成済み
- 公開用Webページ: `public/` 配信
- 記事候補: `topics.json` に2件登録
- 記事下書き生成プログラム: `automation/generate_draft.py` 作成済み
- 定期実行の設定: `.github/workflows/draft.yml` 作成済み（毎週月曜10:17 JST）
- Gemini APIキー: GitHub Secretsに登録済み（値は非公開）
- 実行テスト: 2回目のテストで成功（2026-11-03、下書き1本保存）
- 事実確認: URL取得＋出典原文との短い引用文字列の照合まで。意味の正確さや情報の鮮度を保証しない
- A8.net: 会員登録済み（ユーザー申告）。広告主との提携およびアフィリエイトリンク: **未設定**
- Cloudflare Pages公開: **公開済み**（過去にユーザー画面で表示確認済み）

## 設計
1. 登録した一次情報URLからHTMLテキストを取得する。
2. Gemini APIを使って日本語の下書きを作成する。
3. 出典の存在と引用箇所の一致を確認。満たさない場合は停止。
4. 下書きと根拠一覧を `drafts/` と `evidence/` に保存（※現在のリポジトリはPublicのため、保存されるとGitHub上で閲覧可能）。
5. **公開サイトには自動反映しない。** 人による事実確認を含めた公開承認フローは未実装。
6. 将来的に、広告表示・最新条件チェック・サイト配信を整備する。

## 免責事項の表示
- サイトの初期ページ（`public/index.html` と `index.html`）のフッターに指定の免責文を表示。
- 既存の下書き、および今後生成する下書きの末尾にも同文を追加。
- 新しい記事公開機能を追加する場合も、同文が記事ページに反映されるか検証が必要。
- 免責文を掲載しても法律上の責任がすべて免除されるわけではない。

## 安全対策
- APIキーはリポジトリに書かず、GitHub Actions Secretsで管理する。
- 価格・制度・広告条件を確認せずに自動投稿しない。
- 引用元URLと確認日を保存する。
- AIが自分で「正しい」と評価することを事実確認の代わりにしない。
- 景品表示法、広告表示ガイドライン、ASP規約、利用規約、著作権に配慮する。

**注意:** この段階では稼働や収益を保証せず、無人運用はできません。

## 公開サイト（2026-11-03 更新）
- サイト名: えらびの地図
- サイト内運営者表記: えらびの地図編集室（法人名ではない）
- Cloudflare Pages: https://affiliate-autopilot-3ja.pages.dev/ （デプロイ結果の画面確認済み。今回の更新の実表示は未確認）
- 公開用ファイル: `public/` のみ（下書きは公開しない）
- `public/index.html`: 新トップページ
- `public/about/index.html`: 運営者情報（連絡先は未整備）
- `public/advertising/index.html`: 広告掲載方針
- `public/privacy/index.html`: プライバシーポリシー
- `public/assets/site.css`: 共通デザイン
- 広告案件・ASP登録・問い合わせ手段は未設定。法令上必要な表示および情報送信の実態は広告導入前に見直す。
- 現在の公開用HTMLは `noindex`、`public/robots.txt` はクロール禁止設定。正式公開時には見直す。

## 先行制作記事（2026-11-03）
- 1本目「20代の営業職が転職エージェントを選ぶときの5つの確認ポイント」: `drafts/20s-sales-agent-checklist.md`
- 掲載準備用HTML: `ready-to-publish/articles/20s-sales-agent-checklist/index.html`（公開対象の `public/` には未配置）
- 照合記録: `evidence/20s-sales-agent-checklist.json`
- 参考資料: 厚生労働省の公式ページ等5件とhape Agent公式1件。出典URLと記事内引用番号の整合確認済み
- 記事への広告リンク: なし。記事ファイル公開: **実施済み**（Cloudflare上の今回の表示は未確認）
- A8.net: 会員登録完了とユーザー申告あり。hape Agentの成果・否認条件は提供された画面で一部確認済み、提携は未実施
- 残る作業: 公開サイトの実表示確認、問い合わせ窓口整備、広告提携判断、追加記事制作

## 1本目公開（2026-11-03）
- 記事: `public/articles/20s-sales-agent-checklist/index.html`
- 一覧: `public/articles/index.html`
- トップページへの記事導線を設定
- 表示: `https://affiliate-autopilot-3ja.pages.dev/articles/20s-sales-agent-checklist/`（GitHubの登録を確認。Cloudflareの更新反映・画面表示は別途確認が必要）
- `public/robots.txt`: クロール許可
- `public/sitemap.xml`: URL 6件を登録
- 個別記事に広告リンクなし／APIキーは非公開のGitHub Secretsで管理
- 定期生成する記事の自動公開は未設定のまま。公開判断は個別に行う

## 追加記事の下書き（2026-11-03）
- 2本目: `drafts/sales-to-other-industry.md` → `public/articles/sales-to-other-industry/index.html`（広告リンクなしで公開用登録済み）
- 3本目: `drafts/specialized-vs-general-agents.md` → `public/articles/specialized-vs-general-agents/index.html`（広告リンクなしで公開用登録済み）
- 両方とも公式一次情報6件を参照し、出典番号・免責文・未公開設定をチェック。広告リンクなし。
- 2本目・3本目は公式情報を再点検して `public/` に配置済み。ただしCloudflare上の実表示は未確認。
- お問い合わせ窓口: `erabichizu.contact@gmail.com` を運営者情報・プライバシーポリシーに掲載済み。利用者が送受信確認済み。

## 2026-11-03 サイト更新
- 記事2・3本目を `public/articles/` に追加、トップページと記事一覧からリンク
- サイトマップを全8ページに更新
- `public/about/index.html` と `public/privacy/index.html` に専用メールアドレスを掲載。送受信できることを利用者が確認済み
- 各公開用HTMLに免責文と記事一覧への導線を配置
- 広告主との提携・広告リンク設置は未実施。今後のAI記事の自動公開も未設定
- Cloudflare上で更新後のページが閲覧できるかは未検証（ユーザーのブラウザでの確認が必要）
