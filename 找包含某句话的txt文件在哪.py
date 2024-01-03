import os

def search_files(folder_path, sentence):
    found_files = []  # 创建一个列表，用于存储满足条件的文件路径
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        contents = f.read()
                        if sentence in contents:
                            found_files.append(file_path)  # 将满足条件的文件路径添加到列表中
                except UnicodeDecodeError:
                    pass
    for file_path in found_files:  # 打印列表中的所有文件路径
        print("你要找的句子位于", file_path)

# 获取用户输入的文件夹路径和句子
folder_path = input("请输入文件夹路径：")
sentence = input("请输入要查找的句子：")

# 调用函数进行查找
search_files(folder_path, sentence)