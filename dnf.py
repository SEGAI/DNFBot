import win32gui, win32ui, win32con, win32api
from PIL import ImageGrab 
import cv2
from lib.pywin import keyIo 
import time
import random
import numpy

class GameAssist:

    def __init__(self, wdname):
        """初始化"""
        self.key_press = keyIo().key_press
        # 取得窗口句柄
        self.hwnd = win32gui.FindWindow(0, wdname)
        if not self.hwnd:
            print("窗口找不到，请确认窗口句柄名称：【%s】" % wdname )
            exit()
        # 窗口显示最前面
        win32gui.SetForegroundWindow(self.hwnd)
        time.sleep(2)
        hwnd = self.hwnd
        win32gui.SetForegroundWindow(hwnd)
        hwndDC = win32gui.GetWindowDC(hwnd)

        # 获取监控器信息
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        # print(left, top, right, bottom)
        self.scree_left_and_right_point = (left, top, right, bottom)
        self.width = right - left
        self.height = bottom - top - 270

        self.mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        self.saveDC = self.mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        self.saveBitMap = win32ui.CreateBitmap()
        # 为bitmap开辟空间
        self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.width, self.height)
        # 高度saveDC，将截图保存到saveBitmap中
        self.saveDC.SelectObject(self.saveBitMap)
        # cor1, img1, dif1 = self.findActive()

        #         #内存释放
        # win32gui.DeleteObject(saveBitMap.GetHandle())
        # saveDC.DeleteDC()
        # mfcDC.DeleteDC()
        # win32gui.ReleaseDC(hWnd,hWndDC)\
        # self.GrandWave()
        self.findChar()



    def findChar(self):
        target = self.screenshot()
        target = cv2.threshold(target,250,255,cv2.THRESH_BINARY)[1]
        template = cv2.imread('./lv.jpg')
        template = cv2.threshold(template,250,255,cv2.THRESH_BINARY)[1]
        cv2.imwrite('level.jpg', template)

        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        theight, twidth = template.shape[:2]
        #执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
        result = cv2.matchTemplate(target,template,cv2.TM_SQDIFF_NORMED)
        #归一化处理
        cv2.normalize( result, result, 0, 1, cv2.NORM_MINMAX, -1 )
        #寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        #匹配值转换为字符串
        #对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近与0匹配度越好，匹配位置取min_loc
        #对于其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc
        strmin_val = str(min_val)
        #绘制矩形边框，将匹配区域标注出来
        #min_loc：矩形定点
        #(min_loc[0]+twidth,min_loc[1]+theight)：矩形的宽高
        #(0,0,225)：矩形的边框颜色；2：矩形边框宽度
        cv2.rectangle(target,min_loc,(min_loc[0]+twidth,min_loc[1]+theight),(0,0,225),2)
        cv2.imshow('1', target)
        cv2.waitKey()
        # 人物坐标
        x = min_loc[0] + 60
        y = max_loc[1] + 150
        return (x, y)

    def findActive(self):
        img1 = self.screenshot()
        time.sleep(1/60)
        img2 = self.screenshot()
        diff = cv2.absdiff(img1, img2)
        diff = cv2.threshold(diff,25,255,cv2.THRESH_BINARY)[1]
        diff = cv2.dilate(diff,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,4)),iterations = 2)

        cnts,hierarchy = cv2.findContours(diff.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        act_cordinate = []
        for c in cnts:
            if cv2.contourArea(c) < 2000:
               continue
            #c是一个二值图，boundingRect是矩形边框函数，用一个最小的矩形，把找到的形状包起来；
            #x,y是矩形左上点的坐标；w,h是矩阵的宽和高
            (x,y,w,h) = cv2.boundingRect(c)
            #rectangle画出矩形，frame是原图，(x,y)是矩阵的左上点坐标，(x+w,y+h)是矩阵右下点坐标
            #(0,255,0)是画线对应的rgb颜色，2是画线的线宽
            # cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),2)
            #目标坐标
            act_cordinate.append((x + w / 2, y + h))
        return act_cordinate, img1, diff

    
    def screenshot(self):
        """屏幕截图"""
        
        # 截取从左上角（0，0）长宽为（w，h）的图片
        self.saveDC.BitBlt((0, 0), (self.width, self.height), self.mfcDC, (0, 200), win32con.SRCCOPY)
        signedIntsArray = self.saveBitMap.GetBitmapBits(True)
        im_opencv = numpy.frombuffer(signedIntsArray, dtype = 'uint8')
        im_opencv.shape = (self.height, self.width, 4)
        image = cv2.cvtColor(im_opencv, cv2.COLOR_RGB2GRAY)
        # img = cv2.cvtColor(numpy.asarray(image),cv2.COLOR_RGB2GRAY)
        # img = cv2.GaussianBlur(img,(1,1),0)
        return image
      
    def GrandWave(self):
        self.key_press('j', 0.3 + random.random() / 10)



if __name__ == "__main__":
        # wdname 为窗口的名称
        # wdname = u'地下城与勇士'
        wdname = u'test.txt - 记事本'

        demo = GameAssist(wdname)