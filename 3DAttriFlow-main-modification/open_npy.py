import numpy as np
from plyfile import PlyData, PlyElement

# 加载 npy 文件
point_cloud = np.load('out/out_npy/211119001lowerjaw20211119113742.points.ply.npy')

# 将 numpy 数组转换为点云数据
vertices = np.zeros(point_cloud.shape[0], dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
vertices['x'] = point_cloud[:, 0]
vertices['y'] = point_cloud[:, 1]
vertices['z'] = point_cloud[:, 2]

# 创建 PlyData 对象并保存为 ply 文件
ply_data = PlyData([PlyElement.describe(vertices, 'vertex')])
ply_data.write('./point_cloud.ply')

# **********************************************
# import os
# import numpy as np

# import os
# import numpy as np

# def find_file_with_least_points(folder_path):
#     min_points = float('inf')
#     min_points_file = None

#     # 遍历文件夹中的文件
#     for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)

#         # 检查文件是否为npy文件
#         if filename.endswith(".npy"):
#             # 从npy文件加载数据
#             points = np.load(file_path)

#             # 获取点的数量
#             num_points = points.shape[0]

#             # 更新最小点数和文件路径
#             if num_points < min_points:
#                 min_points = num_points
#                 min_points_file = file_path
#     print(min_points)
#     return min_points_file

# # 指定文件夹路径
# folder_path = "out/npy_1"

# # 查找具有最少点数的文件
# result_file = find_file_with_least_points(folder_path)

# if result_file:
#     print("文件中最少点数的文件是:", result_file)
# else:
#     print("文件夹中没有找到npy文件。")



# import os
# import random
# import numpy as np

# def random_downsample_npy_files(input_folder, output_folder, target_num_points):
#     # 遍历输入文件夹中的文件
#     for filename in os.listdir(input_folder):
#         input_file_path = os.path.join(input_folder, filename)

#         # 检查文件是否为npy文件
#         if filename.endswith(".npy"):
#             # 从npy文件加载数据
#             points = np.load(input_file_path)

#             # 获取当前点的数量
#             num_points = points.shape[0]

#             # 随机选择下采样的点索引
#             indices = random.sample(range(num_points), target_num_points)

#             # 根据选择的索引进行下采样
#             downsampled_points = points[indices]

#             # 构建输出文件路径
#             output_file_path = os.path.join(output_folder, filename)

#             # 保存下采样后的数据到新的npy文件
#             np.save(output_file_path, downsampled_points)

# # 指定输入文件夹路径、输出文件夹路径和目标点数
# input_folder = "out/npy_1"
# output_folder = "out/out_npy"
# target_num_points = 30000

# # 创建输出文件夹（如果不存在）
# os.makedirs(output_folder, exist_ok=True)

# # 对npy文件进行随机下采样并保存到新的文件夹中
# random_downsample_npy_files(input_folder, output_folder, target_num_points)