import os

def change_file_extension(folder_path):
    # 获取文件夹内所有文件和子文件夹的路径
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_paths.append(os.path.join(root, file_name))
    
    # 遍历每个文件路径
    for file_path in file_paths:
        # 获取文件名和扩展名
        file_name, file_extension = os.path.splitext(file_path)
        
        # 如果扩展名不是txt，并且目标文件不存在，则重命名为txt格式
        if file_extension != '.txt' and not os.path.exists(file_name + '.txt'):
            new_file_path = file_name + '.txt'
            os.rename(file_path, new_file_path)
            print(f'文件 {file_path} 的扩展名已经修改为txt')
        
    print('所有文件的扩展名已经修改完成！')

# 请在下面输入文件夹路径
folder_path = input('请输入文件夹路径：')
change_file_extension(folder_path)