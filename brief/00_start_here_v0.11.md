# 制作開始ガイド v0.11

## 今回の成果物

| ファイル | 用途 |
|---|---|
| [企画・仕様](01_game_design_draft_v0.11.md) | 相談で決まったこと、物語案、ルール、セーブ、完成基準 |
| [Claude Code用プロンプト](02_claude_code_prompt_v0.11.md) | 「プロンプト本文」以降を渡して制作を開始 |
| [AI素材制作の指示](03_ai_asset_workflow_v0.6.md) | ChatGPT画像生成・Suno Proと、Claude Codeの受け渡し |
| [物語・相棒の具体案](04_story_and_starters_proposal_v0.5.md) | 採用した事件・担当決定の動機、序章の会話、相棒3系列の案 |
| [全種の図像確認とデザイン再考](05_pokemon_design_research_v0.3.md) | 確認した範囲、抽出した方針、前案の変更点 |
| [確認範囲の記録](pokedex_review_coverage_v0.1.json) | 1,025種・1,321掲載画像と、比較した系列の記録 |
| [御三家の特別感と好み](06_starter_signature_design_brief_v0.2.md) | 初期形のかわいさ、最終形の迫力・華やかさと、新しい3候補 |
| [進化・名前・性格の計画](07_starter_evolution_plan_v0.1.md) | 採用した方向と、担当決定の名前、中間進化の案 |
| [中間進化の画像](starter_middle_concepts_v0.1.png) | 初期と最終の間をつなぐ3体。中間形は確認中 |
| [12属性の確定事項](08_type_system_draft_v0.2.md) | 12種類の名前・分類と、確定した倍率 |
| [戦闘・捕獲・全滅の最新ルール](09_battle_capture_defeat_rules_v0.1.md) | 今回確定した3方式。旧資料の未確定表記を更新 |
| [御三家の最新ルール](10_starter_playstyle_proposal_v0.2.md) | 役割・レベル16と36での進化・技枠使用・クリア後入手の確定を反映 |
| [探索技と採用した序章](11_field_moves_and_opening_v0.2.md) | 穏やかな旅立ちの採用と、技の使い勝手・帰還対策の案 |
| [最初の地域](12_first_region_proposal_v0.3.md) | 最初の大きな目標を町の代表戦へ確定。地図・一般種・編成の案 |
| [試作用の相性表](13_type_matchup_proposal_v0.2.md) | 144組を試作用に採用。JSON・CSVと構造確認の記録 |
| [採用した一般種6種](14_early_wild_creatures_v0.2.md) | A～Fすべての造形方向を採用。設定画・ドット素材へ仕上げる |
| [Claude Codeへの試作開始指示](15_claude_first_region_prompt_v0.2.md) | 村から代表戦・進化・保存後の再開までを作る具体的な指示 |
| [最初に貼り付ける短い指示](16_claude_start_message_v0.1.txt) | ZIPを解凍し、専用フォルダをClaude Codeで開いてから貼り付ける |
| [相棒の比較画像](starter_concepts_v0.4.png) | 初期・最終の造形方向を採用した6体。ゲーム素材の仕上げはこれから |
| [見下ろし型の参考画像](field_topdown_concept_v0.1.png) | 採用した2D方式を、より真上寄りの構図へ調整した画像 |
| [最初の比較画像](field_art_comparison_v0.1.png) | 上段3D・下段2Dを比較した経緯 |
| [見下ろし画像の生成指示](field_topdown_prompt_v0.1.txt) | 画像生成に実際に渡した全文 |

本体の実装、リポジトリ作成、プラグイン導入、公開は、このチャットではまだ実施していない。
仕様とプロンプトはv0.11の初稿で、Claude Codeへの投入試験は未実施。

## 使い方

1. game_brief_v0.11.zipを、新しい専用フォルダ（例：MonsterRPG）へ解凍する。中にSTART_HERE.md、START_CLAUDE.txt、briefフォルダができる。
2. Claude Codeで、その専用フォルダを開く。briefフォルダ自体をプロジェクトのルートにはしない。
3. START_CLAUDE.txtの内容を貼り付ける。15の具体的な開始指示と02の全体条件を読む指示になっている。
4. まず村の移動・会話・保存を動かし、捕獲・戦闘・進化・探索・代表戦へ順に進める。
5. ChatGPT用の画像生成指示やSuno用の音楽生成指示が出たら、各アプリで生成し、指定された場所へ保存してClaude Codeへ戻す。
6. 最初の地域を遊び、操作・見た目・進行で気になった点を具体的に修正する。本編全体の制作はその後も段階的に進める。

ChatGPTやSunoとの受け渡しは、実際の接続がない場合はユーザーが行う。
画像や音楽の完成を待つ間も、仮表示で独立したシステムを検証できる。仮表示を完成した美術として扱わない。
既存契約の利用枠に合わせて素材を段階的に作り、別料金のAPIへ切り替えない。

## 推奨プラグイン

このゲームには、まず以下の2つを候補にする。

| 名前 | 用途 |
|---|---|
| frontend-design | 図鑑・編成・設定・タッチ操作などのUI。採用したドット絵RPGの美術基準を優先する |
| playwright | ブラウザ操作、画面撮影、保存・再開・オフラインなどの確認 |

いずれもAnthropicの公式マーケットプレイスに掲載されている。
frontend-designはAnthropic製、playwrightはMicrosoftのブラウザ自動化MCPをまとめたプラグイン。
WindowsデスクトップではCode側のプラグイン管理で名前を検索する。
ターミナルの対話型Claude Codeを使う場合は次のコマンドを利用できる。

~~~text
/plugin install frontend-design@claude-plugins-official
/plugin install playwright@claude-plugins-official
~~~

マーケットプレイスが表示されない場合は、公式マーケットプレイスを追加する。

~~~text
/plugin marketplace add anthropics/claude-plugins-official
~~~

TypeScriptを採用した後は、typescript-lspも候補。

~~~text
/plugin install typescript-lsp@claude-plugins-official
~~~

このプラグインにはTypeScriptの言語サーバーも必要。Node.jsとnpmが使える環境で、次をシェルから導入する。

~~~powershell
npm install -g typescript-language-server typescript
~~~

最初から大量のSkillを入れる必要はない。
このプロジェクト固有の決定はCLAUDE.mdと仕様書へ残し、必要に応じてコンテンツ検査・セーブ検査の手順をプロジェクト用Skillへまとめる。
プラグインを使えることと、ゲームそのものが完成・検証されることは別なので、実行結果で確認する。

## 次にレビューする内容

物語の「新しい育成補助技術と地域の異変」は採用済み。幼なじみの動機は担当へ任され、約束を守りたい焦りとして決定した。
初期・最終の造形方向は採用済み。名前は担当へ任され、進化系列の作業名を決定した。
属性倍率・複合属性、捕獲方式、全滅方式は確定。最新の09を優先し、旧資料の未確定表記を読み替える。
御三家は草が速さ・特殊攻撃と回復、炎が高い攻撃、水が耐久・物理攻撃と反撃。3系列ともレベル16・36で進化する。
探索技は戦闘用4技の1枠を使い、他の御三家はクリア後に入手する。10のv0.2を優先し、旧資料の別枠案は採用しない。
12属性の名前と分類、穏やかな旅立ち型の序章も確定。08のv0.2と11のv0.2を優先する。
13の相性表は試作用に採用し、最初の大きな攻略目標は12の町の代表戦で確定。細かな編成や数値は試作で調整する。
14の一般種6種の造形方向も採用済み。15の段階Aから試作へ進む。技の数値、探索技の習得・帰還の細部、中間形の仕上げ、本編全体の内容は試作中も設計を続ける。
数式や全種の名前まで最初に固定せず、設定と試作を照らし合わせて調整する。

## 公式の参考先

- [Claude Code：プラグインの導入とデスクトップでの管理](https://code.claude.com/docs/en/discover-plugins)
- [frontend-design](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design)
- [playwright](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/playwright)
- [typescript-lspと必要な言語サーバー](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/typescript-lsp)

変更履歴：v0.1 初稿。画像方式・人物関係・クリア後の重点を反映。


変更履歴：v0.2 最新の仕様・プロンプトを参照し、物語・相棒の具体案と比較画像を追加。v0.1は過去版として残す。


変更履歴：v0.3 事件の方向と動機を反映。相棒原画と素材制作指示を更新し、最新ファイルへ案内を切り替えた。


変更履歴：v0.4 全種の公式図像確認とデザイン再考を追加し、新しい3系列候補と最新の仕様・プロンプトへ参照を更新。


変更履歴：v0.5 御三家の特別感、具体的な好み、新しい原画と最新の制作指示を反映。


変更履歴：v0.6 御三家の造形採用と中間進化、担当決定の名前、12属性案を追加。一式のZIPを用意。


変更履歴：v0.7 戦闘・捕獲・全滅の確定と、御三家の次の具体案を追加。


変更履歴：v0.8 御三家の役割・進化、探索技の4技枠使用、他の2系列のクリア後入手を反映。序盤の具体案を追加。


変更履歴：v0.9 12属性名と穏やかな序章を採用。相性表初稿・データと最初の地域の設計を追加。


変更履歴：v0.10 相性表の試作用採用、町の代表戦、一般種の比較画像、試作開始指示を反映。


変更履歴：v0.11 一般種6種の造形を採用。解凍→専用フォルダを開く→短い指示を貼り付ける手順へ整理。
