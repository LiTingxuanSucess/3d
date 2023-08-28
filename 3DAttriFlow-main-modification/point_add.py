# import open3d as o3d
# import numpy as np

# # 读取PLY文件
# input_file = "predict_test.ply"
# point_cloud = o3d.io.read_point_cloud(input_file)

# # 获取点云数据
# points = np.asarray(point_cloud.points)

# # 指定上采样后的点数
# desired_point_count = 30000  # 根据需要设置期望的点数

# # 计算上采样的体素大小
# voxel_size = np.max(points, axis=0) / np.cbrt(desired_point_count)

# # 进行上采样处理
# upsampled_point_cloud = point_cloud.voxel_down_sample(voxel_size=voxel_size)

# # 确保生成指定数量的点
# while len(upsampled_point_cloud.points) < desired_point_count:
#     upsampled_point_cloud += point_cloud.voxel_down_sample(voxel_size=voxel_size)

# # 保留指定数量的点
# upsampled_point_cloud.points = o3d.utility.Vector3dVector(np.asarray(upsampled_point_cloud.points)[:desired_point_count])

# # 保存为新的PLY文件
# output_file = "output.ply"
# o3d.io.write_point_cloud(output_file, upsampled_point_cloud)

import open3d as o3d
import numpy as np

# 读取PLY文件
input_file = "predict_test.ply"
point_cloud = o3d.io.read_point_cloud(input_file)

# 检查顶点是否包含NaN坐标，并去除无效顶点
points = np.asarray(point_cloud.points)
valid_indices = np.logical_not(np.any(np.isnan(points), axis=1))
valid_points = points[valid_indices]

# 指定上采样后的点数
desired_point_count = 30000  # 根据需要设置期望的点数

# 进行上采样处理
upsampled_points = []
for i in range(desired_point_count):
    voxel_points = valid_points[np.random.choice(len(valid_points))]
    upsampled_points.append(voxel_points)

# 创建上采样后的点云
upsampled_point_cloud = o3d.geometry.PointCloud()
upsampled_point_cloud.points = o3d.utility.Vector3dVector(upsampled_points)

# 保存为新的PLY文件
output_file = "output.ply"
o3d.io.write_point_cloud(output_file, upsampled_point_cloud)