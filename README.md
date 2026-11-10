# えらびの地図｜アフィリエイトサイト運営（Affiliate Autopilot）

## 現在の状態（2026-11-10）
- 公開サイト: https://affiliate-autopilot-3ja.pages.dev/
- GitHub: https://github.com/nobotasuke-byte/affiliate-autopilot
- サイト名: えらびの地図 / サイト内運営者表記: えらびの地図編集室（法人名ではない）
- 公開用HTML: `public/`（Cloudflare Pagesがmainのpublicを配信）
- 記事: **5本を公開用ディレクトリに登録**（個別のCloudflare配信表示は今回未確認）
- A8.net: 2026-11-03にhape Agent（ID `s00000025290001`）への提携申請済み。2026-11-10に利用者から「まだ承認されていない」と報告
- 広告リンク: **未設置**。広告提携が承認され、媒体・対象記事と掲載条件を点検するまでは設置しない
- 問い合わせ先: erabichizu.contact@gmail.com（運営者情報・プライバシーポリシーに掲載。ユーザーが送受信確認済み）
- GitHub Actionsの自動生成: 毎週月曜10:17 JSTにGitHub SecretsのGeminiキーを使用して**下書きのみ**作成、`drafts/`と`evidence/`へ保存。**公開は自動実行しない**
- 2026-11-09のGitHub Actions定期実行: 外部HTTP 503で失敗。2026-11-10にHTTP 429/500/502/503/504の最大3回再試行を追加。**修正後の実動作は未検証**

## 公開用記事
| 順番 | タイトル | 公開用パス |
|---|---|---|
| 1 | 20代の営業職が転職エージェントを選ぶときの5つの確認ポイント | `public/articles/20s-sales-agent-checklist/index.html` |
| 2 | 営業職から異業種へ転職する際の注意点と準備 | `public/articles/sales-to-other-industry/index.html` |
| 3 | 営業職専門と幅広い職種を扱う転職エージェントの違い｜比較の6つの観点 | `public/articles/specialized-vs-general-agents/index.html` |
| 4 | 仕事やキャリアを見直すときに活用できる公的な情報ツール | `public/articles/career-tools-guide/index.html` |
| 5 | 転職サイトと職業紹介サービスの違い――応募する側が知っておきたいこと | `public/articles/job-info-vs-placement/index.html` |

## 記事4と5の引き継ぎ
- 2026-11-10、利用者から「4本目・5本目を別の生成AIで下書きから公開まで進めた」旨の申告
- GitHubで確認した時点では、4本目は公開用ファイルにあり、5本目は `drafts/job-info-vs-placement.md` のみ存在し、記事一覧と公開用ディレクトリに5本目がない状態だった
- 4本目は元の公開用記事を変更せず継続利用
- 5本目は元原稿を保存してから、ハローワークによる紹介と直接応募の再就職手当上の扱いを正確化。確認不能なスカウト例を削除し、第三の一次資料を追加してから新たに公開用HTMLに配置
- 5本目の編集確認記録は `evidence/job-info-vs-placement-editorial.json`
- **旧 `evidence/job-info-vs-placement.json` はAI初回生成時点の根拠データであり、編集後の全文の正しさを証明しない**
- 4本目の `evidence/career-tools-guide.json` もAI初回生成時の引用照合データであり、後日の追加編集を含む全文の意味的検証結果ではない

## 安全性・公開手順
1. 調査・下書きはどのAIで作ってもよいが、必ずGitHubの同一リポジトリを最新版とする
2. 公開前に一次情報のURL到達性、記事の主張と出典の対応、制度・数値・料金の鮮度、誇張・比較表現、著作権を確認する
3. AIが出典原文の一部を引用できることは、本文すべての意味が正しい証明ではない。必要なら人による追加確認を行う
4. アフィリエイト広告を追加するときは提携状況・成果条件・禁止事項・「広告」「PR」の表示・プライバシーポリシー・リンクテストを確認する
5. 公開用 `public/` は明示的な編集判断で更新する。自動下書きと自動公開を混同しない
6. 別のAI・人が同時に同じファイルを上書きすると競合するため、編集の順序を管理する
7. Google検索等へのインデックス登録、Cloudflareの配信状況、検索流入や収益の発生はコード上の設定のみでは証明できない
8. リポジトリはPublic。GitHub SecretsのAPIキーをソースに書かない

## 免責文（全記事に配置）
当サイトに掲載される情報は、正確性・完全性を保証するものではなく、内容を利用することで生じた損害について、当サイト運営者は故意または重過失がある場合を除き責任を負いません。

## 次の作業
1. 5本目のCloudflare公開表示をユーザー画面で確認
2. A8.netでhape Agentが承認されたら適用範囲・広告リンク・PR表示を実装
3. GitHub Actionsの通信再試行が実動作するか検証
4. 新規記事はテーマと収益導線を評価し、サイト内の過度な重複を避けて企画
