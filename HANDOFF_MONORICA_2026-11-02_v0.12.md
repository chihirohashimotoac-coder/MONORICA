# MONORICA Handoff v0.12

2026-11-02（日本時間）。v0.11は経緯として保持。最新のユーザー回答・本書・docs/DECISIONS.md・manifests/assets.jsonを優先する。

## 今回の採用と停止位置

リスコロ・ツルモグ・ハネリの前面96px・背面96px・アイコン32px、計9枚を提示後、ユーザーが**「3体ともこのまま採用」**と回答。台帳・制作キュー・制作カード・プレビュー・現在の案内を採用済みへ更新した。御三家9枚＋一般種9枚＋UI枠1枚で、runtime PNG19枚すべてが採用済み。

続いてミズッタ・ココイル・ヨルミルの前後横の設定画案を制作・提示した。**新しい設定画3枚への採用回答はまだ。** 元の6体比較原画の造形方向は採用済みだが、新しい背面・横面・接続の採用とは区別する。

次はこの3枚への回答を確認する。回答がなければ見せて確認。採用されたものだけ台帳・キュー・制作カードを更新し、前後96px・アイコン32pxへ展開する。新しいドット画像の見た目はその後に確認する。「続行」を採用回答に読み替えない。

## 新しい確認対象

詳しくは[後続3体の設定画](docs/LATER_WILD_MODEL_SHEETS_v0.1.md)。左から斜め前・斜め後ろ（右上向き）・左向き横面。

| 対象 | ファイル | RGB PNG実寸 | 確認点 |
|---|---|---|---|
| ミズッタ | assets/source/monsters/wild_stream_otter_01/model_sheet_v0.1.png | 1983×793 | 長く低い胴、四肢、1本の平たい尾と水紋 |
| ココイル | assets/source/monsters/wild_coil_dormouse_01/model_sheet_v0.1.png | 1983×793 | 1本につながる渦状の尾、銅色3帯と水色3帯 |
| ヨルミル | assets/source/monsters/wild_dusk_glider_01/model_sheet_v0.2.png | 1922×818 | 前脚2・後脚2、飛膜が手首から足首へつながる |

ヨルミル初回v0.1（1923×818）は、膜端の後脚とは別に腹下へ小さい脚が追加され6肢に見えたため不採用。内蔵画像生成で余分な脚を取り除いたv0.2を保存した。旧案はsourceと台帳へrejected_anatomy_supersededとして保持し、素材確認帳でも不採用と表示。今回の確認対象はv0.2のみ。古い比較原画の小器官を根拠に6肢へ戻さない。

新設定画は高解像度・白地の参照資料であり、透過済み96pxスプライトではない。戦闘前面の左下向きへの調整は個別素材の書き出し時に行う。生成・修正指示はdocs/prompts/へ保存。元の比較原画と既存リスコロ設定画を参照し、別料金の外部APIは使用していない。

## 現在の範囲

- 台帳49件（前版45件＋新設定画3件＋不採用旧案1件）。新設定画3件はreference_only・model_sheet_visual_review_pending・runtime_ready=false。
- runtime_image_count=19、runtime_ready_image_count=19。個別PNGがあるのは御三家初期3体と一般種先行3体の6体。全9体のruntime素材ができたわけではない。
- catalog_complete=false、full_content_data_complete=false。全156種の詳細・技・道具・人物・地形・会話などは未完成。音源0曲、Suno指示のみ。
- 本体実装、戦闘、セーブ、PWA、実機、プレイ時間は未検証。今は素材・データを先に整える段階。

## 実検査と再現

チェックアウトは/workspace/MONORICA。Python 3.12、Pillow 12.3.0、Playwright、/usr/bin/chromiumを確認した。

```sh
cd /workspace/MONORICA
python3 tools/validate_assets.py
python3 tools/validate_preproduction.py
```

両検査成功。49件の存在・SHA-256・PNG寸法、runtime19／採用19、企画参照・件数が整合。JavaScript構文確認も成功。--require-completeは未制作カテゴリを検出して終了コード1になることを区別する。

reports/later-wild-model-check_v0.1.json：新設定画3枚と旧不採用案の選択・寸法・参照表示、6体の採用ラベル、幅390pxの横はみ出しなし、戦闘配置3組、ページ例外・失敗レスポンス・外部HTTP要求なし。従来のハナミミ戦闘UIはreports/battle-ui_v0.1.pngと画素一致。既存assets・brief計80ファイルはSHA-256不変。

初回のブラウザ検査は画像だけの選択欄に全台帳49件を期待して停止。PNG42件へ待機条件を修正。続く検査はローカルblob URLを外部HTTPと誤分類して記録前に停止。分類を修正し全項目を再実行・成功。これらは検査側の修正で、アプリ不具合とはしない。

reports/riscoro-sprites_v0.2.png、tsurumogu-sprites_v0.2.png、haneri-sprites_v0.2.pngは採用済みラベルの新表示記録。v0.1の画像・JSONは当時の履歴として保持。

必要時はルートで python3 -m http.server 8765 --bind 127.0.0.1 を起動し、内部ブラウザから/tools/asset-review/等を確認する。プロセスの継続を仮定しない。localhostを公開プレビューとして案内しない。環境ドラフトへinstall_script・start_skillを保存したが、Publishと新タスクでの復元成功は未確認。

## 維持する条件・継続ルール

詳細はAGENTS.md、CLAUDE.md、docs/DECISIONS.md、前版v0.11。日本語で相談。156種／本編8地域・代表8人／クリア後2地域、対立側B（一部責任者の隠蔽）、希望のある結末、探索技が戦闘4技枠を使う条件を維持。ホノルの独立腕2・脚2・翼2も維持。

追加予算0円。原画保存とコードによる切り出し・減色・透過整理・サイズ調整は委任済み。新しい美術の採用は別。採用済みの御三家・UI・先行一般種9枚の方向を聞き直さない。

コンテキストが多くなったら毎回Handoffと成果物を保存し、こちらから新しいセッションへ案内する。AGENTS.mdとdocs/SESSION_CONTINUITY.mdを参照。アカウント全体のメモリ登録ではない。

## Gitと次回への受け渡し

対象chihirohashimotoac-coder/MONORICA。ブランチwork、HEADコミットなし、ファイルは未追跡。commit・push・デプロイ・公開・Claudeクラウド実行はしていない。このチャット初期のGit読み取りは成功したが参照なし。今回の制作後にリモート最新状態は再照会していない。

最新素材はチェックアウトとZIPにある。空のGitHubへresetしない。明示依頼なしにworktreeを作らない。既存HTTPS Gitプロキシを使い、トークン変数の有無だけで新しい秘密値を要求しない。認証情報・.git・秘密値をZIPへ入れない。

別セッションへ本書、MONORICA_preproduction_v0.12.zip、NEXT_SESSION_START_v0.12.txtを渡す。ZIPの実ファイルを検証して再開し、空のリモートだけを見て素材がないと判断しない。
