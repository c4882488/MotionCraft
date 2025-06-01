#!/usr/bin/env python3
"""
Motion Photo 轉換工具
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

def generate_xmp(jpeg_path, video_path):
    """生成符合Google Motion Photos規範的XMP元數據"""
    primary_image_size = os.path.getsize(jpeg_path)
    video_size = os.path.getsize(video_path)
    
    # 使用exiftool能識別的標準命名空間
    rdf_ns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    container_ns = "http://ns.google.com/photos/1.0/container/"
    camera_ns = "http://ns.google.com/photos/1.0/camera/"
    x_ns = "adobe:ns:meta/"

    NSMAP = {
        None: "adobe:ns:meta/",
        "rdf": rdf_ns,
        "Container": container_ns,
        "Camera": camera_ns  # 改回Camera以便exiftool識別
    }

    # 創建根元素
    xmpmeta = etree.Element(f"{{{x_ns}}}xmpmeta", nsmap=NSMAP)
    rdf = etree.SubElement(xmpmeta, f"{{{rdf_ns}}}RDF")
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

    return etree.tostring(xmpmeta, pretty_print=True, xml_declaration=True, encoding='utf-8')

def inject_xmp_metadata(jpeg_path, xmp_content):
    """將XMP元數據注入JPEG檔案"""
    print(f"📝 注入XMP元數據...")
    
    with open(jpeg_path, 'rb') as f:
        jpeg_data = f.read()
    
    if jpeg_data[:2] != b'\xff\xd8':
        raise ValueError("Invalid JPEG file")
    
    # 移除XML聲明
    xmp_lines = xmp_content.decode('utf-8').split('\n')
    xmp_rdf = '\n'.join([line for line in xmp_lines if not line.strip().startswith('<?xml')])
    
    # 創建XMP包
    xmp_packet = f'''<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
{xmp_rdf.strip()}
<?xpacket end="w"?>'''.encode('utf-8')
    
    # Adobe XMP標識符
    adobe_xmp_ns = b'http://ns.adobe.com/xap/1.0/\x00'
    
    # 構建XMP段
    xmp_length = len(xmp_packet) + len(adobe_xmp_ns) + 2
    if xmp_length > 65535:
        xmp_length = 65535
    
    xmp_segment = b'\xff\xe1' + xmp_length.to_bytes(2, 'big') + adobe_xmp_ns + xmp_packet
    
    # 插入XMP段到JPEG開頭
    new_jpeg = jpeg_data[:2] + xmp_segment + jpeg_data[2:]
    
    with open(jpeg_path, 'wb') as f:
        f.write(new_jpeg)
    
    print(f"✅ XMP元數據已注入")

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
        
        # 步驟2: 合併檔案
        append_video_to_jpeg(cover_path, str(video_path), str(output_path))
        
        # 步驟3: 生成並注入XMP
        xmp_content = generate_xmp(cover_path, str(video_path))
        inject_xmp_metadata(str(output_path), xmp_content)
        
        # 步驟4: 清理臨時檔案
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
