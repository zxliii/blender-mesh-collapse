import bpy
import os

def compress_fbx(input_dir, output_dir, scale=0.1):
    # 如果输出目录不存在，则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取输入目录下的所有FBX文件
    fbx_files = [f for f in os.listdir(input_dir) if f.endswith('.fbx')]

    for fbx_file in fbx_files:
        # 构建文件路径
        input_path = os.path.join(input_dir, fbx_file)
        output_filename = os.path.splitext(fbx_file)[0] + '_col.fbx'
        output_path = os.path.join(output_dir, output_filename)

        # 清空当前场景
        bpy.ops.wm.read_factory_settings(use_empty=True)

        # 导入FBX文件
        bpy.ops.import_scene.fbx(filepath=input_path)

        # 选择所有对象并缩放
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.transform.resize(value=(scale, scale, scale))

        # 应用变换
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # 清理和三角化网格
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)  # 修复法线
                bpy.ops.mesh.quads_convert_to_tris()  # 三角化网格
                bpy.ops.object.mode_set(mode='OBJECT')

        # 导出FBX文件
        bpy.ops.export_scene.fbx(filepath=output_path)

# 获取脚本所在目录
input_dir = os.path.dirname(os.path.realpath(__file__))
# 指定输出目录
output_dir = os.path.join(input_dir, 'Compressed')

# 压缩比例
scale = 0.2

# 执行压缩操作
compress_fbx(input_dir, output_dir, scale)
