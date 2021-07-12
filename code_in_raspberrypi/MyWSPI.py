import wiringpi
import time
import matplotlib.pyplot as plt
import numpy as np

class MyWSPI:
    def __init__(self):
        self.w_cs_n = 24    # BCM_19 = WiringPi_24
        self.w_dclk = 28    # BCM_20 = WiringPi_28
        self.w_miso = [30,31,8,9,7,21,22,26,23,15,16,27]    # BCM_0=miso[0]=WiringPi_30
        wiringpi.wiringPiSetup()
        for i in self.w_miso:
            wiringpi.pinMode(i, 0)
        wiringpi.pinMode(self.w_cs_n, 1)
        wiringpi.pinMode(self.w_dclk, 1)
        wiringpi.digitalWrite(self.w_cs_n,1)
        wiringpi.digitalWrite(self.w_dclk,0)
        self.fig = plt.figure(num=1, figsize=(15, 8),dpi=80)     #开启一个窗口，同时设置大小，分辨率
        self.ax1 = self.fig.add_subplot(1,1,1)  #通过fig添加子图，参数：行数，列数，第几个。
        
    def fifo_sample(self,point):
        wiringpi.digitalWrite(self.w_cs_n,0)
        #time.sleep(0.1)
        result = []
        for i in range(0,point):
            wiringpi.digitalWrite(self.w_dclk,1)
            wiringpi.digitalWrite(self.w_dclk,0)
            ccc = wiringpi.digitalReadByte()
            #print(ccc)
            if ccc>2047:
                ccc = ccc - 4096
            result.append(ccc)
        wiringpi.digitalWrite(self.w_cs_n,1)
        #time.sleep(0.1)
        return result
    

if __name__ == '__main__':
    ex = MyWSPI()
    ret = ex.fifo_sample(1024)

    #while 1:
        #ret = ex.fifo_sample()
        #print(ret)
        #ex.show_sample(ret)
    
        
        


