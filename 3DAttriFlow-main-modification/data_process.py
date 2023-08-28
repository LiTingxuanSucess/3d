# 处理数据集的过程传入的是ply文件夹
from vtk import vtkUnsignedCharArray
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkWindowToImageFilter
)
from vtkmodules.vtkIOImage import (
    vtkBMPWriter,
    vtkJPEGWriter,
    vtkPNGWriter,
    vtkPNMWriter,
    vtkPostScriptWriter,
    vtkTIFFWriter
)
import math
import os
import numpy as np
import os
import vtk

def ply_to_stl(ply_patch):
    import os
    import trimesh
    # 源文件夹路径
    source_folder = ply_patch
    # 目标文件夹路径
    target_folder = './out/stl'
    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)
    # 获取源文件夹中的所有文件
    file_list = os.listdir(source_folder)
    # 遍历文件列表
    for file_name in file_list:
        # 构建源文件的完整路径
        source_file = os.path.join(source_folder, file_name)
        # 检查文件是否为PLY文件
        if file_name.lower().endswith('.ply'):
            # 读取PLY文件
            mesh = trimesh.load_mesh(source_file)
            # 构建目标文件的完整路径
            target_file = os.path.join(target_folder, file_name[:-4] + '.stl')
            # 将PLY转换为STL并保存
            mesh.export(target_file, file_type='stl')
def transform(ply_patch):

    ply_to_stl(ply_patch)
    # 输入文件夹路径和输出文件夹路径
    input_folder = './out/stl'
    output_folder = './out/new_stl'

    # 创建输出文件夹，如果不存在的话
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # 读取输入文件夹中的所有文件
    file_list = os.listdir(input_folder)
    # 遍历每个文件
    for file_name in file_list:
        # 构建输入文件的完整路径
        input_file_path = os.path.join(input_folder, file_name)
        # 创建一个STL读取器
        reader = vtk.vtkSTLReader()
        reader.SetFileName(input_file_path)
        reader.Update()
        # 获取点云数据
        point_cloud = reader.GetOutput()
        # 获取点云数据的中心坐标
        center = point_cloud.GetCenter()
        # 计算平移向量，使点云数据移动到坐标原点
        translation = vtk.vtkTransform()
        translation.Translate(-center[0], -center[1], -center[2])
        # 应用平移变换到点云数据
        transform_filter = vtk.vtkTransformPolyDataFilter()
        transform_filter.SetInputData(point_cloud)
        transform_filter.SetTransform(translation)
        transform_filter.Update()

        # 输出文件名，保持与输入文件相同
        output_file_name = file_name

        # 构建输出文件的完整路径
        output_file_path = os.path.join(output_folder, output_file_name)

        # 创建一个STL写入器
        writer = vtk.vtkSTLWriter()
        writer.SetFileName(output_file_path)
        writer.SetInputData(transform_filter.GetOutput())
        writer.Write()
def vtk_test(input_pach):
    colors = vtkNamedColors()
        # 读取输入文件夹中的所有文件
    file_list = os.listdir(input_pach)
    # 遍历每个文件
    for file_name in file_list:
        # 构建输入文件的完整路径
        input_file_path = os.path.join(input_pach, file_name)
        path = input_file_path
        # filename = get_program_parameters()
        reader = vtkSTLReader()
        reader.SetFileName(path)
        reader.Update()


        # 获取渲染的数据对象
        polyData = reader.GetOutput()

        # 根据物理坐标计算颜色值，并设置给每个点
        vcolors = vtkUnsignedCharArray()
        vcolors.SetNumberOfComponents(3)
        vcolors.SetName("Colors")
        vcolors.SetNumberOfTuples(polyData.GetNumberOfPoints())
        # print('polyData.GetNumberOfPoints()=',polyData.GetNumberOfPoints())
        # 假设 BBOX 的最小点和最大点为 minPoint 和 maxPoint
        minPoint = polyData.GetBounds()[0:3]  # (minX, minY, minZ)
        maxPoint = polyData.GetBounds()[3:6]  # (maxX, maxY, maxZ)

        newCenterX = (minPoint[0] + maxPoint[0]) / 2
        newCenterY = (minPoint[1] + maxPoint[1]) / 2
        newCenterZ = (minPoint[2] + maxPoint[2]) / 2


        # 假设 BBOX 的最小点和最大点为 minPoint 和 maxPoint
        bounds = polyData.GetBounds()
        minPoint = np.array([bounds[0], bounds[2], bounds[4]])  # (minX, minY, minZ)
        maxPoint = np.array([bounds[1], bounds[3], bounds[5]])  # (maxX, maxY, maxZ)

        diagonalLength = np.linalg.norm(maxPoint - minPoint)  # 对角线长度
        scalePara = 1.0 / diagonalLength

        for i in range(polyData.GetNumberOfPoints()):
            tempNOCS_x = ((polyData.GetPoint(i)[0] - newCenterX) * scalePara + 0.5) * 255
            tempNOCS_y = ((polyData.GetPoint(i)[1] - newCenterY) * scalePara + 0.5) * 255
            tempNOCS_z = ((polyData.GetPoint(i)[2] - newCenterZ) * scalePara + 0.5) * 255
            vcolors.SetTuple3(i,tempNOCS_x,tempNOCS_y,tempNOCS_z)

        polyData.GetPointData().SetScalars(vcolors)

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(polyData)

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetSpecular(0.3)
        actor.GetProperty().SetSpecularPower(60.0)


        # 创建背面属性对象
        backFaceP = vtk.vtkProperty()
        backFaceP.SetColor(0.3, 0.3, 0.3)  # 设置颜色为灰色
        backFaceP.SetOpacity(0.7)  # 设置不透明度为0.7

        # 将背面属性对象应用于第二个演员
        actor.SetBackfaceProperty(backFaceP)

        # Create a rendering window and renderer
        ren = vtkRenderer()
        renWin = vtkRenderWindow()
        renWin.AddRenderer(ren)
        renWin.SetSize(137, 137)
        renWin.SetWindowName('ReadSTL')

        # Create a renderwindowinteractor
        iren = vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)

        # Assign actor to the renderer
        ren.AddActor(actor)
        white_color = (0.0, 0.0, .0)  # 自定义颜色为白色
        ren.SetBackground(white_color)
        # ren.GetActiveCamera().Zoom(1.5)


        sphereXSet = []
        sphereYSet = []
        sphereZSet = []
        arcInterval = math.pi / 10.0
        theta = 0.0
        while theta <= 2 * math.pi:
            phi = arcInterval
            while phi <= math.pi/2 :
                if abs(theta - math.pi / 2) <= 0.018 and abs(phi - math.pi / 2) <= 0.01:
                    phi += arcInterval
                    continue
                sphereXSet.append(math.sin(phi) * math.cos(theta))
                sphereYSet.append(math.sin(phi) * math.sin(theta))
                sphereZSet.append(math.cos(phi))
                phi += arcInterval
            theta += arcInterval

        # for i in range(len(sphereXSet)):
        #     print(f"Point {i + 1}: ({sphereXSet[i]}, {sphereYSet[i]}, {sphereZSet[i]})")
        # print(file_name[0:22])
        file_name = file_name.replace(".stl", "")
        path_png = 'out_png/'+file_name+"/rendering"

        if not os.path.exists(path_png ):
            os.makedirs(path_png)
        for i in range(len(sphereXSet)): 
                ren.GetActiveCamera().SetPosition(sphereXSet[i],sphereYSet[i],sphereZSet[i])
                ren.GetActiveCamera().SetViewUp(0,1,0)
                renWin.SetOffScreenRendering(1)
                ren.ResetCamera()
                renWin.Render()

                w2if = vtkWindowToImageFilter()
                w2if.SetInput(renWin)
                w2if.Update()
                path1 = str(i)+".png"
                if i<10:
                    i = "0" + str(i) 
                    path1 = i +".png"
                else:
                    path1 = str(i)+".png"

                filename = os.path.join(path_png,path1)
                writer = vtkPNGWriter()
                writer.SetFileName(filename)
                writer.SetInputData(w2if.GetOutput())
                writer.Write()

        # Enable user interface interactor
        iren.Initialize()
        renWin.Render()
        # iren.Start()
        renWin.Finalize()

import os
import numpy as np
import trimesh

def stl_to_npy(input_folder, output_folder):
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的STL文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".stl"):
            stl_path = os.path.join(input_folder, filename)

            # 读取STL文件
            stl_mesh = trimesh.load_mesh(stl_path)

            # 提取顶点数据
            vertices = stl_mesh.vertices

            # 构建输出文件路径
            output_filename = os.path.splitext(filename)[0] +".points.ply"+ ".npy"
            output_path = os.path.join(output_folder, output_filename)

            # 保存为Numpy文件
            np.save(output_path, vertices)

def random_upsample_pointcloud(pointcloud, target_point_count):
    if len(pointcloud) >= target_point_count:
        return pointcloud

    indices = np.random.choice(len(pointcloud), target_point_count, replace=True)
    upsampled_pointcloud = pointcloud[indices]

    return upsampled_pointcloud

def upsample_pointcloud_folder(input_folder, output_folder, target_point_count):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.npy'):
            file_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            pointcloud = np.load(file_path)

            if len(pointcloud) < target_point_count:
                upsampled_pointcloud = random_upsample_pointcloud(pointcloud, target_point_count)
                np.save(output_path, upsampled_pointcloud)



if __name__ == '__main__':
    # ply_patch = "jaw"
    # transform(ply_patch)

    # ply_patch = "tooch"
    # transform(ply_patch)
    # input_pach =  "out/new_stl"
    # vtk_test(input_pach)
    # # 指定输入和输出文件夹路径
    input_folder = "out/new_stl"
    output_folder = "out/npy_1"

    # 执行STL转换为Numpy文件操作
    stl_to_npy(input_folder, output_folder)
    # 设置输入文件夹和输出文件夹路径
    # input_folder = 'out/npy_1'
    # output_folder = 'out/out_npy'
    # target_point_count = 30000  # 设置目标点数
    # 将输入文件夹中点云数据数小于30000的文件进行上采样，保存到输出文件夹中
    # upsample_pointcloud_folder(input_folder, output_folder, target_point_count)









# import os
# import re

# def remove_symbols(filename):
#     # 定义要移除的符号列表
#     symbols = ["-", "_", "."]  # 根据需要添加其他符号

#     # 使用正则表达式去除符号
#     pattern = "[" + re.escape("".join(symbols)) + "]"
#     new_filename = re.sub(pattern, "", filename)
    
#     return new_filename

# def rename_files(folder_path):
#     # 遍历文件夹中的文件
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             # 获取文件名和扩展名
#             filename, ext = os.path.splitext(file)
            
#             # 去除符号并重新命名文件
#             new_filename = remove_symbols(filename)
#             new_file = new_filename + ext
            
#             # 构建新的文件路径
#             old_path = os.path.join(root, file)
#             new_path = os.path.join(root, new_file)
            
#             # 重命名文件
#             os.rename(old_path, new_path)

# # 指定要遍历的文件夹路径
# folder_path = "jaw"

# # 执行文件重命名操作
# rename_files(folder_path)