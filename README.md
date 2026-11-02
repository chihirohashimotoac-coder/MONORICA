# MONORICA：ゲーム企画と素材準備

2026-11-03：GitHubを正本とする初期登録を完了。再開ブランチは `work/species-review-v013-20261103`。[最新Handoff](LATEST_HANDOFF.md)・[GitHub運用手順](docs/operations/GITHUB_WORKFLOW_v0.1.md)・[今回の実検査](reports/github-initial-import_2026-11-03.json)から再開する。以下のv0.13以前のGit未実施・PC内フォルダー指定は履歴。156種の内容レビューは次工程で、今回完了した構造検査とは区別する。

2026-11-02 v0.13：**全156種の詳細設計案を作成**。[図鑑一覧](docs/SPECIES_CATALOG_v0.1.md)・[日本語詳細](docs/SPECIES_DESIGN_DETAILS_v0.1.md)・[設計JSON](content/planning/species-catalog_v0.1.json)・[設定画バッチ](docs/SPECIES_ART_BATCHES_v0.1.md)・[検査結果](reports/species-catalog-check_v0.1.json)を参照。追加内容は制作案で、新しい美術やゲーム仕様を採用済みへ変更していない。次は設計レビュー。画像生成・ゲーム実装・公開は今回行わない。

2026-11-02 更新。素材を先に整え、展開済みファイルをGitHubからClaude Codeクラウドへ渡す。
現在は制作途中。展開済み資料のGitHub登録と今回の構造検査は完了。ゲーム本体の実装・全素材完成・Claudeでの本体実行は未実施。

## 次のセッションへ

最新の引き継ぎは[LATEST_HANDOFF.md](LATEST_HANDOFF.md)、開始文は[NEXT_SESSION_START_2026-11-03_GITHUB.txt](NEXT_SESSION_START_2026-11-03_GITHUB.txt)。旧版の開始文は履歴として保持する。
コンテキストが増えたら毎回Handoffを作成し、新しいセッションへ移るよう案内するユーザー希望を、[AGENTS.md](AGENTS.md)と[継続ルール](docs/SESSION_CONTINUITY.md)へ保存した。アカウント全体のメモリ登録ではない。

## 今回から読む入口

- [ミズッタ・ココイル・ヨルミルの新設定画案](docs/LATER_WILD_MODEL_SHEETS_v0.1.md)
- [今回の決定と保留事項](docs/DECISIONS.md)
- [8地域・代表・章・系統の骨格案](docs/WORLD_OUTLINE_v0.1.md)
- [B採用後の人物・物語・素材案](docs/STORY_CONFLICT_B_v0.1.md)
- [序盤一般種3体の96px前後・32pxアイコン候補](docs/EARLY_WILD_SPRITES_v0.1.md)
- [序盤一般種3体の前後横の設定画](docs/EARLY_WILD_MODEL_SHEETS_v0.1.md)
- [ホノル・ミオマルの96px前後・32pxアイコン](docs/STARTER_SPRITES_v0.1.md)
- [ホノル・ミオマルの前後横の設定画案](docs/STARTER_MODEL_SHEETS_v0.1.md)
- [参考画面に寄せた戦闘UIとひらがな表記](docs/BATTLE_UI_v0.1.md)
- [ハナミミの96px前後・32pxアイコン](docs/HANAMIMI_SPRITES_v0.1.md)
- [採用した戦闘構図と素材の向き](docs/BATTLE_COMPOSITION_v0.1.md)
- [素材規格と最初の確認セット](docs/ASSET_SPEC_v0.1.md)
- [ハナミミ設定画案と次の画像制作指示](docs/prompts/FIRST_ART_BATCH_v0.1.md)
- [全素材の制作量](docs/PRODUCTION_ESTIMATE_v0.1.md)
- [Sunoの制作指示](docs/AUDIO_PRODUCTION_v0.1.md)
- [GitHub・Claudeクラウドへの引き継ぎ手順と依頼文](docs/GITHUB_CLAUDE_HANDOFF.md)

156種・本編8地域／代表8人・クリア後2地域で骨格案を進める規模を採用。対立側はB「一部責任者の隠蔽」を採用。個別の地域・人物の具体像や外見・種族の詳細は提案。
御三家初期3体9枚・一般種3体9枚・戦闘UI枠1枚の計19PNGは、すべて見た目採用・画像規格確認済み。ミズッタ・ココイル・ヨルミルの前後横の新設定画は確認待ち。台帳49件。全素材は未完成、音源0曲。

```sh
python3 tools/validate_assets.py
python3 tools/validate_preproduction.py
```

原画・設定画と制作候補の寸法・透過・余白を確認する[素材確認帳](tools/asset-review/README.md)も同梱。Python標準のHTTPサーバーだけで起動できる。

## 引き継いだ資料パックの説明（経緯）

# モンスター育成RPG：クラウド開発の素材準備

このパックはGitHubへ登録するための資料・参照原画・素材台帳の初期構成です。全素材完成版やゲーム本体ではありません。

現在は素材先行の準備段階です。先に[制作手順](brief/17_cloud_asset_first_workflow_v0.1.md)と[全素材台帳](brief/18_asset_inventory_v0.1.md)を読んでください。

1. 全体のコンテンツ一覧と素材規格を決める。
2. 少数の素材で規格を確認する。
3. 本編・クリア後の素材とデータを制作する。
4. ファイルを照合し、一式をGitHubにそろえる。
5. Claude Codeクラウドで本格実装を開始する。

GitHubには、このZIPを展開したファイル構成で登録します。素材制作の途中から登録しても構いません。
まだGitHubリポジトリの作成・アップロード・Claude Codeでの実装は実行していません。

記録したファイルを確認するコマンド：`python3 tools/validate_assets.py`
全素材がそろった条件も含めるコマンド：`python3 tools/validate_assets.py --require-complete`
後者は、現在は未制作カテゴリがあるため失敗するのが正しい状態です。
