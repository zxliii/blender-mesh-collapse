import math
import os.path
import sys
import traceback
import bpy

total_count = 0
success_count = 0

def compress_file(input: str, output: str = '', scale: float = 0.5, threshold: int = 0) -> None:
    if not input or input == '' or input.isspace() or not os.path.exists(input):
        print(f'操作失败，传入的input路径为空，或者路径不存在:{input}')
        return

    if not output or output == '' or output.isspace():
        per = math.floor(scale * 100)
        output = input.replace('.fbx', f'{per}off.fbx')
        output = output.replace('.FBX', f'{per}off.FBX')

    outdir = os.path.dirname(output)
    if (not os.path.exists(outdir)):
        os.mkdir(outdir)

    try:
        # 清空当前场景
        bpy.ops.wm.read_factory_settings(use_empty=True)
        # 导入FBX文件
        bpy.ops.import_scene.fbx(filepath=input)

        obj_names = []
        for o in bpy.context.selected_objects:
            obj_names.append(o.name)
        print(','.join(obj_names))

        polygon_count_old = 0
        polygon_count_new = 0

        for obj in bpy.context.selected_objects:

            if not obj.data.polygons:
                continue

            polygon_count_old += len(obj.data.polygons)
            if threshold > 0 and polygon_count_old < threshold:
                print(f"操作被阻止，物体 {obj.name} 的面数为：{polygon_count_old},没到指定的阈值{threshold}")
                return

            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_add(type='DECIMATE')
            bpy.context.object.modifiers["Decimate"].ratio = scale
            bpy.ops.object.modifier_apply(modifier="Decimate")
            bpy.ops.object.mode_set(mode='OBJECT')
            polygon_count_new += len(obj.data.polygons)

        bpy.ops.export_scene.fbx(filepath=output)

        print(f'操作成功，面数由{polygon_count_old}减为{polygon_count_new},减少了{round((polygon_count_new - polygon_count_old) / polygon_count_old * 100, 1)}%')

    except Exception as e:
        print(f'异常操作，文件{input}\n{e}')


def compress_dir(input: str, output: str = '', scale: float = 0.5, threshold: int = 0) -> None:

    if not input or input == '' or input.isspace() or not os.path.exists(input):
        print(f'操作失败，传入的input路径为空，或者路径不存在:{input}')
        return

    if os.path.isdir(output) and os.path.exists(output):
        os.mkdir(output)

    for filepath, dirnames, filenames in os.walk(input):
        for folder in dirnames:
            diri = os.path.join(filepath, folder)
            fbx_exists = False
            for fn in os.listdir(diri):
                if fn.lower().endswith('.fbx'):
                    fbx_exists = True
                    break

            if not fbx_exists:
                continue

            diro = os.path.join(output, folder) if os.path.isdir(output) else ''
            if os.path.isdir(diro) and not os.path.exists(diro):
                os.mkdir(diro)

            for fn in os.listdir(diri):
                if fn.lower().endswith('.fbx'):
                    fni = os.path.join(diri, fn)
                    fno = os.path.join(diro, fn) if os.path.isdir(diro) else ''
                    compress_file(fni, fno, scale, threshold)

if __name__ == '__main__':

    try:
        length = len(sys.argv)
        if length < 2:
            print('parameter could not below than 2.')
            exit()
        comp = None
        params = sys.argv[1:]
        num = len(params)
        input = params[0]
        output = params[1] if num > 1 else ''

        if os.path.isdir(input):
            compress_dir(*params)
        elif os.path.isfile(input):
            compress_file(*params)

    except KeyboardInterrupt:
        print('手动退出！')
    except Exception as e:
        traceback.print_exc()