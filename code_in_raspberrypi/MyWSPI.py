import numpy as np
import matplotlib.pyplot as plt
# 定义的布尔值isValidWiringPi用于展示wiringpi是否可用，这在非树莓派的平台非常重要
isValidWiringPi = True
try:
    import wiringpi
except Exception:
    print("未成功导入wiringPi!!!")
    isValidWiringPi = False


class MyWSPI:
    def __init__(self):
        if isValidWiringPi:
            self.ad_width = 12
            self.w_cs_n = 24    # BCM_19 = WiringPi_24
            self.w_dclk = 28    # BCM_20 = WiringPi_28
            self.w_miso = [30, 31, 8, 9, 7, 21, 22, 26, 23, 15, 16, 27]    # BCM_0=miso[0]=WiringPi_30
            wiringpi.wiringPiSetup()
            for i in self.w_miso:
                wiringpi.pinMode(i, 0)
            wiringpi.pinMode(self.w_cs_n, 1)
            wiringpi.pinMode(self.w_dclk, 1)
            wiringpi.digitalWrite(self.w_cs_n, 1)
            wiringpi.digitalWrite(self.w_dclk, 0)
            self.fig = plt.figure(num=1, figsize=(15, 8), dpi=80)
            self.ax1 = self.fig.add_subplot(1, 1, 1)
        else:
            print("未成功导入wiringPi!!!")
        
    def fifo_sample(self, point):
        if isValidWiringPi:
            wiringpi.digitalWrite(self.w_cs_n, 0)
            result = []
            for i in range(0, point):
                wiringpi.digitalWrite(self.w_dclk, 1)
                wiringpi.digitalWrite(self.w_dclk, 0)
                ccc = wiringpi.digitalReadByte()
                if ccc > (2 ** (self.ad_width - 1)) - 1:
                    ccc = ccc - 2 ** self.ad_width
                result.append(ccc)
            wiringpi.digitalWrite(self.w_cs_n, 1)
            return result
        else:
            x1 = np.linspace(0, 2570 / 100, 2571)
            f = 0.699
            return 1500 * np.cos(2 * np.pi * f * x1)
    

if __name__ == '__main__':
    ex = MyWSPI()
    ret = ex.fifo_sample(1024)
