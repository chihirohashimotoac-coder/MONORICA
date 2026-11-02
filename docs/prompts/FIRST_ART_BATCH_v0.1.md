> 最新更新：ハナミミ設定画の形の方向をユーザーが採用。中央背面を左右反転した`model_sheet_v0.2.png`と、向きをそろえた`pixel_study_v0.1.png`を追加した。試作は1983×793であり96/32pxの完成素材ではない。詳細は[BATTLE_COMPOSITION_v0.1.md](../BATTLE_COMPOSITION_v0.1.md)。以下は制作時点の記録と指示。

# 最初の画像制作指示 v0.1

## いま確認する画像

`assets/source/monsters/starter_flower_hare_01/model_sheet_v0.1.png`。
内蔵画像生成で、採用済み`brief/starter_concepts_v0.4.png`の左上を参照して新規制作した。元原画は変更していない。前3/4・後3/4・横の3体を同じ個体として描いた設定画案。文字は埋め込んでいない。

目視結果：緑と象牙色、桃色の瞳と耳内側、つぼみの尾を引き継いでいる。背面で尾の付け根が見える。耳裏の色、足の白い領域、顔の比率は原画で見えない部分の補完や揺れがあるため提案。画像は1983×793のRGB PNG、透過なし。**原画の正確な三面図・ドット絵・取り込み可能素材として採用済みではない。**

次の確認は「この背面の耳裏・つぼみの接続で同じ種に見えるか」。新しい種や進化形の確認とは分ける。

実際の生成指示は`hanamimi_model_sheet_v0.1.txt`に保存。以下は未実行の次工程の指示。

## ハナミミ：戦闘前面96px

参照：採用原画の左上＋今回の設定画案。原画を主、設定画を背面構造の補助とする。

```text
Create ONE original game pixel-art sprite of Hanamimi, the green flower-hare in the TOP LEFT of the approved reference board. Preserve its small rounded ivory face, pink eyes, two broad green leaf ears with pink inner petals, compact green body, ivory paws, and ONE closed pink flower-bud tail. Do not depict its evolution or any other creature.
Enemy battle FRONT view, three-quarter facing down-left. Quiet alert pose, all four paws supported, both ears and the bud fully visible. Use large clear pixel clusters, restrained green/ivory/pink colors, a colored dark outline, no texture or anti-aliased painting. Logical target is a 96x96 transparent RGBA sprite with a bottom ground anchor at (48,88) and at least four empty pixels on each edge. No text, grid, shadows, scene or decorations. If the generator cannot output an exact 96x96 file, treat its output only as a pixel-art study; do not label it production-ready.
```

## ハナミミ：戦闘背面96px

```text
Using the same approved Hanamimi design and the reviewed rear model sheet, create ONE pixel-art BACK-view battle sprite. Player companion facing up-right, away from the viewer. Show the backs of the two broad leaf ears, the compact green back, and the ONE pink bud connected to the rump on a short green base. Do not substitute a mirrored front view. Match the front sprite's body scale, palette, contour weight, ground level and anatomy. Logical target 96x96 transparent RGBA PNG, ground anchor (48,88), four empty border pixels. No face turned toward camera, no text, scenery, grid or ground shadow. Exact dimensions, transparency and continuity must be checked after generation; do not call an enlarged study a finished sprite.
```

## ハナミミ：32pxアイコン

```text
Create ONE tiny, readable pixel-art party icon of the same Hanamimi. Show its round ivory face, pink eyes, two broad green-and-pink leaf ears and one hint of the pink bud. Simplify deliberately for a logical 32x32 transparent RGBA canvas with two empty border pixels. Colored dark-green outline, broad pixel clusters, no tiny fur detail or soft shading. It must read as the initial flower-hare, not the taller floral evolution. No text, frame, grid, shadow, background or extra creatures. Verify actual export dimensions before classifying it as a runtime asset.
```

## 後続の設定画：原画を主にする

| 制作対象 | 固定する識別点 | 補完前に確認する点 |
|---|---|---|
| ホノル | 赤、暗い角、小さな翼、明るい口元、胸の火の印 | 最新指定は独立腕2・脚2・背中の翼2。新しいv0.2設定画を参照し、4肢の旧指示を使わない |
| ミオマル | 丸い耳、青い目、象牙色の腹、濃紺の手足、前腕の波形 | 小さな波形の裏側、短い尾の有無 |
| リスコロ | 木の実、大きな種房形の尾、橙と茶、丸い目 | 尾の基部を一本に統一。複数の尾を勝手に追加しない |
| ツルモグ | 低い胴、大きな前足、葉の前髪、つたの尾 | 葉と尾の接続。後ろ足の長さ |
| ハネリ | 青緑、珊瑚色、扇尾 | 閉じた翼と背面の羽色、尾羽の枚数の整理 |
| ミズッタ | 長い胴、平たい尾、水紋、灰青と象牙色 | 水紋が体表か尾の模様か、背面の連続性 |
| ココイル | 薄紫と茶、巻いた尾、光る帯 | 巻きの向きと尾の付け根。左右反転で帯を増やさない |
| ヨルミル | 藍と紫の飛膜、目の周りの模様、淡い尾端 | 飛膜が手首から足首につながる構造を統一 |

共通指示：元の比較原画を必ず参照してから、同寸の前・後・横を白地で別ファイルへ生成する。見えない器官は提案として記録し、設定画のレビュー後にドット素材へ進める。中間形の承認や全種の量産をこの指示から推定しない。
