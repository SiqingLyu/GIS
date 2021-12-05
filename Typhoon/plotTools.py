import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import math
from sklearn.metrics import r2_score
# 字体
plt.rcParams['font.sans-serif']=['SimHei']
img = plt.imread('./hainan.png',100)
X_begin = 105
X_end = 117
Y_begin = 14
Y_end = 25
colors = ['#B7B7D4','#9B9BC3','#7575AC','#515197','#3C3C8A','#191975','#000066']
# 拟合函数
def func(x, a, b):
    #    y = a * log(x) + b
    y = x / (a * x + b)
    return y
class plotCurve():
    '''
    Use this Class to plot and save the pictures of the typhoon tracks
    '''
    def __init__(self, x_index, y_index, speed_index, pr_index,id_index):
        self.x_index = x_index
        self.y_index = y_index
        self.speed_index = speed_index
        self.pr_index = pr_index
        self.id_index = id_index
    def get_X(self):
        return self.x_index
    def get_Y(self):
        return self.y_index
    def get_Speed(self):
        return self.speed_index
    def get_Pr(self):
        return self.pr_index

    def show(self):

        # 拟合的坐标点
        x0 = self.x_index
        y0 = self.y_index
        speed = self.speed_index
        pr = self.pr_index
        # 坐标字体大小
        fig = plt.figure(figsize=(24, 11), dpi=200)
        ax = fig.add_subplot(121)
        # fig, ax = plt.subplots(1,2, figsize=(12, 11), dpi=200)

        ax.imshow(img, extent=[X_begin, X_end, Y_begin, Y_end])
        ax.tick_params(labelsize=11)
         # 原数据散点
        length = len(x0)
        for i in range(length):
            longitude = x0[i]
            latitude = y0[i]
            speed_temp = speed[i]
            min_speed = min(speed)

            color = colors[int((pr[i]/28.7) * 7)]
            ax.scatter(longitude,latitude,s=(speed_temp-min_speed+10)*100,marker='o',c=color,edgecolors='k')
        ax.plot(x0, y0, linestyle=':',marker = '.',color='k',linewidth=2)
        ax.set_title("{0}号台风路线图".format(int(self.id_index)),fontsize=30)
        ax.set_xlabel('经度',fontsize=25)
        ax.set_ylabel('纬度',fontsize=25)
        plt.grid(True, linestyle = "--", color = "g", linewidth = "0.5")

        ax2 = fig.add_subplot(122)
        X_speed = np.array(speed)
        Y_pr = np.array(pr)
        if min(X_speed) == max(X_speed):
            ax2.set_title('无拟合结果（数据不足）', fontsize=30)
        else:
            parameter = np.polyfit(X_speed, Y_pr, 1)
            x_simu = X_speed
            y_simu = parameter[0] * x_simu + parameter[1]
            ax2.scatter(X_speed, Y_pr, s=300, marker='o', c=color, edgecolors='k')
            ax2.plot(x_simu, y_simu, color='k', linewidth=2)
            ax2.set_xlim((min(X_speed) - 5, max(X_speed) + 5))
            ax2.set_ylim((min(Y_pr) - 1, max(Y_pr) + 1))
            ax2.set_xlabel('风速',fontsize = 25)
            ax2.set_ylabel('降雨量', fontsize = 25)

            ax2.set_title('最小二乘法拟合结果',fontsize = 30)

        plt.savefig('./Pics/TyphoonNo{0}.jpg'.format(int(self.id_index)))
        # plt.show()