import numpy as np
import shapely, geopandas
from shapely.geometry import Polygon, MultiPoint
from tqdm import tqdm
import json
import time
def Cal_area_2polygon(data1, data2):
    '''
    TO extract the common area of two polygons
    :param data1: list or array which contains the index of the points of the polygon1
    :param data2: list or array which contains the index of the points of the polygon2
    :return: the common area and the propotion (IOU)
    '''
    polygon1 = Polygon(data1).convex_hull
    polygon2 = Polygon(data2).convex_hull
    if not polygon1.intersects(polygon2):
        inter_area = 0
    else:
        try:
            inter_area = polygon1.intersection(polygon2).area
        except shapely.geos.TopologicalError:
            print('shapely.geos.TopologicalError occured, inter_area set to 0')
            inter_area = 0
    return inter_area

def Cal_area_2shp(dict, dict_gt):
    '''
    the function is to use the function "Cal_area_2polygon"
    to calculate the total IOU of the shpfile
    :param dict: json type polygon of test file
    :param dict_gt: json type polygon of groung truth
    :return: total IOU and the amount of the use-able buildings
    '''
    inter_area_total = 0
    GT_area = 0
    amount = 0

    len_test = len(dict["features"])
    len_gt = len(dict_gt["features"])

    with tqdm(total=len_gt) as pbar:
        for i in range(0,len_gt):
            data_gt = dict_gt["features"][i]["geometry"]["coordinates"][0]
            GT_area += Polygon(data_gt).convex_hull.area
            for j in range(0,len_test):
                data = dict["features"][j]["geometry"]["coordinates"][0]
                inter_area = Cal_area_2polygon(data,data_gt)
                if inter_area > 0 :
                    inter_area_total += inter_area
                    amount += 1
            pbar.set_postfix(IOU= float(inter_area_total / GT_area), amount = amount)
            pbar.update()
            if i+1 % 10 == 0:
                print("For now the IOU is:")
    if inter_area_total > 0:
        IOU_total = float(inter_area_total) / GT_area
    return IOU_total, amount

def Cal_shp_area(dict):
    '''
    to calculate the area of a shp file
    :param dict: input shp file dictionary
    :return: total area
    '''
    area_total = 0
    len_dict = len(dict["features"])
    with tqdm(total=len_dict) as pbar:
        for i in range(0,len_dict):
            if dict["features"][i]["geometry"]["coordinates"][0].__len__() >= 3:
                data = dict["features"][i]["geometry"]["coordinates"][0]

                area_total += Polygon(data).convex_hull.area
                pbar.set_postfix(total_area = area_total)
                pbar.update()
    time.sleep(0.5)
    return area_total

def readShpFile(path):
    '''
    to read a shp file and convert the data to list type
    :param path:  file path where the target shp file is
    :return: a list which contains all the points and the polygons
    '''
    shp_f = geopandas.read_file(path)
    polygon = shp_f.geometry.to_json()
    polygon_dict = json.loads(polygon)
    return polygon_dict

def main():
    result = [['上海市','无数据','无数据','D:\\ArcMapAbout\\Data\\test\\TFshanghai.shp','D:\\ArcMapAbout\\Data\\test\\intersectSetP.shp','D:\\ArcMapAbout\\Data\\test\\intersectSH1.shp'],
              ['重庆市','无数据','无数据','D:\\ArcMapAbout\\Data\\test\\TFchongqing.shp','D:\\ArcMapAbout\\Data\\test\\intersectCQP.shp','D:\\ArcMapAbout\\Data\\test\\intersectCQP_BAIDU.shp']]
    #           ['青岛市',0,0,'D:\\ArcMapAbout\\Data\\test\\TFqingdao.shp','Null',                                          'D:\\ArcMapAbout\\Data\\test\\intersectQDP.shp']]
    # result = [ ['青岛市',0,0,'D:\\ArcMapAbout\\Data\\test\\TFqingdao.shp','Null',                                          'D:\\ArcMapAbout\\Data\\test\\intersectQDP.shp']]
    result_arr = np.array(result)
    for i in range(len(result)):

        path_gt = result[i][3]
        path_gd = result[i][4]
        path_bd = result[i][5]
        print("读取{0}的真值文件中...\nreading ground truth file ...".format(result[i][0]))
        polygon_dict2 = readShpFile(path_gt)
        print("正在运算对应总面积...\ncalculating total area ...")
        time.sleep(0.1)
        area_gt = Cal_shp_area(polygon_dict2)

        if path_gd != 'Null':
            print("读取高德地图测试文件中...\nreading test file ...")
            polygon_dict1 = readShpFile(path_gd)
            print("正在运算对应总面积...\ncalculating total area ...")
            time.sleep(0.1)
            area_intersect = Cal_shp_area(polygon_dict1)
            IOU = float(area_intersect) / (area_gt)
            time.sleep(0.2)
            print("{0} 在高德地图上的总IOU为\n\tIOU:{1}".format(result[i][0],IOU))
            result[i][1] = IOU
        if path_bd != 'Null':
            print("读取百度地图测试文件中...\nreading test file ...")
            polygon_dict1 = readShpFile(path_bd)
            print("正在运算对应总面积...\ncalculating total area ...")
            time.sleep(0.1)
            area_intersect = Cal_shp_area(polygon_dict1)
            IOU = float(area_intersect) / (area_gt)
            time.sleep(0.2)
            print("{0} 在百度地图上的总IOU为\n\tIOU:{1}".format(result[i][0],IOU))
            result[i][2] = IOU
    print('城市\t\t高德IOU\t\t\t\t\t百度IOU\n')
    for i in range(len(result)):
        print(result[i][0]+'\t'+ str(result[i][1]) +'\t\t'+ str(result[i][2]))
if __name__ == '__main__':
    main()
