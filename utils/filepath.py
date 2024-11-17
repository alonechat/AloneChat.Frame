import os

# 获取脚本所在的绝对路径
script_path = os.path.abspath(__file__)

# 获取脚本所在的目录
script_dir = os.path.dirname(script_path)

print(script_dir)