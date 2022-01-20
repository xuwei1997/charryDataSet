# 将 训练 测试 验证 移动到对应的文件夹
import numpy as np
import os
import shutil
import datetime
# from pathos.multiprocessing import ProcessingPool as Pool
from multiprocessing import Pool
from functools import partial


def create_assist_date(datestart=None, dateend=None):
    # 创建日期辅助表

    if datestart is None:
        datestart = '2016-01-01'
    if dateend is None:
        dateend = datetime.datetime.now().strftime('%Y-%m-%d')

    # 转为日期格式
    datestart = datetime.datetime.strptime(datestart, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(dateend, '%Y-%m-%d')
    date_list = []
    date_list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend:
        # 日期叠加一天
        datestart += datetime.timedelta(days=+1)
        # 日期转字符串存入列表
        date_list.append(datestart.strftime('%Y-%m-%d'))
    # print(date_list)
    return date_list


def rename_img(dates, points, times):  # 更改文件名
    s = str(points) + '_' + dates + '_' + str(times) + '.jpg'
    return s


def copy_img(name, opath, tpath, dir_name):  # 复制。name是文件名，opath tpath是目录
    opath1 = os.path.join(opath, name)
    oname = dir_name + name
    tpath1 = os.path.join(tpath, oname)

    if os.path.exists(opath1):
        shutil.copyfile(opath1, tpath1)
    else:
        print(name)


if __name__ == '__main__':
    # 训练 测试 验证 220 100 50

    # 设置参数
    path_base = '/mnt/hdd/cherry2021'
    dir_name = 'E88570046'
    datestart = '2021-02-05'
    datesend = '2021-04-25'
    # point_liat = ['2','7']
    point_liat = range(3,6)
    time_list = ['09', '12', '15']
    kind = 'train'

    #
    opath = os.path.join(path_base, dir_name)
    tpath = os.path.join(path_base, 'cherryDataSet', kind)
    print(opath)
    print(tpath)

    for point in point_liat:
        for time in time_list:
            print(point, time)

            if not os.path.exists(tpath):
                os.mkdir(tpath)

            # 获取文件名列表
            data_list = create_assist_date(datestart, datesend)
            rename_img_p = partial(rename_img, points=point, times=time)
            name_list = map(rename_img_p, data_list)
            name_list0 = list(name_list)
            print(name_list0)

            # 复制多线程
            copy_img_p = partial(copy_img, opath=opath, tpath=tpath, dir_name=dir_name)
            p = Pool()
            p.map(copy_img_p, name_list0)
