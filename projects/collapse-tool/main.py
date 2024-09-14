import os
import traceback


if __name__ == '__main__':

    try:

        root_dir = '~/work/github/blender-mesh-collapse/res/chesses'

        files = os.listdir(root_dir)

        for f in files:
            print(f)




    except KeyboardInterrupt:
        print('手动退出！')
    except Exception as e:
        traceback.print_exc()
