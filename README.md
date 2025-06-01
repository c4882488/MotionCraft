# MotionCraft 🎬✨

> *Seamlessly transform videos into Google Motion Photos with precision and elegance*

Transform your videos into stunning Motion Photos that comply with Google's Motion Photos 1.0 specification. MotionCraft brings the magic of living photographs to your fingertips.

## 🌟 Features

- 📱 **Full Google Motion Photos 1.0 Compliance** - Perfect compatibility with supported apps
- 🎯 **Smart Auto-naming** - `video.mp4` → `video.MP.jpg` automatically
- 🧹 **Auto-cleanup** - Temporary files cleaned up automatically
- 🔍 **Comprehensive Validation** - Built-in verification tools
- 💻 **Simple CLI Interface** - Easy-to-use command line tools
- 🎭 **Interactive Demo** - Showcase all features with live examples

## 📂 Project Structure (4 Core Files)

```
MotionCraft/
├── main.py              # 🔧 Core conversion engine
├── verify.py            # ✅ Motion Photo validator  
├── setup.py             # 📦 Environment setup & dependencies
├── demo.py              # 🎭 Interactive feature showcase
├── README.md            # 📖 Documentation
└── Demo.mp4             # 🎬 Sample video
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
python setup.py
```

### 2. Convert Video
```bash
python main.py your_video.mp4
```

### 3. Validate Result
```bash
python verify.py your_video.MP.jpg
```

### 4. Run Demo
```bash
python demo.py
```

## 🛠️ System Requirements

### Required Tools
- **Python 3.6+**
- **ffmpeg**: Video processing engine
- **exiftool**: Metadata manipulation tool

### Installation
```bash
# macOS
brew install ffmpeg exiftool

# Ubuntu/Debian
sudo apt install ffmpeg exiftool

# Windows (using Chocolatey)
choco install ffmpeg exiftool
```

### Python Dependencies
- `lxml` (automatically installed)

## 📝 Usage Guide

### Basic Conversion
```bash
# Auto-generate filename
python main.py Demo.mp4
# Output: Demo.MP.jpg

# Custom output filename
python main.py Demo.mp4 my_motion_photo.MP.jpg
```

### Batch Processing
```bash
# Convert multiple videos
for video in *.mp4; do
    python main.py "$video"
done
```

### Advanced Options
```bash
# Verify Motion Photo integrity
python verify.py photo.MP.jpg

# Interactive feature demonstration
python demo.py photo.MP.jpg

# Auto-detect and demo available Motion Photos
python demo.py
```

## 📊 Supported Formats

### Input Video Formats
- ✅ MP4, AVI, MOV, MKV, WMV
- ✅ All ffmpeg-supported formats
- ✅ Various codecs and resolutions

### Output Format  
- ✅ Motion Photo (.MP.jpg)
- ✅ Standard JPEG compatibility
- ✅ Embedded MP4 video stream
- ✅ XMP metadata with Google Container specification

## 🎯 Best Practices

### Video Specifications
- **Resolution**: Recommended 1080p or lower for optimal file size
- **Duration**: 3-15 seconds works best
- **Quality**: Balance between file size and visual quality
- **Frame Rate**: 30fps recommended

### File Management
- **Naming**: Use descriptive filenames
- **Storage**: Avoid cloud sync folders during processing
- **Backup**: Keep original videos as backup
- **Organization**: Group related Motion Photos together

## 🔍 Technical Details

### Motion Photo Structure
```
Motion Photo File (.MP.jpg)
├── JPEG Image (Primary)
│   ├── SOI Marker (0xFFD8)
│   ├── APP1 Segment (XMP Metadata)
│   └── Image Data
└── MP4 Video (MotionPhoto)
    ├── ftyp box
    ├── moov box
    └── mdat box
```

### XMP Metadata Schema
- **Container Directory**: Google Photos 1.0 specification
- **Camera Metadata**: Motion Photo flags and version
- **Semantic Items**: Primary image and MotionPhoto video
- **Length Information**: Precise byte offsets for each component

## 🎭 Demo Features

The interactive demo showcases:

1. **🖼️ JPEG Compatibility** - Display as static image
2. **📊 Metadata Analysis** - XMP structure examination  
3. **🎥 Video Extraction** - Live video data recovery
4. **🔧 File Structure** - Binary format analysis
5. **✅ Compatibility Testing** - Cross-platform validation

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Google for the Motion Photos specification
- FFmpeg team for video processing capabilities
- ExifTool for metadata manipulation
- Python community for excellent libraries

---

**MotionCraft** - *Where videos come alive in photographs* ✨
