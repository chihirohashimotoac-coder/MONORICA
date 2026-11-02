> 2026-11-02 v0.12更新：一般種ドットPNG9枚も採用済みとなり、runtime PNG19枚すべてが採用済み。次はミズッタ・ココイル・ヨルミルの新設定画の確認。現在の採用状態はdocs/DECISIONS.mdと台帳を優先。以下の未採用の表現は当時の記録。

# GitHubからClaude Codeクラウドへ渡す

## 現在の位置

素材制作の途中。既存の引き継ぎ55ファイルを展開し、今回の骨格案・規格案・設定画案・制作キュー・音楽指示・確認ツールを追加した。ゲーム本体の実装や全素材の完成はまだ。

作業対象は`chihirohashimotoac-coder/MONORICA`。今回開始時のGitHub読み取りではリモート参照がなく、ローカルも未コミットだった。**今回の作業はローカルのファイル準備と検証まで。commit・push・公開・Claudeでの実行は未実施。**

## 先に見る順番

1. `LATEST_HANDOFF.md`と`docs/DECISIONS.md`：最新の停止位置、今回の回答と保留事項。
2. `docs/WORLD_OUTLINE_v0.1.md`：8地域、代表、章、系統の出発点。対立側はB採用。具体化は`docs/STORY_CONFLICT_B_v0.1.md`。
3. `docs/EARLY_WILD_SPRITES_v0.1.md`：一般種3体の個別候補9枚。設定画の経緯は`docs/EARLY_WILD_MODEL_SHEETS_v0.1.md`。`docs/STARTER_SPRITES_v0.1.md`：採用済みの2体6PNG。モデルの経緯は`docs/STARTER_MODEL_SHEETS_v0.1.md`。`docs/BATTLE_UI_v0.1.md`：採用済みのひらがな戦闘UI。`docs/HANAMIMI_SPRITES_v0.1.md`：見た目を採用した静止素材3点。`docs/ASSET_SPEC_v0.1.md`、`docs/prompts/FIRST_ART_BATCH_v0.1.md`：最初の1体と規格。
4. `docs/PRODUCTION_ESTIMATE_v0.1.md`：全体の制作量。
5. `docs/AUDIO_PRODUCTION_v0.1.md`：Sunoに渡す指示。

## 素材準備中に渡す依頼文

```text
このリポジトリは素材先行の企画・制作段階です。CLAUDE.md、docs/DECISIONS.md、docs/WORLD_OUTLINE_v0.1.md、docs/ASSET_SPEC_v0.1.md、manifests/assets.jsonを読んでください。
python3 tools/validate_assets.py と python3 tools/validate_preproduction.py を実行してください。
提案、採用原画、設定画案、取り込み用素材、未制作を区別し、既存の原画を保存してください。
156種・本編8地域／代表8人・クリア後2地域で骨格案を進めることは今回採用しましたが、対立側はB「一部責任者の隠蔽」を採用しました。docs/STORY_CONFLICT_B_v0.1.mdを読み、地域名・人物の具体像と外見・系統の詳細・素材規格の最終値まで承認済みとはしないでください。
ハナミミの個別PNG3点は画像規格確認・見た目採用済みです。戦闘UIを参考画面へ寄せ、ひらがな中心にする指示が追加されています。docs/BATTLE_UI_v0.1.mdを読んでください。さらに、このUI v0.1の見た目も採用済みです。ホノルは独立した腕2本・脚2本・背中の翼2枚がユーザー指定で、4肢案は不採用です。提示した2体の設定画から進める指示を受け、docs/STARTER_SPRITES_v0.1.mdの個別PNG6枚へ展開済みです。その6枚もユーザーが「完璧です」と回答し、採用済みです。一般種3体の設定画に続き、docs/EARLY_WILD_SPRITES_v0.1.mdの個別ドットPNG9枚もユーザーが「3体ともこのまま採用」と回答しました。runtime PNG19枚はすべて採用済みです。後続3体の新設定画はdocs/LATER_WILD_MODEL_SHEETS_v0.1.mdを参照し、確認待ちを維持してください。
content/planning/は制作計画で、ゲームへそのまま読み込む完成データではありません。
今はゲーム本体を実装せず、次の制作単位の資料・素材・参照整合を整えてください。必要な画像は内蔵画像生成のある環境へ渡す具体的な指示を作り、音楽はSuno用指示を使います。既存契約以外の従量APIへ勝手に切り替えないでください。
各タスクは既存チェックアウトで作業し、明示的な依頼がない限りGit worktreeを作らないでください。
```

## 本格実装へ進む前の条件

- 156種の系統・全種一人用入手・技・特性・道具と参照がそろっている。
- 全編と後日要素の人物・会話・マップ・フラグ・再挑戦経路がそろっている。
- 前後・アイコン・人物・地形・UI・音の実ファイルがあり、規格・目視・再生の確認記録がある。
- `python3 tools/validate_assets.py --require-complete`が通る状態に台帳と実物がそろっている。現在は未完成を検出して失敗するのが正しい。
- ユーザーが本格実装の開始を依頼したら、上記に加えて`brief/02_claude_code_cloud_prompt_v0.1.md`と`brief/19_claude_cloud_start_prompt_v0.1.md`の実装依頼文を使う。

台帳のフラグだけをtrueへ変えて開始しない。機械検査は美術・遊び・音の検証を代替しない。

## 初回のGit登録手順（まだ実行していない）

展開済み構成を登録する。ZIPだけをリポジトリへ置かない。最新のリモートを再確認し、他の作業があれば先に統合する。既存の履歴を上書きするforce pushは不要。

```sh
cd /workspace/MONORICA
git status --short
git ls-remote --symref origin
python3 tools/validate_assets.py
python3 tools/validate_preproduction.py
git add .gitignore README.md CLAUDE.md AGENTS.md LATEST_HANDOFF.md START_CLAUDE_CLOUD.txt HANDOFF_game_project_2026-11-02.md HANDOFF_MONORICA_2026-11-02_v0.11.md NEXT_SESSION_game_project.txt NEXT_SESSION_START_v0.11.txt brief content docs manifests tools assets reports
git diff --cached --stat
git commit -m "Prepare asset-first RPG planning and initial art study"
git push -u origin HEAD:main
```

pushはユーザーが登録を指示した時点で行う。GitHubとの読み取り成功は書き込み権限の確認ではない。GitHubへ渡した後も、Claude Codeのリポジトリ接続と実際の検査結果を別途確認する。

ファイルは通常Gitへ入るサイズで、Git LFSや追加課金の構成は導入していない。将来の音声原本の増加は実容量を見て判断する。秘密情報をGitへ含めない。
