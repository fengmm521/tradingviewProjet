#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time
import json

reload(sys)  
sys.setdefaultencoding('utf8')  

# reload(sys)
# sys.setdefaultencoding( "utf-8" )

class BTCViewTool(object):
    """docstring for ClassName"""
    def __init__(self, savepth = 'out'):

        self.savepth = savepth

        if not os.path.exists(self.savepth):
            os.mkdir(self.savepth)

        self.min15pth = self.savepth + os.sep + 'min15'
        if not os.path.exists(self.min15pth):
            os.mkdir(self.min15pth)

        self.hour1pth = self.savepth + os.sep + 'hour1'
        if not os.path.exists(self.hour1pth):
            os.mkdir(self.hour1pth)

        self.day1pth = self.savepth + os.sep + 'day1'
        if not os.path.exists(self.day1pth):
            os.mkdir(self.day1pth)

        self.week1pth = self.savepth + os.sep + 'week1'
        if not os.path.exists(self.week1pth):
            os.mkdir(self.week1pth)

        self.month1pth = self.savepth + os.sep + 'month1'
        if not os.path.exists(self.month1pth):
            os.mkdir(self.month1pth)

        self.reqURL = 'https://www.tradingview.com/symbols/BTCUSD/technicals/'
        self.wdriver = None
    #获取公司资料
    def runWork(self,isCmdMode = True):
        self.isCmdMode = isCmdMode
        if not self.wdriver:
            if self.isCmdMode:
                # import selenium.webdriver.phantomjs.webdriver as wd
                # import selenium.webdriver as wd
                from selenium import webdriver
                self.wdriver = webdriver.PhantomJS('/usr/local/bin/phantomjs')       #test
                self.wdriver.maximize_window()
                # self.wdriver.set_window_size(1920,1080)
                print('used phantomjs')
            else:
                # import selenium.webdriver.chrome.webdriver as  wd
                # chrome_options = wd.ChromeOptions()
                # chrome_options.add_argument('--headless')
                # chrome_options.add_argument('--disable-gpu')
                # self.wdriver = wd.WebDriver('/Users/mage/Documents/tool/cmdtool/chromedriver')       #test
                # self.wdriver.maximize_window()
                # linux上安装chrome要安装这两个库libgconf2-4 libnss3-1d
                #https://jiayi.space/post/zai-ubuntufu-wu-qi-shang-shi-yong-chrome-headless
                #chrome drvier下载：https://sites.google.com/a/chromium.org/chromedriver/downloads
                #

                from selenium import webdriver
                # from pyvirtualdisplay import Display
                # display = Display(visible=0, size=(800, 800))  
                # display.start()
                # time.sleep(1)
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument("user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'")
                # self.wdriver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/root/chrome/chromedriver')
                # print('used chrome')

                self.wdriver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/Users/mage/Documents/tool/cmdtool/chromedriver')
                print('used chrome')

        time.sleep(1)
        

        outdic = {} 

        #企业高管信息
        # self.startMining()                                                #获取高管信息

    def splitOneLineData(self,linestr):
        tmpstr = linestr.strip()
        p = tmpstr.rfind(' ')
        name = linestr[:p]
        np = name.rfind(' ')
        name = linestr[:np]
        name = name.replace(' ','')
        dat1 = linestr[np:p]
        dat1 = dat1.strip()
        statdat = linestr[p:]
        statdat = statdat.strip()
        return [name,dat1,statdat]

    def getDataFromStr(self,pstr):
        tmpstr = pstr.replace('\r','')
        tmpstr = tmpstr.replace(',','|')
        lines = tmpstr.split('\n')
        outdat = {}
        oscdat = lines[2:13]
        madat = lines[15:]
        oscdats = []
        for o in oscdat:
            dattmp = self.splitOneLineData(o)
            oscdats.append(dattmp)
        madats = []
        for d in madat:
            dattmp = self.splitOneLineData(o)
            madats.append(dattmp)
        outdat['osc'] = oscdats
        outdat['ma'] = madats
        return outdat

    def startMining(self):
        self.wdriver.get(self.reqURL)

        browser = self.wdriver

        outdic = {}
        #输入地址//*[@id="iotaAddress"]
        print('start url')
        time.sleep(1)
        print('get btn')
        #//*[@id="technicals-root"]/div/div/div[1]/div/div[1]/div
        min15btn = browser.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[1]/div/div[1]/div')

        hour1btn = browser.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[1]/div/div[2]/div')

        week1btn = browser.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[1]/div/div[4]/div')

        month1btn = browser.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[1]/div/div[5]/div')

        #//*[@id="technicals-root"]/div/div/div[3]
        data = browser.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[3]')

        time.sleep(1)
        print('day')
        tmpstr1day = data.text
        # print(data.text)
        outdic['day1'] = self.getDataFromStr(tmpstr1day)

        
        min15btn.click()
        print('min')
        time.sleep(8)
        data = browser.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[3]')
        time.sleep(0.2)
        tmpstr1day = data.text
        # print(data.text)
        outdic['min15'] = self.getDataFromStr(tmpstr1day)


        hour1btn.click()
        print('hour')
        time.sleep(8)
        data = browser.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[3]')
        time.sleep(0.2)
        tmpstr1day = data.text
        # print(data.text)
        outdic['hour1'] = self.getDataFromStr(tmpstr1day)


        week1btn.click()
        print('week')
        time.sleep(8)
        data = browser.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[3]')
        time.sleep(0.2)
        tmpstr1day = data.text
        # print(data.text)
        outdic['week1'] = self.getDataFromStr(tmpstr1day)

        month1btn.click()
        print('month')
        time.sleep(8)
        data = browser.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[3]')
        time.sleep(0.2)
        tmpstr1day = data.text
        # print(data.text)
        outdic['month1'] = self.getDataFromStr(tmpstr1day)


        # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # return outdic
        self.saveDatToFile(outdic)


    def saveLineDatStr(self,datas):
        outdataline = ''
        outflogline = ''
        oscdats = datas['osc']
        madatas = datas['ma']
        for o in oscdats:
            print(o)
            outdataline += str(o[1]) + ','
            if o[2] == 'Neutral':
                outflogline += '0,'
            elif o[2] == 'Sell':
                outflogline += '-1,'
            elif o[2] == 'Buy':
                outflogline += '1,'
        for o in madatas:
            outdataline += o[1] + ','
            if o[2] == 'Neutral':
                outflogline += '0,'
            elif o[2] == 'Sell':
                outflogline += '-1,'
            elif o[2] == 'Buy':
                outflogline += '1,'
        outdataline = outdataline[:-1]
        outflogline += outdataline
        return outflogline

    def getFirstLineName(self,datas):
        line = ''
        flogline = 'time,'
        oscdats = datas['osc']
        madatas = datas['ma']
        for o in oscdats:
            line += o[0] + ','
            flogline += o[0] + 'Flog,'
        for m in madatas:
            line += m[0] + ','
            flogline += m[0] + 'Flog,'
        line = line[:-1]
        flogline = flogline + line
        return flogline

    def saveDatToFile(self,datdic):
        #time.localtime(timeStamp)
        ftime = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
        fname = ftime.split('_')[0] + '.csv'

        fmin15pth = self.min15pth + os.sep + fname
        outline = ftime + ',' + self.saveLineDatStr(datdic['min15']) + '\n'
        if os.path.exists(fmin15pth):
            f = open(fmin15pth,'a+')
            f.write(outline)
            f.close()
        else:
            savestr = self.getFirstLineName(datdic['min15']) + '\n' + outline
            f = open(fmin15pth,'a+')
            f.write(savestr)
            f.close()

        fhour1pth = self.hour1pth + os.sep + fname
        outline = ftime + ',' + self.saveLineDatStr(datdic['hour1']) + '\n'
        if os.path.exists(fhour1pth):
            f = open(fhour1pth,'a+')
            f.write(outline)
            f.close()
        else:
            savestr = self.getFirstLineName(datdic['hour1']) + '\n' + outline
            f = open(fhour1pth,'a+')
            f.write(savestr)
            f.close()

        fday1pth = self.day1pth + os.sep + fname
        outline = ftime + ',' + self.saveLineDatStr(datdic['day1']) + '\n'
        if os.path.exists(fday1pth):
            f = open(fday1pth,'a+')
            f.write(outline)
            f.close()
        else:
            savestr = self.getFirstLineName(datdic['day1']) + '\n' + outline
            f = open(fday1pth,'a+')
            f.write(savestr)
            f.close()

        fweek1pth = self.week1pth + os.sep + fname
        outline = ftime + ',' + self.saveLineDatStr(datdic['week1']) + '\n'
        if os.path.exists(fweek1pth):
            f = open(fweek1pth,'a+')
            f.write(outline)
            f.close()
        else:
            savestr = self.getFirstLineName(datdic['week1']) + '\n' + outline
            f = open(fweek1pth,'a+')
            f.write(savestr)
            f.close()

        fmonth1pth = self.month1pth + os.sep + fname
        outline = ftime + ',' + self.saveLineDatStr(datdic['month1']) + '\n'
        if os.path.exists(fmonth1pth):
            f = open(fmonth1pth,'a+')
            f.write(outline)
            f.close()
        else:
            savestr = self.getFirstLineName(datdic['month1']) + '\n' + outline
            f = open(fmonth1pth,'a+')
            f.write(savestr)
            f.close()
#OSCILLATORS
# Name Value Action
# Relative Strength Index (14) 37.8 Neutral
# Stochastic Fast (14, 3, 1) 33.6 Neutral
# Commodity Channel Index (20) -108.4 Buy
# Average Directional Index (14) 30.7 Neutral
# Awesome Oscillator -1090.6 Sell
# Momentum (10) -310.0 Buy
# MACD Level (12, 27) -454.5 Sell
# Stochastic RSI Fast (3, 3, 14, 14) 28.1 Neutral
# Williams Percent Range (14) -66.4 Neutral
# Bull Bear Power -1063.7 Neutral
# Ultimate Oscillator (7, 14, 28) 47.1 Neutral
# MOVING AVERAGES
# Name Value Action
# Exponential Moving Average (10) 8331.9 Sell
# Simple Moving Average (10) 8477.5 Sell
# Exponential Moving Average (20) 8682.2 Sell
# Simple Moving Average (20) 8563.8 Sell
# Exponential Moving Average (30) 8970.6 Sell
# Simple Moving Average (30) 9279.8 Sell
# Exponential Moving Average (50) 9447.3 Sell
# Simple Moving Average (50) 9407.8 Sell
# Exponential Moving Average (100) 9892.7 Sell
# Simple Moving Average (100) 11104.7 Sell
# Exponential Moving Average (200) 9008.9 Sell
# Simple Moving Average (200) 9318.2 Sell
# Ichimoku Cloud Base Line (9, 26, 52, 26) 9470.0 Neutral
# Volume Weighted Moving Average (20) 8600.8 Sell
# Hull Moving Average (9) 7795.5 Buy
        
    def stopWork(self):
        self.wdriver.quit()


def main():
    companytool = BTCViewTool()
    companytool.runWork(False)
    runtime = 60*15  #延时15分钟
    while True:
        companytool.startMining()
        # companytool.stopWork()
        time.sleep(runtime)


#测试
if __name__ == '__main__':
    main()




