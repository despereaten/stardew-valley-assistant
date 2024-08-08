import os

def list_directories(path, level=2, current_level=1):
    if current_level > level:
        return
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            print('    ' * (current_level - 1) + '|-- ' + entry)
            list_directories(entry_path, level, current_level + 1)

# 设置你要检查的目录路径
root_path = r'C:\Users\wyx\Desktop\实训\客服\stardew-valley-assistant'

# 列出目录结构
list_directories(root_path)
