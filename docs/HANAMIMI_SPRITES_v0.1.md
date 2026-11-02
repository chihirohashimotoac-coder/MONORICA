> 最新：ユーザーが「ドット絵の雰囲気・細かさは問題ありません。完璧です」と回答し、前面・背面・アイコン3点の見た目を採用。台帳のruntime_readyを3点trueへ更新した。以下の確認待ちは制作当時の記録。実機・アニメーションは未検証。

# ハナミミ：前面・背面・アイコンの取り込み候補

2026-11-02。ユーザーが「コードによる仕上げも任せる」を選択。元画像を残し、切り出し・減色・透過整理・サイズ調整をコードで行った。以下は**画像規格を確認した取り込み候補**で、出力後の見た目のユーザー確認はまだ。

## 今回の3ファイル

| 素材 | 実ファイル | 実寸 | 向き・基準点 | 最小の外周余白 | 容量 |
|---|---|---|---|---|---:|
| 戦闘前面 | [front.png](../assets/runtime/monsters/starter_flower_hare_01/front.png) | 96×96 | 左下向き・(48,88) | 8px | 5,305 bytes |
| 戦闘背面 | [back.png](../assets/runtime/monsters/starter_flower_hare_01/back.png) | 96×96 | 右上向き・(48,88) | 8px | 4,516 bytes |
| 手持ちアイコン | [icon.png](../assets/runtime/monsters/starter_flower_hare_01/icon.png) | 32×32 | (16,30) | 2px | 1,350 bytes |

合計11,171 bytes。すべてRGBA PNGで、アルファ値は0か255のみ。共通の31色以下の色表で処理し、各出力の不透明色は30色。前後の倍率をそろえ、広い耳の中心ではなく足元を接地点へ合わせた。元の設定画と高解像度試作は変更していない。

## 見た目の確認

- [原寸と拡大の比較](../reports/hanamimi-sprites_v0.1.png)：96px・32pxの実ファイルを1倍と整数倍で表示。
- [濃紺背景での比較](../reports/hanamimi-sprites_dark_v0.1.png)：輪郭や透過縁の見え方を確認。
- [戦闘配置での表示](../reports/battle-composition_v0.2.png)：実寸96pxの候補を使った静的な配置例。位置・倍率・UIは引き続き案。

担当の目視では、前面の桃色の目・緑と桃色の耳、背面の耳裏・つぼみ、アイコンの輪郭を判別できた。原寸のアイコンでは瞳の細部より、耳と桃色の尾が識別点になる。32pxで顔をもっと大きく見せたい場合は、頭と耳を中心にした別アイコン案と比較する。

機械的な寸法一致だけを理由に最終採用しない。輪郭の段差、顔の印象、前後の同一性、他の種と並べた体格差は引き続き確認対象。今回の1体から全156種の規格が確定したとはしない。

## 再現方法

元：`assets/source/monsters/starter_flower_hare_01/pixel_study_v0.1.png`。
スクリプト：`tools/prepare_hanamimi_sprites.py`。今回は導入済みPillow 12.3.0で実行した。

```sh
cd /workspace/MONORICA
python3 tools/prepare_hanamimi_sprites.py
python3 tools/validate_assets.py
python3 tools/validate_preproduction.py
```

Pillowがない環境では画像を再書き出す場合だけ`tools/requirements-art.txt`を使う。生成済みPNGの利用や素材確認帳の閲覧にPillowは不要。

処理：元画像のハッシュ確認→明示した3領域の切り出し→アルファ192以上を輪郭として最大の連結部分を保持→nearestで縮小→共通パレットへ減色（ディザなし）→足元を基準点へ配置→寸法・余白・アルファ・色数を検査して書き出し。

元絵を描き直す処理ではない。新しい顔・器官をコードで付け足していない。別種の切り出し位置へ自動流用しない。既存の出力が異なる内容に手修正されていた場合は、上書きせず停止する。

## 記録と未完了

- `reports/hanamimi-sprite-geometry.json`：実寸・余白・色数・接地点・SHA-256。
- `reports/hanamimi-sprite-browser-check.json`：原寸表示、候補別の規格自動選択、背景切り替え、戦闘配置、狭い画面の確認。
- `manifests/assets.json`：取り込み候補3件を登録。`runtime_ready`はfalse、見た目の採用待ち。
- `manifests/production_queue.csv`：ハナミミ3件を未制作から候補確認待ちへ更新。

本体実装、実機での表示、アニメーション、希少色、他155種の画像、人物・タイル・音声は今回の完了範囲ではない。
