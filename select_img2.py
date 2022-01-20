# 将对应文件夹取出所需数量
from random import sample
import os
import shutil
# from pathos.multiprocessing import ProcessingPool as Pool
from multiprocessing import Pool
from functools import partial
import cv2


def get_dir(path, kind=True):  # 获取文件夹下路径
    filenames = os.listdir(path)
    filenames = sorted(filenames)
    if kind:
        pathnames = [os.path.join(path, filename) for filename in filenames]
        return pathnames
    else:
        return filenames


def copy_img(name, opath, tpath):  # 复制。name是文件名，opath tpath是目录
    opath1 = os.path.join(opath, name)
    tpath1 = os.path.join(tpath, name)

    if os.path.exists(opath1):
        shutil.copyfile(opath1, tpath1)
    else:
        print(name)


def copy_img_reshape(name, opath, tpath):  # 复制。name是文件名，opath tpath是目录
    opath1 = os.path.join(opath, name)
    tpath1 = os.path.join(tpath, name)

    if os.path.exists(opath1):
        # shutil.copyfile(opath1, tpath1)
        img = cv2.imread(opath1)
        img = cv2.resize(img, (1024, 576), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(tpath1, img)
    else:

        print(name)


if __name__ == '__main__':
    # 设置参数
    path_base = '/mnt/hdd/cherry2021/cherryDataSet'
    kind = 'test'
    num = 70  # 个数

    #
    opath = os.path.join(path_base, kind)
    # tpath = os.path.join(path_base, 'ran_' + kind)
    tpath = os.path.join(path_base, 're_ran_' + kind)

    if not os.path.exists(tpath):
        os.mkdir(tpath)

    filenames = get_dir(opath, False)
    print(filenames)
    ran_filenames = sample(filenames, num)
    # print(len(ran_filenames))

    # copy_img_p = partial(copy_img, opath=opath, tpath=tpath)
    copy_img_p = partial(copy_img_reshape, opath=opath, tpath=tpath) # 更改形状
    p = Pool()
    p.map(copy_img_p, ran_filenames)
