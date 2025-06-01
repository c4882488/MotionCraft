# MotionCraft 🎬✨

🎬 將影片轉換為符合 Google Motion Photos 1.0 規範的格式

## 🌟 功能特色

- 📱 完全符合Google Motion Photos 1.0規範
- 🎯 自動生成檔案名稱 (video.mp4 → video.MP.jpg)
- 🧹 自動清理臨時檔案
- 🔍 完整的驗證工具
- 💻 簡單易用的命令行介面
- 🎭 互動式演示功能

## 📂 項目結構 (4個核心檔案)

```
Motion-Photos/
├── main.py              # 🔧 主要轉換工具
├── verify.py            # ✅ Motion Photo驗證工具  
├── setup.py             # 📦 環境設置和依賴安裝
├── demo.py              # 🎭 功能演示工具
├── README.md            # 📖 說明文檔
└── Demo.mp4             # 🎬 範例影片
```

## 🚀 快速開始

### 1. 環境設置
```bash
python setup.py
```

### 2. 轉換影片
```bash
python main.py your_video.mp4
```

### 3. 驗證結果
```bash
python verify.py your_video.MP.jpg
```

### 4. 查看演示
```bash
python demo.py
```

## 🛠️ 系統需求

### 必需工具
- **Python 3.6+**
- **ffmpeg**: 影片處理
- **exiftool**: 元數據處理

### 安裝方法
```bash
# macOS
brew install ffmpeg exiftool

# Ubuntu/Debian
sudo apt install ffmpeg exiftool
```

### Python依賴
- `lxml` (自動安裝)

## 📝 使用方法

### 基本轉換
```bash
# 自動生成檔名
python main.py Demo.mp4
# 輸出: Demo.MP.jpg

# 指定輸出檔名
python main.py Demo.mp4 my_photo.MP.jpg
```

### 批次處理
```bash
# 轉換多個影片
for video in *.mp4; do
    python main.py "$video"
done
```

## 📊 支援格式

### 輸入影片格式
- ✅ MP4, AVI, MOV, MKV
- ✅ 所有ffmpeg支援的格式

### 輸出格式  
- ✅ Motion Photo (.MP.jpg)
- ✅ 標準JPEG相容
- ✅ 內嵌MP4影片

## 🎯 最佳實踐

1. **檔案命名**: 使用描述性名稱
2. **影片品質**: 建議1080p以下以控制檔案大小
3. **影片長度**: 建議3-15秒
4. **存儲位置**: 避免OneDrive等雲端同步資料夾

## 📄 授權

MIT License