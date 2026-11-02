# Handoff：GitHub移行準備・資料ZIP取得待ち

更新日：2026-11-02（日本時間）

## 再開情報

- リポジトリ：https://github.com/chihirohashimotoac-coder/MONORICA
- 作業ブランチ：`work/github-migration-preflight-20261102`
- ベース：`main`
- 今回の作業元コミット：`32680058a1d4f66a37e9fb2eb07832f5c6e29623`
- 指示書・運用手順・検査阻害記録を保存したコミット：`7216013340ce0b4b4ef28ffc18df95e197cf6f21`
- Draft PR：https://github.com/chihirohashimotoac-coder/MONORICA/pull/1
- このHandoffを含む最終コミットSHAはチャットの最終報告を参照。GitHubで作業ブランチの最新SHAを再取得して再開する。

## 確認できた事実

開始時のGitHubにはmainが存在し、既存コミットはルートコミット `32680058a1d4f66a37e9fb2eb07832f5c6e29623`（Initialize repository）。再帰ツリーは空の.gitkeepだけで、ブランチはmainのみ、PRは0件。前セッションの「ブランチ0本」から状態が変わっていた。書き込み権限あり。mainは更新していない。

ユーザーが今回の作業指示として明示した添付Markdownを取得し、原文を [../requests/MONORICA_Work_GitHub_prompt_v0.1.md](../requests/MONORICA_Work_GitHub_prompt_v0.1.md) に保存した。SHA-256は `ad16d71d9925702f6609deabf32ff049859bd547122697693af9a3cce29603ce`。

添付ZIPは download_file の `file exceeds the executor transfer limit of 32 MiB` により取得できなかった。実際のZIP内容、217件の実測、元ZIPのSHA-256は未確認。指示書内Libraryリンクだけを取得成功として扱っていない。利用可能な別のファイル取得機能は見つからず、PCブラウザーには切り替えていない。

クラウドの一時チェックアウトを使用した。Git CLIのリモート通信はproxy:8080へ接続できず失敗したが、接続済みGitHub機能でリモートの参照確認・作業ブランチ作成・コミット保存・Draft PR作成はできた。CLIのpush成功とは報告しない。PC内の作業フォルダー、OneDriveには依存していない。

## 実検査と限界

クラウドで指定の4コマンドの実行を試みた。

| コマンド | 結果 |
| --- | --- |
| python tools/build_species_catalog_v01.py | exit 2：ファイル不在、開始不可 |
| python tools/validate_species_catalog_v01.py | exit 2：ファイル不在、開始不可 |
| python tools/validate_assets.py | exit 2：ファイル不在、開始不可 |
| python tools/validate_preproduction.py | exit 2：ファイル不在、開始不可 |

詳細は [../../reports/github-migration-preflight_2026-11-02.json](../../reports/github-migration-preflight_2026-11-02.json)。保存したJSONの構文と指示書原文のハッシュはクラウドで確認した。前版の46項目成功は流用していない。構造検査の成功件数は0で、ゲームのバランス・面白さ・通しプレイも未検証。

## 未完了

資料ZIP内のAGENTS.md、CLAUDE.md、旧LATEST_HANDOFF.md、リンク先Handoff、docs/DECISIONS.md、指示書「2. 読む資料」の全資料、採用画像・フォント等は取得できておらず未読。

初期登録、全156種レビュー、生成元の修正、JSON・CSV・Markdownの再生成、設計レビュー記録、既存運用指示の統合更新、本来の設計レビューPRは未実施。このDraft PRは移行準備のみ。新規制作案や検証済みのゲーム設定は作成していない。

## 次の一手

1. 元ZIP全体を30 MiB以下へ分割した全パートを取得する。クラウドで連結し、期待SHA-256 `548d7c87d5b0fad25a8a179ded85f9607ca41406bc37768cb4b2cfcaf031235c` と照合する。ハッシュ不一致なら相違を報告して止める。
2. GitHubの最新参照・main・この作業ブランチ・PRを再確認する。安全に展開して217ファイルを実測し、PNG・フォントを省略せず、既存内容を比較・保持して初期登録用ブランチへ保存する。
3. 本準備差分の同名Handoff等は、ZIP内の原本と比較して統合する。AGENTS.md・CLAUDE.md・docs/DECISIONS.mdは原本を読んで今回のGitHub正本方針へ更新する。
4. 今回の指示書の全条件を維持して、156種の具体的な問題特定から生成元の修正・再生成・実検査まで進める。採用済みと制作案を区別する。
5. 作業ブランチへコミットしてGitHubに保存し、主要ファイル・最新SHAをGitHubから読み直す。実在するベースで設計レビューPRを作成し、最新Handoffへ引き継ぐ。

[GitHubからの開始・終了手順と次セッション用開始文](../operations/GITHUB_WORKFLOW_v0.1.md) を参照。main直接更新・force push・マージ・画像生成・ゲーム実装・公開・デプロイは行わない。
