#!/usr/bin/env python3
"""
Motion Photo 演示工具
展示Motion Photo的各種功能和特性
"""

import os
import sys
import subprocess
import re
from pathlib import Path

def show_banner():
    print("🎭 Motion Photo 演示")
    print("=" * 50)

def show_file_info(filepath):
    """顯示檔案基本信息"""
    print(f"📁 檔案: {filepath}")
    
    if not os.path.exists(filepath):
        print("❌ 檔案不存在")
        return False
    
    file_size = os.path.getsize(filepath)
    print(f"📊 大小: {file_size:,} bytes")
    return True

def demo_as_image(filepath):
    """演示作為JPEG圖片的功能"""
    print("\n1️⃣ 作為JPEG圖片顯示:")
    
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            print(f"   📷 圖片尺寸: {img.size}")
            print(f"   🎨 色彩模式: {img.mode}")
            print(f"   🖼️ 格式: {img.format}")
            print("   ✅ 可以正常顯示為靜態圖片")
            return True
    except ImportError:
        print("   📝 需要安裝Pillow: uv add Pillow")
        return False
    except Exception as e:
        print(f"   ❌ 無法讀取圖片: {e}")
        return False

def demo_metadata(filepath):
    """演示XMP元數據讀取"""
    print("\n2️⃣ 讀取Motion Photo元數據:")
    
    try:
        # 檢查所有XMP元數據
        result = subprocess.run([
            'exiftool', '-XMP:all', filepath
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            output = result.stdout
            
            # 檢查Motion Photo相關欄位
            motion_photo = None
            version = None
            timestamp = None
            
            for line in output.split('\n'):
                line = line.strip()
                if 'Motion Photo' in line and 'Version' not in line and 'Timestamp' not in line:
                    motion_photo = line.split(':')[-1].strip()
                elif 'Motion Photo Version' in line:
                    version = line.split(':')[-1].strip()
                elif 'Motion Photo Presentation Timestamp' in line:
                    timestamp = line.split(':')[-1].strip()
            
            if motion_photo == '1':
                print(f"   🎯 Motion Photo: {motion_photo}")
            if version == '1':
                print(f"   📋 版本: {version}")
            if timestamp == '0':
                print(f"   ⏰ 時間戳: {timestamp}")
            
            # 檢查Container信息
            if 'Primary' in output and 'MotionPhoto' in output:
                print("   ✅ 包含Primary圖片和MotionPhoto影片")
            if 'image/jpeg' in output:
                print("   🖼️ 主圖片: JPEG格式")
            if 'video/mp4' in output:
                print("   🎥 附加影片: MP4格式")
            
            return True
        else:
            print("   ❌ 無法讀取元數據")
            return False
            
    except FileNotFoundError:
        print("   📝 需要安裝exiftool: brew install exiftool")
        return False
    except Exception as e:
        print(f"   ❌ 讀取元數據失敗: {e}")
        return False

def demo_video_extraction(filepath):
    """演示影片提取功能"""
    print("\n3️⃣ 提取內嵌影片:")
    
    try:
        # 從原始XMP中獲取Container信息
        result = subprocess.run([
            'exiftool', '-b', '-XMP', filepath
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            xmp_content = result.stdout
            
            # 解析Container:Length信息
            length_matches = re.findall(r'<Container:Length>(\d+)</Container:Length>', xmp_content)
            
            if len(length_matches) >= 2:
                primary_size = int(length_matches[0])  # 第一個是Primary圖片
                video_size = int(length_matches[1])    # 第二個是MotionPhoto影片
                
                print(f"   📏 Primary圖片大小: {primary_size:,} bytes")
                print(f"   🎥 內嵌影片大小: {video_size:,} bytes")
                
                # 提取影片到臨時檔案
                temp_video = "demo_extracted.mp4"
                try:
                    with open(filepath, 'rb') as f:
                        # 跳到影片數據的開始位置（Primary圖片之後）
                        f.seek(primary_size)
                        video_data = f.read(video_size)
                    
                    # 檢查影片數據是否有效
                    if len(video_data) == video_size and len(video_data) > 8:
                        with open(temp_video, 'wb') as f:
                            f.write(video_data)
                        
                        print(f"   ✅ 影片已提取: {temp_video}")
                        
                        # 嘗試分析影片信息
                        try:
                            result = subprocess.run([
                                'ffprobe', '-v', 'quiet', '-select_streams', 'v:0',
                                '-show_entries', 'stream=width,height,duration',
                                '-of', 'csv=p=0', temp_video
                            ], capture_output=True, text=True)
                            
                            if result.returncode == 0:
                                info = result.stdout.strip().split(',')
                                if len(info) >= 3:
                                    width, height, duration = info
                                    print(f"   📐 影片解析度: {width}x{height}")
                                    print(f"   ⏱️ 影片時長: {float(duration):.2f}秒")
                                else:
                                    print("   ✅ 影片檔案有效")
                        except FileNotFoundError:
                            print("   📝 需要ffprobe來分析影片詳情")
                        except Exception as e:
                            print(f"   ⚠️ 影片分析失敗: {e}")
                        
                        # 清理臨時檔案
                        try:
                            os.remove(temp_video)
                            print(f"   🗑️ 已清理臨時檔案")
                        except:
                            pass
                        
                        return True
                    else:
                        print("   ❌ 影片數據無效")
                        return False
                
                except Exception as e:
                    print(f"   ❌ 提取影片失敗: {e}")
                    return False
            
            elif len(length_matches) == 1:
                print("   ⚠️ 只找到一個Length值，可能缺少影片數據")
                return False
            else:
                print("   ⚠️ 未找到Container:Length信息")
                return False
        else:
            print("   ❌ 無法獲取XMP內容")
            return False
            
    except Exception as e:
        print(f"   ❌ 提取影片時發生錯誤: {e}")
        return False

def demo_file_structure(filepath):
    """演示檔案結構分析"""
    print("\n4️⃣ 檔案結構分析:")
    
    try:
        with open(filepath, 'rb') as f:
            # 檢查JPEG頭
            f.seek(0)
            header = f.read(10)
            if header[:2] == b'\xff\xd8':
                print("   ✅ JPEG SOI (Start of Image) 標記")
                
                # 檢查APP1段（可能包含XMP）
                f.seek(2)
                while True:
                    marker = f.read(2)
                    if not marker:
                        break
                    if marker == b'\xff\xe1':  # APP1
                        length_bytes = f.read(2)
                        if len(length_bytes) == 2:
                            app1_length = int.from_bytes(length_bytes, 'big')
                            print(f"   ✅ APP1段 (長度: {app1_length} bytes)")
                            
                            # 檢查是否為XMP
                            identifier = f.read(29)  # Adobe XMP identifier length
                            if b'http://ns.adobe.com/xap/1.0/' in identifier:
                                print("   ✅ XMP元數據段")
                            break
                        else:
                            break
                    else:
                        # 跳過其他段
                        if marker[0] == 0xff:
                            length_bytes = f.read(2)
                            if len(length_bytes) == 2:
                                length = int.from_bytes(length_bytes, 'big')
                                f.seek(length - 2, 1)
                            else:
                                break
                        else:
                            break
            
            # 檢查檔案末尾
            f.seek(-16, 2)
            end_bytes = f.read(16)
            print(f"   📄 檔案末尾16字節: {end_bytes.hex()}")
            
            # 檢查是否可能是MP4數據
            if b'ftyp' in end_bytes or b'moov' in end_bytes or b'mdat' in end_bytes:
                print("   🎥 檔案末尾可能包含MP4影片數據")
            else:
                print("   📄 檔案末尾數據格式未知")
            
        return True
        
    except Exception as e:
        print(f"   ❌ 分析檔案結構時發生錯誤: {e}")
        return False

def demo_compatibility(filepath):
    """演示相容性測試"""
    print("\n5️⃣ 相容性測試:")
    
    # 測試作為普通JPEG的相容性
    print("   🖼️ 普通JPEG查看器相容性:")
    try:
        from PIL import Image
        with Image.open(filepath):
            print("   ✅ Pillow可以正常開啟")
    except:
        print("   ❌ Pillow無法開啟")
    
    # 測試檔案大小合理性
    file_size = os.path.getsize(filepath)
    if file_size > 1000000:  # 1MB
        print(f"   📊 檔案大小: {file_size:,} bytes (包含影片數據)")
        print("   ✅ 檔案大小合理，包含影片數據")
    else:
        print(f"   📊 檔案大小: {file_size:,} bytes")
        print("   ⚠️ 檔案較小，可能不包含影片數據")
    
    return True

def run_demo(filepath):
    """執行完整演示"""
    show_banner()
    
    if not show_file_info(filepath):
        return False
    
    tests = [
        demo_as_image(filepath),
        demo_metadata(filepath),
        demo_video_extraction(filepath),
        demo_file_structure(filepath),
        demo_compatibility(filepath)
    ]
    
    print("\n" + "=" * 50)
    passed = sum(tests)
    total = len(tests)
    
    print(f"🎭 演示完成! {passed}/{total} 項功能正常")
    print("📱 此檔案在支援Motion Photos的應用程式中可看到動態效果")
    print("🖼️ 在一般圖片查看器中會顯示為靜態圖片")
    
    return passed == total

def main():
    if len(sys.argv) < 2:
        # 尋找可用的Motion Photo檔案
        mp_files = list(Path('.').glob('*.MP.jpg'))
        if mp_files:
            filepath = str(mp_files[0])
            print(f"🎯 自動選擇檔案: {filepath}")
        else:
            print("使用方法:")
            print("  python demo.py <Motion Photo檔案>")
            print("範例:")
            print("  python demo.py photo.MP.jpg")
            return
    else:
        filepath = sys.argv[1]
    
    run_demo(filepath)

if __name__ == "__main__":
    main()
