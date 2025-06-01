#!/usr/bin/env python3
"""
MotionCraft - Motion Photo Conversion Tool
Transform videos into Google Motion Photos format with automatic cleanup
將影片轉換為Google Motion Photos格式，並自動清理臨時檔案
"""

import subprocess
import os
import sys
import argparse
from pathlib import Path
from lxml import etree

def extract_frame(video_path, output_path):
    """從影片提取JPEG封面"""
    print(f"🎬 從影片提取封面: {video_path}")
    result = subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-ss", "00:00:00.500", "-vframes", "1", output_path
    ], capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to extract frame: {result.stderr.decode()}")
    print(f"✅ 封面已提取: {output_path}")

def append_video_to_jpeg(jpeg_path, video_path, output_path):
    """將影片數據附加到JPEG檔案"""
    print(f"🔗 合併JPEG和影片數據...")
    with open(jpeg_path, 'rb') as f_jpeg:
        jpeg_data = f_jpeg.read()
    with open(video_path, 'rb') as f_video:
        video_data = f_video.read()

    with open(output_path, 'wb') as f_out:
        f_out.write(jpeg_data)
        f_out.write(video_data)

    print(f"✅ 檔案合併完成: {len(video_data):,} bytes 影片數據")
    return len(jpeg_data)

# 舊的 generate_xmp() 函數已移除，請使用 generate_xmp_with_size() 代替

def generate_xmp_with_size(primary_image_size, video_path):
    """使用指定的主要圖片大小生成XMP元數據"""
    video_size = os.path.getsize(video_path)
    
    # 使用與正常Motion Photos相同的命名空間結構
    rdf_ns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    container_ns = "http://ns.google.com/photos/1.0/container/"
    camera_ns = "http://ns.google.com/photos/1.0/camera/"

    NSMAP = {
        "rdf": rdf_ns,
        "Container": container_ns,  # 使用Container前綴（不是GContainer）
        "Camera": camera_ns         # 使用Camera前綴（不是GCamera）
    }

    # 創建根元素 - 直接使用RDF，不需要xmpmeta包裝
    rdf = etree.Element(f"{{{rdf_ns}}}RDF", nsmap=NSMAP)
    desc = etree.SubElement(rdf, f"{{{rdf_ns}}}Description")
    desc.set(f"{{{rdf_ns}}}about", "")

    # Camera metadata - 使用Camera命名空間
    etree.SubElement(desc, f"{{{camera_ns}}}MotionPhoto").text = "1"
    etree.SubElement(desc, f"{{{camera_ns}}}MotionPhotoVersion").text = "1"
    etree.SubElement(desc, f"{{{camera_ns}}}MotionPhotoPresentationTimestampUs").text = "0"

    # Container directory
    container_dir = etree.SubElement(desc, f"{{{container_ns}}}Directory")
    seq = etree.SubElement(container_dir, f"{{{rdf_ns}}}Seq")
    
    # Primary image item
    primary_li = etree.SubElement(seq, f"{{{rdf_ns}}}li")
    primary_item = etree.SubElement(primary_li, f"{{{container_ns}}}Item")
    etree.SubElement(primary_item, f"{{{container_ns}}}Mime").text = "image/jpeg"
    etree.SubElement(primary_item, f"{{{container_ns}}}Semantic").text = "Primary"
    etree.SubElement(primary_item, f"{{{container_ns}}}Length").text = str(primary_image_size)
    
    # Motion Photo video item
    video_li = etree.SubElement(seq, f"{{{rdf_ns}}}li")
    video_item = etree.SubElement(video_li, f"{{{container_ns}}}Item")
    etree.SubElement(video_item, f"{{{container_ns}}}Mime").text = "video/mp4"
    etree.SubElement(video_item, f"{{{container_ns}}}Semantic").text = "MotionPhoto"
    etree.SubElement(video_item, f"{{{container_ns}}}Length").text = str(video_size)

    return etree.tostring(rdf, pretty_print=True, xml_declaration=False, encoding='utf-8')

def inject_xmp_metadata(jpeg_path, xmp_content):
    """將XMP元數據注入JPEG檔案"""
    print(f"📝 注入XMP元數據...")
    
    with open(jpeg_path, 'rb') as f:
        jpeg_data = f.read()
    
    if jpeg_data[:2] != b'\xff\xd8':
        raise ValueError("Invalid JPEG file")
    
    # 先移除現有的XMP段（如果有的話）
    cleaned_jpeg = remove_existing_xmp(jpeg_data)
    
    # 創建XMP包 - 與正常Motion Photos格式相同
    xmp_packet = f'''<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
{xmp_content.decode('utf-8').strip()}
<?xpacket end="w"?>'''.encode('utf-8')
    
    # Adobe XMP標識符
    adobe_xmp_ns = b'http://ns.adobe.com/xap/1.0/\x00'
    
    # 構建XMP段
    xmp_length = len(xmp_packet) + len(adobe_xmp_ns) + 2
    if xmp_length > 65535:
        raise ValueError("XMP data too large")
    
    xmp_segment = b'\xff\xe1' + xmp_length.to_bytes(2, 'big') + adobe_xmp_ns + xmp_packet
    
    # 插入XMP段到JPEG開頭
    new_jpeg = cleaned_jpeg[:2] + xmp_segment + cleaned_jpeg[2:]
    
    with open(jpeg_path, 'wb') as f:
        f.write(new_jpeg)
    
    print(f"✅ XMP元數據已注入")

def remove_existing_xmp(jpeg_data):
    """移除JPEG中現有的XMP段"""
    if len(jpeg_data) < 4:
        return jpeg_data
    
    result = jpeg_data[:2]  # 保留JPEG標頭
    i = 2
    
    while i < len(jpeg_data) - 1:
        if jpeg_data[i] == 0xFF:
            marker = jpeg_data[i + 1]
            
            if marker == 0xE1:  # APP1 段（可能包含XMP）
                if i + 4 < len(jpeg_data):
                    length = int.from_bytes(jpeg_data[i + 2:i + 4], 'big')
                    segment_end = i + 2 + length
                    
                    # 檢查是否為XMP段
                    if segment_end <= len(jpeg_data):
                        segment_data = jpeg_data[i + 4:segment_end]
                        if segment_data.startswith(b'http://ns.adobe.com/xap/1.0/\x00'):
                            # 跳過XMP段
                            i = segment_end
                            continue
                
                # 不是XMP段，保留
                if i + 4 < len(jpeg_data):
                    length = int.from_bytes(jpeg_data[i + 2:i + 4], 'big')
                    segment_end = i + 2 + length
                    if segment_end <= len(jpeg_data):
                        result += jpeg_data[i:segment_end]
                        i = segment_end
                    else:
                        result += jpeg_data[i:]
                        break
                else:
                    result += jpeg_data[i:]
                    break
            
            elif marker in [0xE0, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xEB, 0xEC, 0xED, 0xEE, 0xEF]:
                # 其他APP段
                if i + 4 < len(jpeg_data):
                    length = int.from_bytes(jpeg_data[i + 2:i + 4], 'big')
                    segment_end = i + 2 + length
                    if segment_end <= len(jpeg_data):
                        result += jpeg_data[i:segment_end]
                        i = segment_end
                    else:
                        result += jpeg_data[i:]
                        break
                else:
                    result += jpeg_data[i:]
                    break
            
            elif marker == 0xDA:  # SOS段，圖像數據開始
                result += jpeg_data[i:]
                break
            
            else:
                result += jpeg_data[i:i + 2]
                i += 2
        else:
            result += jpeg_data[i:i + 1]
            i += 1
    
    return result

def convert_to_motion_photo(video_path, output_path=None):
    """轉換影片為Motion Photo"""
    video_path = Path(video_path)
    
    if not video_path.exists():
        print(f"❌ 找不到影片檔案: {video_path}")
        return False
    
    # 自動生成輸出檔名
    if output_path is None:
        output_path = video_path.with_suffix('.MP.jpg')
    
    print(f"🎯 轉換 {video_path} → {output_path}")
    
    # 臨時檔案
    cover_path = "cover.jpg"
    
    try:
        # 步驟1: 提取封面
        extract_frame(str(video_path), cover_path)
        
        # 步驟2: 生成初始XMP來估算大小
        temp_xmp = generate_xmp_with_size(os.path.getsize(cover_path), str(video_path))
        inject_xmp_metadata(cover_path, temp_xmp)
        
        # 步驟3: 計算包含XMP後的實際主要圖片大小
        primary_image_with_xmp_size = os.path.getsize(cover_path)
        video_size = os.path.getsize(str(video_path))
        
        print(f"📏 主要圖片大小 (含XMP): {primary_image_with_xmp_size:,} bytes")
        print(f"📏 影片大小: {video_size:,} bytes")
        
        # 步驟4: 生成最終正確的XMP元數據
        final_xmp = generate_xmp_with_size(primary_image_with_xmp_size, str(video_path))
        inject_xmp_metadata(cover_path, final_xmp)
        
        # 步驟5: 最終合併檔案
        append_video_to_jpeg(cover_path, str(video_path), str(output_path))
        
        # 步驟6: 清理臨時檔案
        if os.path.exists(cover_path):
            os.remove(cover_path)
            print(f"🗑️ 已清理臨時檔案: {cover_path}")
        
        print(f"🎉 Motion Photo 已創建: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 轉換失敗: {e}")
        # 清理臨時檔案
        if os.path.exists(cover_path):
            os.remove(cover_path)
        return False

def main():
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python main.py <影片檔案> [輸出檔案.MP.jpg]")
        print("範例:")
        print("  python main.py video.mp4")
        print("  python main.py video.mp4 output.MP.jpg")
        return
    
    video_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_to_motion_photo(video_file, output_file)

if __name__ == "__main__":
    main()
