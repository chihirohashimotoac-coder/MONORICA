# MONORICA：GitHub正本でのクラウド作業

更新日：2026-11-04（日本時間）

全156種の文字設計レビューを実施した最新の結果は[SPECIES_REVIEW_v0.1.md](../SPECIES_REVIEW_v0.1.md)と[実検査記録](../../reports/species-review-validation_2026-11-04.json)に保存する。初期登録時の46項目は過去の結果。今回の検査器は52項目で、追加理由と実行結果は最新レポートを参照する。

## 現在の正本と参照

- 正本：https://github.com/chihirohashimotoac-coder/MONORICA
- 初期登録ブランチ：`work/preproduction-v013-import`
- 初期登録コミット：`c15d5bf661265d54f7cc61b651ee7884e74b6537`
- 再開ブランチ：`work/species-review-v013-20261103`
- 最新の停止位置：[LATEST_HANDOFF.md](../../LATEST_HANDOFF.md)
- 全要件：[今回の作業指示書](../requests/MONORICA_Work_GitHub_prompt_v0.1.md)

ユーザーが元ZIPをコミット66d12e7bdb19fdebd0f7dd4896b9f29c1a2cebf7へアップロードした。GitHubからクラウドへ取得し、元SHA-256と一致、217ファイルを実測・安全に展開した。PNGとフォントを含む全217ファイルを一切省略せず初期登録した。実行の一時チェックアウトはクラウドのみで、PC内の作業フォルダーやOneDriveには依存しない。

過去のDrive取得ホスト制限は初期登録の阻害ではなくなった。過去の経緯は旧Handoff・取得レポートを履歴として保持する。次回は展開済みGitHubファイルから開始し、DriveのZIPを再取得する工程へ戻らない。

## 開始方法

1. GitHubの最新参照・PRと、上記の再開ブランチの最新コミットを確認してクラウドへチェックアウトする。mainは展開済み資料を含んでいないので、再開ブランチを明示する。
2. AGENTS.md、CLAUDE.md、LATEST_HANDOFF.md、リンク先Handoff、docs/DECISIONS.mdと今回の指示書を読む。
3. 指示書「2. 読む資料」を本文で確認する。資料の存在確認・構造検査の成功を、156種の内容レビューや画像目視の実績へ読み替えない。
4. 生成元はtools/species_drafts_v01.pyとtools/build_species_catalog_v01.py。制作案の変更は生成元へ反映し、JSON・CSV・Markdownを再生成する。

## 検査と保護

今回、クラウドで実行した4コマンドはいずれも成功した。初期取り込み時の詳細は [初期登録レポート](../../reports/github-initial-import_2026-11-03.json)、運用指示更新後の結果は [移行検査レポート](../../reports/github-migration-validation_2026-11-03.json)。カタログ46項目成功、素材台帳49件、runtime19PNG、既存15種カードを確認した。バランス・面白さ・通しプレイ、全156種の内容レビューは未実施。

```text
python tools/build_species_catalog_v01.py
python tools/validate_species_catalog_v01.py
python tools/validate_assets.py
python tools/validate_preproduction.py
```

元202ファイルのハッシュ検査を維持する。運用文書の正当な更新例外はAGENTS.md・CLAUDE.md・docs/SESSION_CONTINUITY.mdと、従来からのLATEST_HANDOFF.md・README.md・docs/DECISIONS.mdに限定し、検査レポートへ対象と理由を出す。assets/・brief/・manifests/・元content/の保護は変更しない。

元のv0.13検査レポートに含まれるWindows作業・資料読了・画像目視の記述は過去の実績。更新した検査器は存在確認と読了・目視を分け、今回の実績へ流用しない。初期登録時の検査項目数は46。

## 終了と再開

変更・実検査・未決事項・次の一手を作業ブランチへコミット・pushし、GitHubから最新SHA・主要ファイル・PRのbase/headを再確認する。Handoff自身を含むSHAは最終報告で示し、自己参照だけのコミットを繰り返さない。

mainへの直接コミット・直接push、force push、履歴置換、PRマージ、画像生成、ドット制作、ゲーム本体実装、公開・デプロイは行わない。新規141種と既存種への詳細追加は制作案のまま。採用済み19PNG・既存15カード・12属性表を保持する。

今回の停止位置と次工程はLATEST_HANDOFF.mdを確認する。全156種の文字レビュー後は、設定画・数値設計・試作の各工程を、ユーザーの最新依頼に合わせて選ぶ。

## 次セッション用開始文

[NEXT_SESSION_START_2026-11-04_REVIEW.txt](../../NEXT_SESSION_START_2026-11-04_REVIEW.txt) を使用する。ZIPの再アップロードは不要。
