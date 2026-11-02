# Suno向け音楽制作パック v0.1

**実音源は0曲。** このファイルはSuno Proでユーザーが制作するための指示。APIや有料追加サービスへの接続、Sunoへの送信は行っていない。28曲のキュー一覧は`content/planning/audio-cues.csv`。用途と共通モチーフを定めてから地域ごとに増やす。

## 共通の音楽像

親しみやすい携帯機RPGらしい明快な旋律と、現代に近い村や自然の空気。特定の既存ゲーム曲や作家の模倣を指定しない。人工の育成設備には木琴に重なる控えめな規則的パルスを使い、異変ではパルスと生楽器の拍を少しずらす案。恐怖一色にはしない。

幼なじみとの約束は「短い上行→少し間を置く→返答」の旋律の形を共通の発想にする。同じ旋律の再現にはユーザーがSunoの対応機能で元音源を参照できるかを確認する。プロンプトだけで音符の一致を保証しない。

全曲インストゥルメンタル。歌詞・台詞なし。ゲーム内の周回に耐える、過密でない編曲。生成曲の最後に長い無音や派手な終止を置かない。出力の接続・音量・権利条件は実ファイルと利用時点の契約で確認し、ループ可能と断言しない。

## 最初に作る3曲

### 1. ハルネ村：穏やかな旅立ち

- ID：`bgm_home_harune`
- 用途：村の屋外、相棒と過ごす序章。設定画確認と並行して最初の1曲に使う。
- 目安：86～96 BPM、4/4、温かい長調、90～120秒。速度は生成後に確認。
- 元音源保管：`assets/source/audio/bgm_home_harune/`。取り込み予定：`assets/runtime/audio/bgm_home_harune.mp3`。

```text
Instrumental music for an original monster-companion adventure RPG, a peaceful modern countryside village before a long journey. Warm intimate wooden flute melody, soft plucked acoustic strings, gentle marimba answers, light brushed percussion and a simple rounded bass. About 92 BPM, 4/4, bright but tender major-key mood. A memorable short rising question phrase followed by a small pause and a friendly answer, suggesting a childhood promise. No vocals, lyrics or spoken words. No orchestral climax, heavy drums or grand crisis. Begin with a short natural pickup, then a stable repeat-friendly A-B structure, around 90 to 120 seconds. End with a light phrase that can return to the beginning rather than a dramatic final chord. Clear melody, sparse accompaniment, comfortable during extended gameplay. Original composition; do not quote existing game music.
```

### 2. はじまりの街道：寄り道の一歩

- ID：`bgm_route_first`
- 目安：106～116 BPM、4/4、笛＋弾む弦＋手打ちの小打楽器、90～150秒。
- 村より前進する感触。まだ強敵の行進曲にはしない。

```text
Original instrumental exploration music for the first grassy road of a creature-collecting adventure. A lively wooden flute and lightly bouncing plucked strings, airy marimba accents, small hand percussion and a walking bass. Around 112 BPM, 4/4. Curious and sunny, with room to hear footsteps and menu sounds. Use a rising question-and-answer melodic contour to evoke the home village, but give the rhythm a gentle forward motion. No vocals, lyrics or speech. A short pickup followed by two contrasting repeat-friendly sections, 90 to 150 seconds, no long silence, fadeout or huge ending. Friendly adventure rather than military march. Entirely original melody.
```

### 3. 野生戦：はじめての駆け引き

- ID：`bgm_battle_wild`
- 目安：138～150 BPM、4/4、木琴の短音＋軽いシンセベース＋明快な打楽器、90～120秒。
- 捕獲の緊張を支えるが、恐怖や決戦の重さにはしない。

```text
Original instrumental turn-based wild creature battle music. Agile short mallet phrases, bright compact synth accents, a nimble bass line and crisp but not overwhelming drums. Around 144 BPM, 4/4. Playful tactical tension and quick exchanges, not a dark boss battle. A clear short main hook, an answer section with a different register, then a natural return. Leave space for attack and capture sound effects. No vocals, lyrics, speech, sampled game sounds or quotations. About 90 to 120 seconds, a brief opening cue and a stable loop-oriented body. Avoid a long fadeout or triumphant ending; victory uses a separate cue.
```

## 受け渡しメモ

生成したら、採用候補の音源、生成に使った指示、生成日、Suno側の曲識別情報、バージョンをまとめて渡す。アカウント情報や秘密鍵は不要。音源のダウンロード形式・契約上の扱いは利用画面で確認する。

受領後に測る項目：実長、BPM、サンプルレート、チャンネル数、ラウドネス、ピーク、導入長、ループ始終サンプル位置。音源未受領の現在はこれらを推定値で埋めない。`manifests/assets.json`の音源数も0のままにする。
