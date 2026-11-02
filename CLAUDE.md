# MONORICA：現在の制作段階

日本語で相談・報告する。素材とデータを先に整え、GitHubのリポジトリからClaude Codeクラウドへ本格実装を引き継ぐ。今は素材準備と表示確認の段階。ユーザーが本体実装を依頼するまで、Phaser等のゲーム本体・戦闘・セーブを実装しない。
既存チェックアウトで作業し、明示的な依頼がなければGit worktreeを作らない。旧資料のWindowsローカル実装開始手順へ戻さない。ユーザーの最新指示を優先する。

## セッション継続のユーザー希望

コンテキスト量が多くなってきたら、毎回こちらからHandoffと必要な成果物を保存し、新しいセッションへ移るよう案内する。ユーザーの依頼を待たない。作業途中の結果を回収し、安全な区切りで切り替える。正確な利用率が不明なら数値を捏造しない。
詳細はAGENTS.mdとdocs/SESSION_CONTINUITY.md。最新の入口はLATEST_HANDOFF.md。アカウント全体のメモリへ書き込んだという意味ではなく、このプロジェクト内で継続するための指示である。

## 最初に読む

1. LATEST_HANDOFF.mdとdocs/DECISIONS.md：最新の停止位置、次の一手、採用と保留。今回の新しい確認対象はdocs/LATER_WILD_MODEL_SHEETS_v0.1.mdのミズッタ・ココイル・ヨルミルの設定画。ヨルミルは四肢へ修正したv0.2を使い、旧6肢案v0.1は不採用。
2. docs/BATTLE_UI_v0.1.md：見た目採用済みの戦闘UIとひらがな表記。
3. docs/EARLY_WILD_SPRITES_v0.1.md：リスコロ・ツルモグ・ハネリの個別候補9枚。モデルの経緯はdocs/EARLY_WILD_MODEL_SHEETS_v0.1.md。docs/STARTER_SPRITES_v0.1.md：採用済みのホノル・ミオマル静止素材。
4. docs/HANAMIMI_SPRITES_v0.1.md：ハナミミの静止素材3点。
5. docs/WORLD_OUTLINE_v0.1.md、docs/STORY_CONFLICT_B_v0.1.md：全体の骨格とBの具体化。
6. docs/ASSET_SPEC_v0.1.md、manifests/assets.json：画像規格案と実ファイル。
7. docs/GITHUB_CLAUDE_HANDOFF.md：素材準備中／本格実装時の依頼を区別。

## 最新の採用状態

- 御三家初期3体（ハナミミ・ホノル・ミオマル）の前面96px・背面96px・アイコン32px、計9枚の見た目をユーザーが採用。画像規格も確認済みで9点はruntime_ready=true。実機・アニメーションの検証は別。
- 戦闘は味方が左下・右上向きの背面、相手が右上・左下向きの正面。
- 戦闘UIはユーザー提示のポケモン画面に酷似させる方向。操作案内はひらがなを基本にする。固有名・HP・Lv・数字は併用。
- 戦闘UI v0.1の具体的な枠・配置・字体・主コマンドの見た目もユーザーが採用。基準384×256の最終実機対応は今後検証する。枠PNGへ名前や数値を焼き込まず、content/ui/の文言と配置を分離する。採用済みUI枠はassets/runtime/ui/battle/frame.png。採用済みruntime PNGは御三家初期3体の9点＋一般種3体の9点＋UI枠1点の計19点。一般種3体の設定画に続き、ドットPNG9枚もユーザーが「3体ともこのまま採用」と回答。runtime_image_countとruntime_ready_image_countはどちらも19。後続3体の新設定画は確認待ち。sourceの高解像度原画をruntime枚数へ数えない。
- 無料のDotGothic16をローカル同梱。フォントの著作権表示とOFL全文を保持。
- ユーザーは、元画像を残してコードで切り出し・減色・透過整理・サイズ調整を行うことも委任済み。定型の仕上げ工程を再確認しない。採用原画は変更せず、出力や変更案は別ファイルにする。

## ゲーム全体で引き継ぐ条件

- 156種・本編8地域／代表8人・クリア後2地域の規模で骨格案を進める。個別の地域名・人物・全系統・能力値は提案を区別。
- 対立側はB「企業内の一部責任者の隠蔽」を採用。企業全体や技術を悪者にしない。人物の具体像・外見・台詞は提案。
- 御三家の初期・最終と一般種6種の造形方向は採用済み。御三家の中間形は提案。ホノルはユーザーが「独立した腕2本・脚2本・翼2枚」を選択。6肢構造を採用し、腕と翼を兼ねる4肢案は不採用。提示したホノル設定画v0.2とミオマル設定画v0.1を基準に進めるよう指示され、個別PNG6枚へ展開した。6枚の比較と戦闘表示に対してユーザーが「完璧です」と回答し、見た目も採用済み。ID内のwyvernを理由に4肢へ戻さない。
- 御三家はLv16と36で進化。他の2系列はクリア後に一人で入手。必須探索技は通常種からも、それを使う地点より前に入手できるようにする。
- 探索技は戦闘の4技枠を使い、実際に覚えた個体を手持ちに入れる。別枠へ変更しない。
- 12属性と相性表は試作用に採用済み、最終バランスは未検証。表はcontent/type-chart.jsonを使う。
- 穏やかな序章、森の小さな異変の後にカザミ町代表戦、幼なじみと決勝に立つ約束と焦り、希望のある結末を維持。
- 全種の一人用入手、端末内セーブ、スマートフォン横持ち、オフラインの方針。本編20～30時間、主要な後日要素込み約50時間を目標とし、未測定と区別。
- 追加素材購入・外注予算0円。既存のChatGPT Plus・Claude Pro・Suno Proを使い、別料金の従量APIへ勝手に切り替えない。実音源はまだ0曲。

## ファイルと検証

content/planning/は制作カードと見積もりで、完成した戦闘データではない。tools/asset-review/は素材とUIの確認用で、ゲーム本体ではない。
python3 tools/validate_assets.py と python3 tools/validate_preproduction.py を実行する。--require-completeは全素材が未完成の現在は失敗するのが正しい。
ハナミミを再書き出す場合はtools/prepare_hanamimi_sprites.py、ホノル・ミオマルはtools/prepare_starter_sprites.pyとcontent/starter-art-export-profiles.jsonを使う。一般種3体はtools/prepare_early_wild_sprites.pyとcontent/early-wild-art-export-profiles.jsonを使う。画像処理の依存はtools/requirements-art.txt。既存の出力が手修正されていれば上書きしない。
実行していない検査や、GitHubへのpush・公開・Claudeクラウド実行を実施済みと報告しない。古いreports内の候補・未採用は、その検査時点の記録。現在の状態はDECISIONSと実ファイル台帳を優先する。
