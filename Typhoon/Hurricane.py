import xlrd
import numpy as np
import plotTools
import matplotlib
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

'''

读取表格文件数据

'''
workbook = xlrd.open_workbook('.\hurricane.xlsx')
data = workbook.sheet_by_name('Sheet1')
nrow = data.nrows
ncol = data.ncols
data_list = []
temp_list = []
typhoon_list = []
typhoon_num = 0
id = data.row_values(1)[0]
speed = []
rain = []

'''
从表格提取每个台风的信息
'''
for i in range(1, nrow):
    row_data = data.row_values(i)
    if data.row_values(i)[0] != id:
        typhoon_num += 1
        typhoon_list.append(temp_list)
        id = row_data[0]
        temp_list = []

    data_list.append(row_data)
    temp_list.append(row_data)
    speed.append(row_data[6])
    rain.append(row_data[7])


'''
风雨数据总拟合图
'''
X_speed = np.array(speed)
Y_rain = np.array(rain)
plt.xlabel('风速（m/s）',fontsize = 15)
plt.ylabel('降雨量(mm/h)',fontsize = 15)
plt.xlim(min(X_speed) - 5, max(X_speed) + 5)
plt.ylim(min(Y_rain) - 1, max(Y_rain) + 1)
parameter = np.polyfit(X_speed, Y_rain, 1)
x_simu = X_speed
y_simu = parameter[0] * x_simu + parameter[1]
plt.scatter(X_speed, Y_rain, s=30, marker='o', c='#00CED1', edgecolors='k')
plt.title('1998-2020海南省风雨相关性最小二乘法拟合结果',fontsize = 12)
plt.plot(x_simu, y_simu, color='#DC143C', linewidth=2)
plt.text(max(X_speed)-2, max(Y_rain)- 1 , 'y = %.5fx + %.5f'% (parameter[0],parameter[1]), va = 'bottom', ha = 'right' ,fontsize = 13)
plt.savefig('./海南省风雨拟合.jpg',dpi=200)

'''

对每一个台风的轨迹以及数据拟合

'''
for typhoon in typhoon_list:
    index = np.array(typhoon)
    if len(index) >= 3:
        latitude = index[:, 2]
        longitude = index[:, 3]
        speed = index[:, 6]
        pr = index[:, 7]
        id = index[0, 0]
        print(id)
        plotTools.plotCurve(longitude, latitude, speed, pr, id).show()


