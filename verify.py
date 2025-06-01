#!/usr/bin/env python3
"""
Motion Photo 驗證工具
驗證Motion Photo檔案是否符合Google Motion Photos 1.0規範
"""

import os
import sys
import subprocess
from pathlib import Path

def check_filename(filepath):
    """檢查檔案名稱是否符合規範"""
    print("1️⃣ 檔案名稱檢查:")
    if filepath.endswith('.MP.jpg'):
        print("   ✅ 檔案名稱符合規範 (*MP.jpg)")
        return True
    else:
        print("   ❌ 檔案名稱不符合規範，應以 .MP.jpg 結尾")
        return False

def check_file_type(filepath):
    """檢查檔案是否為有效的JPEG"""
    print("2️⃣ 檔案類型檢查:")
    try:
        with open(filepath, 'rb') as f:
            header = f.read(2)
            if header == b'\xff\xd8':
                print("   ✅ 檔案是有效的JPEG")
                return True
            else:
                print("   ❌ 檔案不是有效的JPEG格式")
                return False
    except Exception as e:
        print(f"   ❌ 無法讀取檔案: {e}")
        return False

def check_xmp_metadata(filepath):
    """檢查XMP元數據"""
    print("3️⃣ XMP元數據檢查:")
    try:
        # 檢查所有XMP元數據
        result = subprocess.run([
            'exiftool', '-XMP:all', filepath
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            output = result.stdout
            
            # 檢查Motion Photo相關欄位（可能在不同命名空間下）
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
                print("   ✅ MotionPhoto = 1")
            else:
                print(f"   ❌ MotionPhoto = {motion_photo} (應為 1)")
                return False
                
            if version == '1':
                print("   ✅ MotionPhotoVersion = 1")
            else:
                print(f"   ❌ MotionPhotoVersion = {version} (應為 1)")
                return False
                
            if timestamp == '0':
                print("   ✅ MotionPhotoPresentationTimestampUs = 0")
            else:
                print(f"   ❌ MotionPhotoPresentationTimestampUs = {timestamp} (應為 0)")
                return False
                
            return True
        else:
            print("   ❌ 無法讀取XMP元數據")
            return False
            
    except FileNotFoundError:
        print("   ❌ 需要安裝exiftool: brew install exiftool")
        return False
    except Exception as e:
        print(f"   ❌ 檢查XMP元數據時發生錯誤: {e}")
        return False

def check_container_directory(filepath):
    """檢查Container目錄結構"""
    print("4️⃣ Container目錄檢查:")
    try:
        # 檢查原始XMP內容
        result = subprocess.run([
            'exiftool', '-b', '-XMP', filepath
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            xmp_content = result.stdout
            
            # 檢查XMP內容中的關鍵元素
            has_directory = 'Container:Directory' in xmp_content
            has_primary = 'Primary' in xmp_content
            has_motion_photo_semantic = 'MotionPhoto' in xmp_content
            has_image_jpeg = 'image/jpeg' in xmp_content
            has_video_mp4 = 'video/mp4' in xmp_content
            
            if has_directory:
                print("   ✅ Container:Directory結構存在")
                
                if has_primary:
                    print("   ✅ 找到Primary語意項目")
                if has_motion_photo_semantic:
                    print("   ✅ 找到MotionPhoto語意項目")
                if has_image_jpeg:
                    print("   ✅ 找到image/jpeg MIME類型")
                if has_video_mp4:
                    print("   ✅ 找到video/mp4 MIME類型")
                
                return has_primary and has_motion_photo_semantic and has_image_jpeg and has_video_mp4
            else:
                print("   ❌ Container:Directory結構缺失")
                return False
        else:
            print("   ❌ 無法讀取XMP元數據")
            return False
            
    except Exception as e:
        print(f"   ❌ 檢查Container目錄時發生錯誤: {e}")
        return False

def check_file_structure(filepath):
    """檢查檔案結構"""
    print("5️⃣ 檔案結構檢查:")
    try:
        file_size = os.path.getsize(filepath)
        print(f"   📊 總檔案大小: {file_size:,} bytes")
        
        with open(filepath, 'rb') as f:
            # 檢查JPEG SOI標記
            f.seek(0)
            soi = f.read(2)
            if soi == b'\xff\xd8':
                print("   ✅ 檔案開頭有正確的JPEG SOI標記")
            else:
                print("   ❌ 檔案開頭缺少JPEG SOI標記")
                return False
            
            # 檢查檔案末尾（可能是影片數據）
            f.seek(-8, 2)
            end_bytes = f.read(8)
            print(f"   📄 檔案末尾: {end_bytes.hex()}")
            
        return True
        
    except Exception as e:
        print(f"   ❌ 檢查檔案結構時發生錯誤: {e}")
        return False

def verify_motion_photo(filepath):
    """完整驗證Motion Photo檔案"""
    if not os.path.exists(filepath):
        print(f"❌ 找不到檔案: {filepath}")
        return False
    
    print(f"🔍 驗證Motion Photo檔案: {filepath}")
    print("=" * 60)
    
    checks = [
        check_filename(filepath),
        check_file_type(filepath),
        check_xmp_metadata(filepath),
        check_container_directory(filepath),
        check_file_structure(filepath)
    ]
    
    print("\n" + "=" * 60)
    
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print("🎉 Motion Photo驗證完成! 所有檢查都通過!")
        return True
    else:
        print(f"⚠️ 驗證完成: {passed}/{total} 項檢查通過")
        return False

def main():
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python verify.py <Motion Photo檔案>")
        print("範例:")
        print("  python verify.py photo.MP.jpg")
        return
    
    filepath = sys.argv[1]
    verify_motion_photo(filepath)

if __name__ == "__main__":
    main()
