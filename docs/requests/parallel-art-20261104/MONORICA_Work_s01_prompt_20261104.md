# MONORICA：5セッション同時制作 1/5

これは制作の実行依頼です。計画やプロンプトの作成だけで終えず、担当30種の三面設定画を実際に制作・保存してください。
使用AI：ChatGPT Work。モデル：GPT-6.1 Sol、エフォート：高を指定。画像はWorkで利用可能な内蔵画像生成ツールを使用。モデル・エフォートの設定はUIで選び、利用できない設定や機能を利用済みと報告しない。別料金の従量APIへ切り替えない。
役割：MONORICAのキャラクターデザイン担当兼、画像保存・同一性確認担当。日本語で作業・報告する。

## 今回のユーザー指示と優先順位
- 全体は156種。5つの独立したWorkセッションが同時進行する。このセッションの担当は下表の30種のみ。
- 新規制作は既存15種を除く141種で、割り当ては30/28/28/28/27。既存画像の参照記録があることと、採用済み・本体確認済みであることを区別する。
- ユーザーは回収待ちを打ち切り、未確認だった制作分を新たに作り直すことを許可した。過去の131種の復旧は今回の開始条件ではない。再制作を復元と呼ばない。
- 既存成果物は削除・置換せず保全。全体の制作がそろってからユーザーがまとめて確認し、気になる部分を個別修正する。3体ごとの承認待ちを挟まない。
- 旧AGENTS.md/CLAUDE.md/Handoffの「画像生成禁止」「12バッチ」「復旧待ち」は当時の工程指示。この依頼で担当種の画像生成は明示的に許可する。採用状態・runtime昇格の許可とは別。
- 元の仕様・名前・種ID・進化・器官数・配色を勝手に変更しない。

## 正本と共通の設計基準
リポジトリ：https://github.com/chihirohashimotoac-coder/MONORICA
設計元ブランチ：work/species-review-v013-20261103
全5セッションで使う共通の確認済み設計スナップショット：b6c1d875e3f624bb77d1e632bfed561380d7ed19
元のDraft PR：https://github.com/chihirohashimotoac-coder/MONORICA/pull/2
最初にGitHub最新参照を読み、基準SHAが取得できることを確認する。全セッションの設計を統一するため、制作にはこのスナップショットの資料を使う。最新参照と基準SHAの差は記録し、元ブランチを過去SHAへresetしない。以降に明示的な設計訂正があり基準と矛盾するときは、その矛盾だけを問題として報告する。

GitHubから次を読む。大量文書の全内容をチャットへ再掲せず、担当種とその進化系列の必要部分を抽出する。
1. AGENTS.md、CLAUDE.md、LATEST_HANDOFF.md、docs/DECISIONS.md
2. docs/SPECIES_REVIEW_v0.1.md、docs/SPECIES_DESIGN_DETAILS_v0.1.md
3. content/planning/species-catalog_v0.1.json または同CSV
4. docs/SPECIES_ART_BATCHES_v0.1.md（既存の造形上の注意だけ参照。旧12バッチ割り当ては使わない）
5. reports/image-recovery-inventory_2026-11-04.json
6. docs/ASSET_SPEC_v0.1.md、担当系列の既存設定画・比較原画
JSON取得がサイズ等で空になる場合、空をデータなしと扱わずCSV・詳細Markdownまたはクラウド内チェックアウトで読む。同一基準SHAの資料を使う。

## 担当種：30種
番号は検査用、種IDを保存・照合のキーとする。表以外の種を生成しない。
| 図鑑番号 | 種ID | 名前 | 系列・段階 |
|---|---|---|---|
| 011 | wild_seed_squirrel_02 | コノミリア | wild_seed_squirrel 2/2 |
| 013 | wild_vine_mole_02 | ネヅナグ | wild_vine_mole 2/2 |
| 015 | wild_breeze_bird_02 | オウギル | wild_breeze_bird 2/2 |
| 017 | wild_stream_otter_02 | カワミオ | wild_stream_otter 2/2 |
| 019 | wild_coil_dormouse_02 | マキデン | wild_coil_dormouse 2/2 |
| 021 | wild_dusk_glider_02 | ヨイトバリ | wild_dusk_glider 2/2 |
| 022 | wild_reed_crane_01 | アシピナ | wild_reed_crane 1/3 |
| 023 | wild_reed_crane_02 | ササナギ | wild_reed_crane 2/3 |
| 024 | wild_reed_crane_03 | ミナツルネ | wild_reed_crane 3/3 |
| 025 | wild_lock_crab_01 | カチコバ | wild_lock_crab 1/3 |
| 026 | wild_lock_crab_02 | セキバサミ | wild_lock_crab 2/3 |
| 027 | wild_lock_crab_03 | ミトガニス | wild_lock_crab 3/3 |
| 028 | wild_lotus_frog_01 | ハスプク | wild_lotus_frog 1/2 |
| 029 | wild_lotus_frog_02 | ウキハスネ | wild_lotus_frog 2/2 |
| 030 | wild_silt_skate_01 | ドロヒラ | wild_silt_skate 1/2 |
| 031 | wild_silt_skate_02 | スナミオ | wild_silt_skate 2/2 |
| 032 | wild_mist_snail_01 | ツユマキ | wild_mist_snail 1/2 |
| 033 | wild_mist_snail_02 | キリマイム | wild_mist_snail 2/2 |
| 034 | wild_lantern_jelly_01 | ホヤリネ | wild_lantern_jelly 1/2 |
| 035 | wild_lantern_jelly_02 | ミナランプ | wild_lantern_jelly 2/2 |
| 036 | wild_bog_leech_01 | ペタリム | wild_bog_leech 1/2 |
| 037 | wild_bog_leech_02 | シブネリ | wild_bog_leech 2/2 |
| 038 | wild_reed_whistle_01 | アシフエラ | wild_reed_whistle 1/1 |
| 039 | wild_bubble_moth_01 | アワハリカ | wild_bubble_moth 1/1 |
| 040 | wild_kiln_pup_01 | ホコロン | wild_kiln_pup 1/3 |
| 041 | wild_kiln_pup_02 | カマテラ | wild_kiln_pup 2/3 |
| 042 | wild_kiln_pup_03 | ロカマルド | wild_kiln_pup 3/3 |
| 043 | wild_glass_gecko_01 | スナペト | wild_glass_gecko 1/3 |
| 044 | wild_glass_gecko_02 | ハクスリカ | wild_glass_gecko 2/3 |
| 045 | wild_glass_gecko_03 | ルミガレス | wild_glass_gecko 3/3 |

## 対象外・既存画像の保護
図鑑001〜010、012、014、016、018、020の15種は、既存設定画または新画像の保存参照があるため新規制作対象外。最初の6番までを一律に除外する意味ではない。既存原画・旧版・runtime19PNGを保持する。
このセッションだけ、後述する既存画像保全も行う。

## セッション1だけの既存画像保全
これは新規制作30種とは別の作業。既存15種を再生成しない。
GitHub上の既存9種は次の画像本体を読み出し、種IDと現行状態を保持する。
- 001 ハナミミ: assets/source/monsters/starter_flower_hare_01/model_sheet_v0.2.png（静止素材採用済み）。
- 004 ホノル: assets/source/monsters/starter_ember_wyvern_01/model_sheet_v0.2.png（静止素材採用済み・腕2/脚2/独立翼2）。
- 007 ミオマル: assets/source/monsters/starter_tide_bear_01/model_sheet_v0.1.png（静止素材採用済み）。
- 010 リスコロ: assets/source/monsters/wild_seed_squirrel_01/model_sheet_v0.1.png（静止素材採用済み）。
- 012 ツルモグ: assets/source/monsters/wild_vine_mole_01/model_sheet_v0.1.png（静止素材採用済み）。
- 014 ハネリ: assets/source/monsters/wild_breeze_bird_01/model_sheet_v0.1.png（静止素材採用済み）。
- 016 ミズッタ: assets/source/monsters/wild_stream_otter_01/model_sheet_v0.1.png（設定画確認待ち）。
- 018 ココイル: assets/source/monsters/wild_coil_dormouse_01/model_sheet_v0.1.png（設定画確認待ち）。
- 020 ヨルミル: assets/source/monsters/wild_dusk_glider_01/model_sheet_v0.2.png（設定画確認待ち・旧v0.1不採用）。
次の6種は保存登録のみ確認済み。画像本体・寸法・ハッシュ・視覚品質の今回の検証はまだない。利用可能な正式のファイル連携から取得できたものだけ、下記自分の保存領域へ元画像をそのまま複製・GitHub保存し、再取得して照合する。6種は001〜006という連番ではない。
- 002 ハナリット / starter_flower_hare_02 / libfile_ef9f7ab2bb6081918b6d1488e0983e27
- 003 フロレーヌ / starter_flower_hare_03 / libfile_ec098fd6840881918cf6ced883672dfa
- 005 フレイガ / starter_ember_wyvern_02 / libfile_6b650159b7048191b16783af7493204c
- 006 グレンヴァル / starter_ember_wyvern_03 / libfile_d105a36a262881918e568c3a15b419fd
- 008 ナミグマ / starter_tide_bear_02 / libfile_3ab69295b1e0819188ef9c7b06681f08
- 009 タイドガル / starter_tide_bear_03 / libfile_0cdca3869db8819190f00ef336734d9b
取得不能な既存画像は「保存登録あり・本体未確認」と台帳に残し、再生成・採用扱いをしない。この6種や過去の「131種」の復旧を理由に、担当の新規制作を全停止しない。保全できた既存画像は preserved/ に保存して新規生成と区別する。保全できなくても「全156種そろった」と報告しない。

## 同時実行時の保存先とGit運用
自分専用ブランチ：work/art-parallel-s01-20261104
自分専用の画像ルート：assets/source/monsters/parallel_20261104/s01/
自分専用の記録ルート：reports/art-parallel-20261104/s01/
自分専用Handoff：docs/handoffs/art-parallel-20261104/s01.md

- クラウド内の独立した一時チェックアウトを使う。PC内フォルダー・OneDriveへ依存しない。他セッションの作業ディレクトリを操作しない。
- 専用ブランチは上記基準SHAから新規作成する。すでに存在する場合は自分のブランチと記録を読み、完了済み画像から再開。作り直し・reset・force pushをしない。
- 元ブランチ、main、他セッションのブランチへpushしない。共通のLATEST_HANDOFF.md、README.md、DECISIONS.md、manifests/assets.json、設計カタログ、既存PR #2は変更しない。これで同時更新の衝突を避ける。
- 画像は <画像ルート>/<species_id>/model_sheet_v0.1.png へ新規保存。既存の同名画像があれば一致確認して再利用し、不一致は別版名にする。
- 設定画は確認待ち候補として保存。美術の採用、runtime出力、ゲーム実装、マージ、公開、デプロイはしない。
- 最後に自分専用ブランチから設計元ブランチへの独立Draft PRを1件作る。既存の同ブランチPRがあれば重複作成しない。PR #2を更新しない。PRには担当一覧・実画像を閲覧できるGitHubリンク・検証結果・戻し方を記す。外部公開のプレビューサイトは新設しない。
- 統合は別工程。自分で5ブランチを統合・マージしない。

## 制作内容と見た目
1種につき1枚、同じ個体の「前3/4・後3/4・横」の3ビューを並べたフルカラー設定画を作る。複数種の集合画像1枚で30種完成扱いにしない。
既存MONORICA原画に合わせた、可愛く親しみやすいオリジナルのモンスター。白地、明確な輪郭、大きく読める色面、全身と全付属器官を枠内に入れる。文字・番号・ロゴ・透かし・UI・背景風景を画像へ焼き込まない。名前と番号は画像外の台帳へ記載する。
設定画は高解像度のデザイン資料。96px戦闘スプライト・32pxアイコンやドット絵は今回作らない。画像の正確な寸法・モード・透過は実ファイルから測定し、生成前の指定値を実測値として書かない。

- 毎種、CSV/JSONのモチーフ、シルエット、主配色、差し色、顔、器官数、接続、前背横の識別点、進化変化、96px/32pxで残す特徴、差別化、参照を読む。
- 同系列はこの担当内で続けて制作し、基礎形から進化後への成長差を維持。既存基礎形がある場合は必ず原画を参照する。別セッションの画像完成待ちは不要な割り当てになっている。
- 3ビューで色面・器官数・付け根・個体の左右・模様の位置を一致させる。見えない器官は消失した扱いにせず重なりで表現。
- 原画・既存画像を取得できていないのに「参照した」「照合済み」と言わない。採用済みデザインを自分の好みで描き直さない。
- 特に注意：既存の初期形と同系列の進化後は、参照原画を見てから制作。水紋はカワウソの尾上面のみ。マキデンは銅4帯・水色4帯で、初期ココイルの3帯をコピーしない。ヨイトバリは四肢4・独立翼0・手首〜足首の飛膜。蟹は歩脚6＋はさみ2、セキバサミ以降の大鋏は個体左を守る。ガラスヤモリの背板枚数は各段階の最新接続文に従う。
- 構造は最新の種別接続文を優先し、共通バッチ説明の段階共通文を無条件コピーしない。
- 新しい生物の絵は必ず画像生成ツールで制作する。Python/SVG/図形の組み合わせによる代替制作はしない。

## 生成と保存を1体ごとに完了する
最初の担当1種で、生成→実ファイル取得→GitHub保存→読み戻しまで実行できるか確認してから残りへ進む。ここで保存ができなければ大量生成を続けず、実際の問題と保存済みのものを報告する。

1. その種の設計と参照原画を確認し、実際に使う画像生成指示を記録。
2. 画像を生成し、ツールが返した画像を表示。画像本体を保存して開き、三面の整合・器官数・付け根・全身の欠けを目視確認する。
3. 明確な設計違反は必要な修正を行う。好みの細かな調整で大量の候補を増やさず、残る懸念は確認事項へ記録する。
4. 完成候補の画像本体と自分専用台帳のその行をGitHubへ保存。可能なら通常の認証済みGitを使用し、ツールの制限を推測して保存済みと報告しない。
5. GitHub側からその画像本体を再取得し、元のSHA-256・バイト数と一致することを確認する。ファイル名・リンク・blobメタデータだけの確認は本体確認ではない。
6. 画像本体の読み戻しまで確認できた種だけ「保存確認済み」にし、次の種へ進む。チャット表示、生成ログ、ローカル一時保存、保存予約のみで完了にしない。

画像生成機能・参照画像・保存権限が利用不能の場合、実際の制約を明示し、画像を生成したふりをしない。回数制限や接続エラーが出たら、既存成果物を保全し、残りを未完了で記録する。架空の成功報告や、有料APIへの迂回をしない。
生成画像が自動保存されるサービスでも、今回依頼したGitHubへの保存・読み戻しとは別に判定する。

## 台帳・検証・終了条件
自分専用の manifest.json または manifest.csv に、少なくとも以下を記録する。
図鑑番号、種ID、名前、参照基準SHA、生成指示ファイル、実画像パス、画像寸法・モード・バイト数・SHA-256、目視で確認した内容、未確認事項、GitHub読み戻し結果、保存先コミット、状態（未着手／生成済み未保存／保存確認済み／要修正）。
採用状態は pending_user_review を維持。GitHub記録に既存画像の登録や過去検査の成功を流用せず、今回実施分だけ書く。

- 自分の表と台帳を種IDで照合し、30種すべてがそろい、重複・対象外・空ファイル・同一画像の使い回しがないことを確認。
- 担当系列が途中で他セッションへ分断されていないこと、3ビューの整合を確認。
- コードや共通カタログを変更しない。既存のvalidate_assets.py / validate_preproduction.py等を実行した場合は実出力を保存し、実行しなければ未実行とする。候補画像の追加を既存runtimeの検証済み扱いにしない。共通ファイルを修正して検査を無理に通さない。
- 全担当の画像・生成指示・台帳・自分専用Handoffをcommit/pushし、GitHub側の最新SHAを確認。画像のGitHub閲覧リンクをまとめたreview.mdも専用記録ルートへ置く。
- Handoffには担当、保存確認済み数、未完了ID、次の1体、検証、制限、ブランチ、コミット、Draft PRを記す。
- 中断・コンテキスト増大の際は現在の生成結果を保存してから、この専用Handoffへ停止位置を残す。未保存結果を残して新セッションへ移行しない。担当完了前に終了する場合は未完了を明示する。

## チャットへの報告
途中経過の文章・資料全文・逐次の長い思考説明は不要。担当完了、ユーザーの確認が必須の事項、続行不能の問題、ユーザーからの進捗確認のときだけ簡潔に報告する。画像生成ツールによる画像の表示はそのままでよい。
確認が不要な通常の作画判断では止まらず、担当範囲を通して制作する。今回は自分の30種を完了しても「全156種完成」と言わない。
最終報告は担当数／保存確認済み数／未完了数、Draft PR、レビュー一覧、専用Handoff、懸念だけを簡潔に示す。
