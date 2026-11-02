> 2026-11-02 v0.12：一般種9PNGはユーザー採用済み。`later-wild-model-check_v0.1.json`で台帳49件・採用済みruntime19枚・新設定画3枚の表示と旧6肢案の不採用を確認。`resume-validation_v0.11.json`は採用前に再検証した履歴。以下は当時の状態。

> 最新：一般種3体の設定画をユーザーが採用し、個別PNG候補9枚を追加。`early-wild-sprite-geometry_v0.1.json`で画像規格、`early-wild-sprite-browser-check_v0.1.json`で表示、`early-wild-sprite-rebuild-check_v0.1.json`で新9枚の再現性と既存御三家出力の互換性を確認。新9枚の見た目は確認待ち。採用済みPNGは従来の10枚。以下は経緯。

> 最新：御三家初期3体の静止素材9枚＋UI枠1枚が採用済みへ更新。一般種3体（リスコロ・ツルモグ・ハネリ）の設定画案を追加し、`early-wild-model-check_v0.1.json`で表示と採用状態を確認。新設定画の背面・横面はユーザー確認待ち。以下は経緯。

> 最新：ホノル・ミオマルの設定画から個別PNG候補6枚を追加。幾何は`starter-sprite-geometry_v0.1.json`、比較・選択・採用済みUIの不変は`starter-sprite-browser-check_v0.1.json`で確認。採用済み4PNGと、見た目確認待ち6PNGを区別する。以下は経緯。

> 最新：戦闘UI v0.1の見た目をユーザーが採用し、runtime PNGはハナミミ3点＋UI枠1点の計4点。ホノルの4肢案は不採用、独立した腕2・脚2・翼2へ修正した設定画v0.2とミオマルv0.1を追加。`starter-model-check.json`で表示・旧案の不採用ラベル・採用済みUI画像の不変を確認。新設定画の見た目は未確認。以下は経緯。

> 最新：ハナミミ静止素材3点はユーザー採用済み。参考画面へ寄せたひらがな戦闘UI案を追加し、ローカル字体・文字なし枠・表示を`battle-ui-check.json`で確認。表示画像は`battle-ui_v0.1.png`。全素材や実機の完成を表すものではない。以下は過去の経緯。

> 最新：ハナミミの個別候補3点（96px・96px・32px）をコードで出力。幾何検査は`hanamimi-sprite-geometry.json`、ブラウザ検査は`hanamimi-sprite-browser-check.json`。比較画像は`hanamimi-sprites_v0.1.png`、戦闘配置は`battle-composition_v0.2.png`。以下の0件・6件・8件という記載は以前の検査記録。

> 最新の追加確認：ハナミミ設定画の形と戦闘の向きをユーザーが採用。向き修正版・ドット絵風試作を追加し、実ファイル台帳8件の照合と企画整合検査が成功。`battle-orientation-check.json`と`battle-composition_v0.1.png`が今回の確認記録。以下の6件・5原画の記述は前回検査時点の記録。

# 2026-11-02の確認結果

- `validation.json`：実ファイル6件の存在・SHA-256・PNG寸法が一致。骨格の156枠、8地域、8代表、クリア後2地域、制作カード15体、御三家の進化6リンク、BGM計画28件が整合。JavaScriptの構文確認成功。
- `validate_assets.py --require-complete`：終了コード1。全素材・コンテンツの未完成を検出した想定どおりの結果。成功した検査と混同しない。
- `viewer-check.json`：導入済みChromiumをPlaywrightから起動して11項目成功。5原画の切り替え、制作候補の寸法・透明域・外周、4倍表示、背景切り替え、全透明PNGと偽PNGの検出、390px幅での横はみ出しなし、例外なし、外部リクエストなし。
- `asset-review_desktop.png`・`asset-review_mobile.png`：1440px幅と390px幅で取得した表示記録。実機のスクリーンショットではない。

ブラウザ検査の寸法用PNGは一時的な合成テスト図形。制作素材へは登録していない。Playwright既定のブラウザは未導入だったため、環境に既存の`/usr/bin/chromium`を使った。ページの横はみ出しを修正した後に検査を再実行している。

元ZIPの全画像とHANDOFF・企画原本はバイト一致を確認。更新した既存ファイルは入口のREADME・CLAUDE・START、docsの台帳への追記、実ファイル台帳の5件のみ。ローカルMarkdownリンクも照合済み。

これは素材準備と確認ツールの検査。本体、バランス、20～30／50時間、音声再生、iPhone・Android実機、オフライン、セーブ、GitHub push、Claude Codeクラウド実行は未検証。
