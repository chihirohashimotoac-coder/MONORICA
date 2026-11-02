# ホノル・ミオマル：個別PNG6枚の取り込み候補

2026-11-02。2体の修正設定画を提示後、ユーザーが「進めてください」と指示。ホノルは独立腕2・脚2・背中の翼2、ミオマルは提示した小さな尾と腕の波形を基準に、前面・背面・アイコンへ展開した。

**6枚の比較画像と戦闘表示を提示後、ユーザーが「完璧です」と回答し、見た目も採用した。** 画像規格も確認済み。実機・アニメーション・進化形まで検証した意味ではない。

## 見比べる画像

- [ホノル：原寸と拡大](../reports/honoru-sprites_v0.1.png)
- [ミオマル：原寸と拡大](../reports/miomaru-sprites_v0.1.png)
- [味方ホノル・相手ミオマル](../reports/battle-honoru-vs-miomaru_v0.1.png)
- [味方ミオマル・相手ホノル](../reports/battle-miomaru-vs-honoru_v0.1.png)

枠・字体・コマンドは採用済みのUIを使用。表示する名前と画像だけを切り替える。レベル・HP・経験値は引き続き表示用の例で、今回の種族能力値ではない。

## ファイルと実測

| 対象 | 実ファイル | 実寸 | 最小外周余白 | 不透明色数 | 容量 |
|---|---|---|---:|---:|---:|
| ホノル前面 | [front.png](../assets/runtime/monsters/starter_ember_wyvern_01/front.png) | 96×96 | 5px | 31 | 5,830 bytes |
| ホノル背面 | [back.png](../assets/runtime/monsters/starter_ember_wyvern_01/back.png) | 96×96 | 8px | 31 | 5,129 bytes |
| ホノルアイコン | [icon.png](../assets/runtime/monsters/starter_ember_wyvern_01/icon.png) | 32×32 | 2px | 30 | 1,474 bytes |
| ミオマル前面 | [front.png](../assets/runtime/monsters/starter_tide_bear_01/front.png) | 96×96 | 6px | 29 | 6,154 bytes |
| ミオマル背面 | [back.png](../assets/runtime/monsters/starter_tide_bear_01/back.png) | 96×96 | 8px | 29 | 4,843 bytes |
| ミオマルアイコン | [icon.png](../assets/runtime/monsters/starter_tide_bear_01/icon.png) | 32×32 | 2px | 28 | 1,378 bytes |

計24,808 bytes。すべてRGBA PNG、アルファ値は0と255のみ。前面は左下向き、背面は右上向き。接地点は戦闘用(48,88)、アイコン(16,30)。

ホノルの大きな翼と尾を切らないよう、前後共通の倍率で余白を確保した。枠の高さを無理にハナミミと同じにせず、横へ広がる輪郭を保持する。ミオマルは太い胴と丸い耳、波形の前腕を識別点にする。背中に胸の渦巻きを描かない。

担当の目視では、ホノル前後の小さな手が翼と別に見え、ミオマルの波形と尾を判別できた。アイコンでは細部より角と翼／丸い耳と波形が目印になる。これらは目視所見であり、画像の採用を代わりに決めるものではない。

## 制作・再現

元の設定画と生成した`pixel_study_v0.1.png`を各sourceフォルダへ保持。採用済みハナミミと同程度の画素密度を指示して内蔵画像生成を実行し、その後の切り出し・減色・透過整理・サイズ調整は委任済みのコード工程で行った。

両方の生成原画像は前面が右向きだったため、個別出力時に前面だけ左右反転。背面は右上向きのまま保持した。前面を反転して背面の代わりにはしていない。

```sh
cd /workspace/MONORICA
python3 tools/prepare_starter_sprites.py
python3 tools/validate_assets.py
python3 tools/validate_preproduction.py
```

Pillowは`tools/requirements-art.txt`の版を使用。元画像のSHA-256・寸法・切り出し領域・反転の有無は`content/starter-art-export-profiles.json`。寸法と接地点等は`reports/starter-sprite-geometry_v0.1.json`に記録。

前後は共通倍率と種族ごとの共通31色以下の色表を使用し、ディザなし・nearestで出力。足元の低い帯を基準に配置する。既存の出力に異なる手修正があれば上書きせず停止する。別の種族へ切り出し座標を流用しない。

## 確認ツール

`tools/asset-review/sprite-candidates.html`で3体を切り替え、原寸・拡大・濃紺・草地色を比較できる。`battle-composition.html`では味方と相手を選択して向かい合わせる。これは素材の表示確認で、ゲーム本体や戦闘処理ではない。

6枚は`manifests/assets.json`でruntime_image、runtime_ready=trueへ更新。ハナミミ3枚とUI枠1枚と合わせて計10PNGが採用済み。実機、アニメーション、希少色、進化形の画像は今回の完了範囲ではない。
