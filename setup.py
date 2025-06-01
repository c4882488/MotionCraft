#!/usr/bin/env python3
"""
MotionCraft - Environment Setup Tool
Check and install required dependencies
檢查並安裝所需的依賴套件
"""

import os
import sys
import subprocess
import platform

def print_banner():
    print("🛠️ Motion Photo 環境設置")
    print("=" * 50)

def check_system():
    """檢查系統信息"""
    print("📋 系統信息:")
    print(f"   操作系統: {platform.system()} {platform.release()}")
    print(f"   Python版本: {sys.version.split()[0]}")
    print(f"   當前目錄: {os.getcwd()}")
    print()

def check_command(command, name):
    """檢查命令是否可用"""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"   ✅ {name}: {version}")
            return True
        else:
            print(f"   ❌ {name}: 未安裝")
            return False
    except FileNotFoundError:
        print(f"   ❌ {name}: 未找到命令")
        return False

def check_python_module(module_name, import_name=None):
    """檢查Python模組"""
    if import_name is None:
        import_name = module_name
    
    try:
        __import__(import_name)
        print(f"   ✅ {module_name}: 已安裝")
        return True
    except ImportError:
        print(f"   ❌ {module_name}: 未安裝")
        return False

def check_dependencies():
    """檢查所有依賴"""
    print("🔍 檢查系統依賴:")
    
    # 檢查系統工具
    ffmpeg_ok = check_command('ffmpeg', 'FFmpeg')
    exiftool_ok = check_command('exiftool', 'ExifTool')
    
    print("\n🔍 檢查Python模組:")
    
    # 檢查Python模組
    lxml_ok = check_python_module('lxml')
    pillow_ok = check_python_module('Pillow', 'PIL')
    
    print()
    
    missing = []
    if not ffmpeg_ok:
        missing.append('ffmpeg')
    if not exiftool_ok:
        missing.append('exiftool')
    if not lxml_ok:
        missing.append('lxml')
    if not pillow_ok:
        missing.append('Pillow')
    
    return missing

def install_system_tools():
    """安裝系統工具"""
    print("📦 安裝系統工具:")
    
    if platform.system() == 'Darwin':  # macOS
        print("   🍺 使用Homebrew安裝...")
        
        # 檢查Homebrew
        try:
            subprocess.run(['brew', '--version'], capture_output=True, check=True)
            print("   ✅ Homebrew已安裝")
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("   ❌ Homebrew未安裝，請先安裝: https://brew.sh")
            return False
        
        # 安裝ffmpeg
        print("   📹 安裝FFmpeg...")
        result = subprocess.run(['brew', 'install', 'ffmpeg'], capture_output=True)
        if result.returncode == 0:
            print("   ✅ FFmpeg安裝完成")
        else:
            print("   ⚠️ FFmpeg安裝可能有問題")
        
        # 安裝exiftool
        print("   📝 安裝ExifTool...")
        result = subprocess.run(['brew', 'install', 'exiftool'], capture_output=True)
        if result.returncode == 0:
            print("   ✅ ExifTool安裝完成")
        else:
            print("   ⚠️ ExifTool安裝可能有問題")
            
    elif platform.system() == 'Linux':
        print("   🐧 Linux系統，請手動安裝:")
        print("   sudo apt-get install ffmpeg exiftool  # Ubuntu/Debian")
        print("   sudo yum install ffmpeg exiftool      # CentOS/RHEL")
        
    else:
        print("   ❓ 不支援的系統，請手動安裝FFmpeg和ExifTool")

def install_python_modules():
    """安裝Python模組"""
    print("\n🐍 安裝Python模組:")
    
    # 檢查是否有uv
    has_uv = False
    try:
        subprocess.run(['uv', '--version'], capture_output=True, check=True)
        has_uv = True
        print("   ✅ 使用uv安裝...")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("   📦 使用pip安裝...")
    
    modules = ['lxml', 'Pillow']
    
    for module in modules:
        print(f"   📦 安裝{module}...")
        
        if has_uv:
            cmd = ['uv', 'add', module]
        else:
            cmd = [sys.executable, '-m', 'pip', 'install', module]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ {module}安裝完成")
        else:
            print(f"   ❌ {module}安裝失敗: {result.stderr}")

def setup_environment():
    """完整環境設置"""
    print_banner()
    check_system()
    
    missing = check_dependencies()
    
    if not missing:
        print("🎉 所有依賴都已準備就緒!")
        return True
    
    print(f"⚠️ 缺少依賴: {', '.join(missing)}")
    print()
    
    # 詢問是否自動安裝
    try:
        response = input("是否要自動安裝缺少的依賴? (y/N): ").strip().lower()
        if response in ['y', 'yes', '是']:
            # 安裝系統工具
            if 'ffmpeg' in missing or 'exiftool' in missing:
                install_system_tools()
            
            # 安裝Python模組
            if 'lxml' in missing or 'Pillow' in missing:
                install_python_modules()
            
            print("\n🔄 重新檢查依賴...")
            missing_after = check_dependencies()
            
            if not missing_after:
                print("\n🎉 環境設置完成! 所有依賴都已安裝!")
                return True
            else:
                print(f"\n⚠️ 仍缺少: {', '.join(missing_after)}")
                print("請手動安裝或檢查錯誤信息")
                return False
        else:
            print("手動安裝指南:")
            print("=" * 30)
            if 'ffmpeg' in missing:
                print("🍺 安裝FFmpeg: brew install ffmpeg")
            if 'exiftool' in missing:
                print("🍺 安裝ExifTool: brew install exiftool")
            if 'lxml' in missing:
                print("🐍 安裝lxml: uv add lxml 或 pip install lxml")
            if 'Pillow' in missing:
                print("🐍 安裝Pillow: uv add Pillow 或 pip install Pillow")
            return False
            
    except KeyboardInterrupt:
        print("\n👋 設置已取消")
        return False

def test_installation():
    """測試安裝是否成功"""
    print("\n🧪 測試功能...")
    
    # 測試轉換功能
    if os.path.exists('Demo.mp4'):
        print("   🎬 測試影片轉換...")
        result = subprocess.run([sys.executable, 'main.py', 'Demo.mp4'], 
                              capture_output=True)
        if result.returncode == 0:
            print("   ✅ 轉換功能正常")
            
            # 測試驗證功能
            if os.path.exists('Demo.MP.jpg'):
                print("   🔍 測試驗證功能...")
                result = subprocess.run([sys.executable, 'verify.py', 'Demo.MP.jpg'], 
                                      capture_output=True)
                if result.returncode == 0:
                    print("   ✅ 驗證功能正常")
                else:
                    print("   ⚠️ 驗證功能可能有問題")
        else:
            print("   ⚠️ 轉換功能可能有問題")
    else:
        print("   ℹ️ 沒有測試影片檔案，請手動測試")

def main():
    """主程序"""
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        # 只檢查，不安裝
        print_banner()
        check_system()
        missing = check_dependencies()
        
        if not missing:
            print("🎉 所有依賴都已準備就緒!")
        else:
            print(f"⚠️ 缺少依賴: {', '.join(missing)}")
            print("運行 'python setup.py' 來自動安裝")
    else:
        # 完整設置
        success = setup_environment()
        if success:
            test_installation()

if __name__ == "__main__":
    main()
