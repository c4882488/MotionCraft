# ⚡ MotionCraft Quick Start Guide

Get up and running with MotionCraft in under 5 minutes!

## 🎯 Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.6 or higher
- [ ] A video file to convert (.mp4, .mov, .avi, etc.)
- [ ] Internet connection for dependency installation

## 🚀 Installation (One Command)

```bash
python setup.py
```

This will automatically:
- ✅ Check Python version
- ✅ Install required dependencies
- ✅ Verify FFmpeg installation
- ✅ Verify ExifTool installation
- ✅ Run system compatibility tests

## 🎬 Convert Your First Video

### Basic Usage
```bash
python main.py your_video.mp4
```

### Example with Sample Video
```bash
python main.py Demo.mp4
# Creates: Demo.MP.jpg
```

### Custom Output Name
```bash
python main.py vacation.mp4 memories.MP.jpg
# Creates: memories.MP.jpg
```

## ✅ Verify Your Motion Photo

```bash
python verify.py Demo.MP.jpg
```

Expected output:
```
🔍 Verifying Motion Photo: Demo.MP.jpg
============================================================
1️⃣ Filename Check: ✅
2️⃣ File Type Check: ✅ 
3️⃣ XMP Metadata Check: ✅
4️⃣ Container Directory Check: ✅
5️⃣ File Structure Check: ✅
============================================================
🎉 Motion Photo validation complete! All checks passed!
```

## 🎭 Interactive Demo

Explore all features:
```bash
python demo.py
# Auto-detects available Motion Photos

# Or specify a file:
python demo.py Demo.MP.jpg
```

Demo features:
- 📷 JPEG image display
- 📊 Metadata analysis
- 🎥 Video extraction
- 🔧 File structure examination
- ✅ Compatibility testing

## 📱 View Your Motion Photo

### On Mobile Devices
1. Transfer the `.MP.jpg` file to your phone
2. Open in **Google Photos** app
3. Tap and hold to see the motion effect

### On Desktop
- **As Static Image**: Any image viewer
- **With Motion**: Google Photos web interface

## 🎯 Pro Tips

### Best Video Formats
```bash
# Recommended input formats:
python main.py video.mp4    # ✅ Best compatibility
python main.py clip.mov     # ✅ High quality
python main.py record.avi   # ✅ Good support
```

### Batch Processing
```bash
# Convert all MP4 files in current directory:
for video in *.mp4; do
    python main.py "$video"
done
```

### Quality Optimization
```bash
# For smaller file sizes, compress video first:
ffmpeg -i large_video.mp4 -crf 28 -preset fast compressed.mp4
python main.py compressed.mp4
```

## 🛠️ Troubleshooting

### Common Issues & Solutions

**❌ "FFmpeg not found"**
```bash
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt install ffmpeg

# Windows:
choco install ffmpeg
```

**❌ "ExifTool not found"**
```bash
# macOS:
brew install exiftool

# Ubuntu/Debian:
sudo apt install exiftool
```

**❌ "Permission denied"**
```bash
chmod +x main.py verify.py demo.py setup.py
```

**❌ "Module not found: lxml"**
```bash
pip install lxml
# or
python setup.py  # Will install automatically
```

## 📊 Verification Checklist

After conversion, your Motion Photo should:
- [ ] Display as regular JPEG in any image viewer
- [ ] Show motion effect in Google Photos app
- [ ] Pass all 5 verification checks
- [ ] Maintain original video quality
- [ ] Include proper XMP metadata

## 🎉 Success!

You've successfully created your first Motion Photo with MotionCraft! 

**Next Steps:**
- 📱 Transfer to mobile device and test in Google Photos
- 🔄 Try batch converting multiple videos
- 🎭 Explore the interactive demo features
- 📚 Read the full documentation in README.md

---

**Need Help?** Check out `PROJECT_DETAILS.md` for technical details or open an issue on GitHub.

**MotionCraft** - *Your videos, beautifully crafted into living photographs* ✨
