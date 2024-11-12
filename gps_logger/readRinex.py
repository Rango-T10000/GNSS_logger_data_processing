#这个才是代码入口，调用另一个.py里面的函数
#1. 用手机gnss_logger采集的数据有.xxo文件和.txt文件，这两个文件放在gps_logger/log文件夹
#2. 自己从.txt文件把所有“Fix ......”的行都保存到自己建立的location.txt文件中，该文件也放在gps_logger/log文件夹
#3. 官网下载最新的星历数据.xxn，放在gps_logger/ephemeris_file文件夹
#4. 自行更替以下代码的文件路径

import os
import numpy as np
from math import cos, sin, sqrt, pi
from readNav import readRinexNav, getSatXYZ


def coordinateTrans(latitude, longitude, height):
    a = 6378137.0
    b = 6356752.31424518
    E = (a * a - b * b) / (a * a)
    COSLAT = cos(latitude * pi / 180)
    SINLAT = sin(latitude * pi / 180)
    COSLONG = cos(longitude * pi / 180)
    SINLONG = sin(longitude * pi / 180)
    N = a / (sqrt(1 - E * SINLAT * SINLAT))
    NH = N + height
    x = NH * COSLAT * COSLONG
    y = NH * COSLAT * SINLONG
    z = (b * b * N / (a * a) + height) * SINLAT
    return x, y, z

def myDate2JD(y: int, m: int, d: int, hh: int = 0, mm: int = 0, ss: float = 0.0):  # 日期转换
    if m in [1, 2]:
        m = m + 12
        y = y - 1
    B = 0
    if y > 1582 or (y == 1582 and m > 10) or (y == 1582 and m == 10 and d >= 15):
        B = 2 - int(y / 100) + int(y / 400)
    JD = int(365.25 * (y + 4712)) + int(30.61 * (m + 1)) + d - 63.5 + B
    JD = JD + hh / 24 + mm / 60 / 24 + ss / 60 / 60 / 24
    return JD


def getPPosition(timeP, s):
    f = open(s, 'r')
    latitude = -1
    longtitude = -1
    altitude = -1
    for line in f.readlines():
        contains = line.split(',')
        time = float(contains[-1])
        time = int((time) / 1000000000) % 604800

        if (time - timeP) == 0:
            # print(time, timeP)
            latitude = float(contains[2])
            longtitude = float(contains[3])
            altitude = float(contains[4])
            return latitude, longtitude, altitude
        if 0 < (time - timeP) <= 1:
            # print(time, timeP)
            latitude = float(contains[2])
            longtitude = float(contains[3])
            altitude = float(contains[4])
            return latitude, longtitude, altitude
        if 1 < (time - timeP) <= 2:
            # print(time, timeP)
            latitude = float(contains[2])
            longtitude = float(contains[3])
            altitude = float(contains[4])
            return latitude, longtitude, altitude
        if 2 < (time - timeP) <= 3:
            # print(time, timeP)
            latitude = float(contains[2])
            longtitude = float(contains[3])
            altitude = float(contains[4])
            return latitude, longtitude, altitude
    return latitude, longtitude, altitude




if __name__ == '__main__':
    n = 0
    flag = True
    lat = -1
    data = []
    nav = readRinexNav('gps_logger/ephemeris_file/brdc3170.24n')   #读取gps星历文件(去下载最新的)
    for filename in os.listdir('gps_logger/log'):
        if filename.find('gnss_log') != -1 and filename.find('txt') == -1: #寻找log目录下.xxo文件
            # n += 1
            f = open('gps_logger/log/' + filename, "r", encoding='utf-8')
            s = f.readline()
            while s:
                scontain = s.split()
                if s.find('>') != -1:
                    year = float(scontain[1])
                    month = float(scontain[2])
                    day = float(scontain[3])
                    hour = float(scontain[4])
                    minute = float(scontain[5])
                    second = float(scontain[6])
                    sn = int(scontain[-1])
                    time = scontain[1] + '-' + scontain[2] + '-' + scontain[3] + 'T' + scontain[4] + ':' + scontain[5] + ':' + scontain[6]
                    # calculate GPS time----------q------------------
                    UT = hour + (minute / 60.0) + (second / 3600)
                    # 需要将当前需计算的时刻先转换到儒略日再转换到GPS时间
                    JD = myDate2JD(year, month, day, hour, minute, second)
                    WN = int((JD - 2444244.5) / 7)  # WN:GPS_week number 目标时刻的GPS周
                    t_oc = int((JD - 2444244.5 - 7.0 * WN) * 24 * 3600.0)  # t_GPS:目标时刻的GPS秒
                    if flag:
                        t = t_oc - 4731
                        flag = False
                    lat, longt, alt = getPPosition(t_oc - t, 'gps_logger/log/location.txt')
                    x, y, z = coordinateTrans(lat, longt, alt)
                    if lat != -1:
                        n += 1
                    while sn > 0 and lat != -1:
                        s = f.readline()
                        print(s)
                        scontain = s.split()
                        sname = scontain[0]
                        # print(s)
                        if sname.find('G') != -1:
                            if s[6] != ' ':
                                sphase = scontain[2]
                                am = scontain[4]
                            else:
                                sphase = scontain[1]
                                am = scontain[3]

                            sphase = float(sphase) % 1
                            am = float(am)
                            # get satellite position
                            if sname.find('G') != -1:
                                snum = int(sname.replace('G', ''))
                                time = np.datetime64(time)
                                xyz = getSatXYZ(nav, snum, [time], t_oc)
                                # print(xyz)
                                data.append([x, y, z, xyz[0][0],xyz[0][1],xyz[0][2], sphase, am])
                        sn -= 1
                s = f.readline()
    len = len(data)
    data = np.array(data)
    np.random.shuffle(data)
    expname = 'exp-1'
    # train_data = data[0:int(len * 0.9), ...]
    # test_data = data[int(len * 0.9):, ...]
    savepath = os.path.join("gps_logger/output", expname)
    os.makedirs(savepath, exist_ok=True)
    # np.savetxt(os.path.join(savepath, "dataTrain.csv"), train_data, delimiter=',', fmt="%.17f",
    #            header="lat,longt,alt,sx,sy,sz,phase,am", comments="")
    # np.savetxt(os.path.join(savepath, "dataEval.csv"), test_data, delimiter=',', fmt="%.17f",
    #            header="lat,longt,alt,sx,sy,sz,phase,am", comments="")
    np.savetxt(os.path.join(savepath, "data.csv"), data, delimiter=',', fmt="%.17f",
               header="lat,longt,alt,sx,sy,sz,phase,am", comments="")   
