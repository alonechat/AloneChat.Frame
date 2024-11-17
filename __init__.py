import os

# 获取脚本所在的绝对路径
script_path = os.path.abspath(__file__)

# 获取脚本所在的目录
script_dir = os.path.dirname(script_path)

with open('path.txt', 'w') as pathes:
    pathes.write(script_dir)
    print(f'This script is running at {script_dir}. DON\'T MOVE IT!')
    