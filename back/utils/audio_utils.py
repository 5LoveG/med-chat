import os


def cleanup_file(file_path: str):
    """清理临时文件"""
    if os.path.exists(file_path):
        os.remove(file_path)
