# Akihabara Quiz System

Multi-tournament interactive quiz system with hardware buzzer support

## 概要

秋葉原スタイルのマルチ大会対応クイズシステム。RP2040 Pico W ハードウェアブザー統合、3つの異なるテーマ大会、リアルタイム観客画面同期を特徴とします。

## 特徴

### 🎯 4つのクイズ大会
- **🤖 ロボットアニメクイズ大会** - 1995年以降のロボットアニメ (120問)
- **😂 ネットミームクイズ大会** - インターネット文化とミーム (120問)
- **📺 2000年代以降アニメクイズ大会** - 2000年以降の名作アニメ (120問)
- **🎬 2000年代以前アニメクイズ大会** - 昭和・平成初期の名作 (120問)

### 🎮 クイズモード
- **⚡ 早押しクイズ** - 段階的テキスト表示、難易度別得点 (10/20/30pt)
- **🎨 シルエットクイズ** - 3段階ヒントシステム
- **🎵 イントロクイズ** - YouTube動画再生対応

### 🔧 ハードウェア統合
- **RP2040 Pico W ブザーサポート** - 10個のアーケードボタン (GP3-GP12)
- USB HID キーボードエミュレーション
- CircuitPython ファームウェア

### 🎨 ユーザーインターフェース
- リアルタイム観客画面同期 (BroadcastChannel API)
- プレイヤー名のクリック編集
- 不正解プレイヤーの再ブザー防止
- MP3効果音 (出題/ブザー/正解/不正解)
- 動的大会タイトル表示

## クイックスタート

### 方法1: ダウンロード版 (推奨)
1. `RoboAnimeQuiz.zip` をダウンロード
2. 解凍
3. `index.html` をブラウザで開く
4. プレイヤー設定 → ゲーム開始 → 大会選択

### 方法2: ローカルサーバー版
```bash
cd akihabara-quiz-system
python -m http.server 8000
```
ブラウザで `http://localhost:8000` にアクセス

## ハードウェアブザーセットアップ

### 必要なもの
- Raspberry Pi Pico W (RP2040)
- アーケードボタン 10個
- ジャンパーワイヤー

### 配線
```
ボタン1  → GP3  → GND
ボタン2  → GP4  → GND
ボタン3  → GP5  → GND
ボタン4  → GP6  → GND
ボタン5  → GP7  → GND
ボタン6  → GP8  → GND
ボタン7  → GP9  → GND
ボタン8  → GP10 → GND
ボタン9  → GP11 → GND
ボタン10 → GP12 → GND

注: GP0, GP1 (UART0), GP2 (WiFi) は予約済み
```

### ファームウェアインストール
1. CircuitPython 9.x を Pico W にインストール
2. `adafruit_hid` ライブラリを `CIRCUITPY/lib/` にコピー
3. `pico_buzzer/code.py` を `CIRCUITPY/code.py` にコピー
4. Pico W を再接続

## キーボード操作

### ゲームマスター (GM)
- **1-0**: プレイヤーブザー (1-9, 0=プレイヤー10)
- **Enter**: 正解表示
- **→**: 次の問題
- **Space**: ヒント表示 (シルエット) / イントロ再生
- **O**: 正解判定
- **X**: 不正解判定
- **R**: ブザーリセット

### プレイヤー
- **1-0キー** (キーボードまたはPico Wブザー)

## ファイル構成

```
akihabara-quiz-system/
├── index.html              # GM管理画面
├── audience.html           # 観客表示画面
├── tournaments/            # 大会別問題データ
│   ├── robot_anime.json   # ロボットアニメ (120問)
│   ├── net_meme.json      # ネットミーム (120問)
│   ├── modern_anime.json  # 2000年代以降 (120問)
│   └── classic_anime.json # 2000年代以前 (120問)
├── questions.json          # レガシー用（後方互換）
├── Sound/                  # 効果音
│   ├── shutudai.mp3       # 出題音
│   ├── katou.mp3          # ブザー音
│   ├── seikai.mp3         # 正解音
│   └── fuseikai.mp3       # 不正解音
├── pico_buzzer/
│   └── code.py            # Pico W ファームウェア
├── RoboAnimeQuiz.zip      # 配布パッケージ
└── README.md
```

## 問題データ構造

### Tournament形式 (新)
```json
{
  "tournaments": {
    "robot_anime": {
      "title": "チキチキ ロボスタディオン ロボットアニメクイズ大会!!",
      "hayaoshi": [120問],
      "silhouette": [...],
      "intro": [...]
    },
    "net_meme": { ... },
    "2000s_anime": { ... }
  }
}
```

### 早押し問題
```json
{
  "id": 1,
  "question": "「逃げちゃダメだ」が口癖の、新世紀エヴァンゲリオンの主人公は誰？",
  "answer": "碇シンジ",
  "difficulty": 1,
  "points": 10
}
```

## 技術スタック

- **フロントエンド**: Vanilla JavaScript, HTML5, CSS3
- **通信**: BroadcastChannel API (GM ↔ 観客画面)
- **ハードウェア**: CircuitPython, USB HID
- **オーディオ**: HTML5 Audio API (MP3)
- **ビデオ**: YouTube IFrame API

## 後方互換性

旧形式の`questions.json`も自動変換サポート:
```json
{
  "hayaoshi": [...],
  "silhouette": [...],
  "intro": [...]
}
```
→ 自動的に `tournaments.robot_anime` に変換

## トラブルシューティング

### Pico W ブザーが反応しない
- GP0-GP2 を使用していないか確認 (予約済み)
- CircuitPythonバージョンを確認 (9.x推奨)
- `adafruit_hid` ライブラリがインストールされているか確認

### 観客画面が同期しない
- 同じブラウザで開いているか確認
- BroadcastChannel API サポートブラウザを使用 (Chrome, Edge, Firefox)

### 音声が再生されない
- `Sound/` フォルダにMP3ファイルがあるか確認
- ブラウザの自動再生ポリシーを確認

## カスタマイズ

### 新しい大会を追加
1. `questions.json` に新しいtournamentを追加
2. `index.html` の tournament-screen に新しいボタンを追加
3. アイコンとカラーをカスタマイズ

### デザイン変更
- CSS変数 (`:root`) でカラーテーマを調整
- グラデーション、フォント、アニメーションをカスタマイズ

## ライセンス

MIT License

## クレジット

Created with ❤️ by Robostadion Team

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>

---

**Akihabara Quiz System** - Ultimate multi-tournament quiz experience with hardware integration
