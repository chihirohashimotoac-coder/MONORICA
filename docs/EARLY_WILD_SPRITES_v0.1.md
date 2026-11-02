# リスコロ・ツルモグ・ハネリ：採用済み個別PNG9枚

2026-11-02。前後横の設定画を提示後、ユーザーが「問題ありません」と回答。採用した設定画から、御三家と同じ雰囲気のドット素材へ展開した。**今回の9枚は画像規格確認済み。2026-11-02にユーザーが「3体ともこのまま採用」と回答し、見た目も採用済み。** 名前と属性は従来どおり作業案で、進化・能力値の確定ではない。

## 見比べる

- [リスコロ：原寸と拡大](../reports/riscoro-sprites_v0.2.png)
- [ツルモグ：原寸と拡大](../reports/tsurumogu-sprites_v0.2.png)
- [ハネリ：原寸と拡大](../reports/haneri-sprites_v0.2.png)
- [味方ハナミミ・相手リスコロ](../reports/battle-hanamimi-vs-riscoro_v0.1.png)
- [味方ツルモグ・相手ハネリ](../reports/battle-tsurumogu-vs-haneri_v0.1.png)
- [味方ハネリ・相手ツルモグ](../reports/battle-haneri-vs-tsurumogu_v0.1.png)

UI枠・字体・主コマンドは採用済みのまま。名前と画像を切り替えた表示例で、レベル・HP・経験値は種族データの確定値ではない。

## 個別ファイル

| 対象 | 前面96×96 | 背面96×96 | アイコン32×32 | 3枚の容量 |
|---|---|---|---|---:|
| リスコロ | [front.png](../assets/runtime/monsters/wild_seed_squirrel_01/front.png) | [back.png](../assets/runtime/monsters/wild_seed_squirrel_01/back.png) | [icon.png](../assets/runtime/monsters/wild_seed_squirrel_01/icon.png) | 11,361 bytes |
| ツルモグ | [front.png](../assets/runtime/monsters/wild_vine_mole_01/front.png) | [back.png](../assets/runtime/monsters/wild_vine_mole_01/back.png) | [icon.png](../assets/runtime/monsters/wild_vine_mole_01/icon.png) | 10,795 bytes |
| ハネリ | [front.png](../assets/runtime/monsters/wild_breeze_bird_01/front.png) | [back.png](../assets/runtime/monsters/wild_breeze_bird_01/back.png) | [icon.png](../assets/runtime/monsters/wild_breeze_bird_01/icon.png) | 10,766 bytes |

合計32,922 bytes。すべてRGBA PNG、アルファ値は0と255のみ。戦闘画像は前後共通倍率で接地点(48,88)、アイコンは配置基準(16,30)。

戦闘前後の最小外周余白は5～8px、アイコンは全3枚で2px以上。不透明色は各29～31色。種族ごとに前後・アイコンで共通の色表を使用した。

アイコンは輪郭全体を中央へ置き、尾や冠羽が大きい種でも読める面積を確保する。ツルモグは横へ低い姿を保つため、アイコンの描画部分も横長。姿勢を立たせて別の動物に変えない。

## 確認点

- リスコロ：1本につながる大きな種房状の尾、薄緑の尾先、胸に抱えた木の実を維持。背面の腰の付け根と尾が連続し、木の実は背中へ追加していない。
- ツルモグ：頭の葉2枚と、先端に小さな葉がある1本のつたの尾を分けて保持。大きな象牙色の前足、低い胴、小さい後ろ足を残した。
- ハネリ：翼2枚・脚2本・1つの扇尾を保持。青緑と象牙色の扇尾、珊瑚色の肩、黄色いくちばしを識別点にした。

担当は原寸・拡大・戦闘表示で輪郭を目視した。背面では見えない顔の細部を描き足さず、低い体形などの見切れ方は表示確認の対象に残す。提示後にユーザーが3体とも採用と回答した。

## 再現と元画像

元の設定画と生成した各`pixel_study_v0.1.png`はsourceに保持。新規のドット用原画像は内蔵画像生成を使用し、正確な寸法への切り出し・減色・透過整理は委任済みのコード工程で実施した。

```sh
cd /workspace/MONORICA
python3 tools/prepare_early_wild_sprites.py
python3 tools/validate_assets.py
python3 tools/validate_preproduction.py
```

`content/early-wild-art-export-profiles.json`に、元画像のSHA-256、実寸、個別の切り出し領域と反転指定を記録。ハネリは前面とアイコンを左右反転し、他の2体は元の向きを使用。全ての背面は右上向きを維持した。

書き出しはPillowの同じ処理を共用するが、今回のアイコンだけは`icon_alignment=bounds`を指定。御三家の既存出力を変更しない。元画像のハッシュが変わった場合、既存PNGに異なる手修正がある場合は停止する。別種へ切り出し座標を流用しない。

`reports/early-wild-sprite-geometry_v0.1.json`に実寸・余白・色数・配置・SHA-256、`early-wild-sprite-browser-check_v0.1.json`に比較画面の確認記録を保存。

## 現在の状態

取り込みフォルダのPNGは計19枚。御三家9枚＋一般種9枚＋UI枠1枚のすべてが見た目採用済み、runtime_image・runtime_ready=true。全図鑑・音・人物・地形は未完成。

素材確認帳は、出力済みPNGがある6体を切り替えられる。一般種の後続3体（ミズッタ・ココイル・ヨルミル）の設定画案も制作した。新しい前後横は確認待ち。詳細は[後続3体の設定画](LATER_WILD_MODEL_SHEETS_v0.1.md)。
