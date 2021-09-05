# 定义的布尔值isValidWiringPi用于展示wiringpi是否可用，这在非树莓派的平台非常重要
isValidWiringPi = True
try:
    import wiringpi
except Exception:
    print("未成功导入wiringPi!!!")
    isValidWiringPi = False


class MyWiringPiSPI:
    def __init__(self):
        if isValidWiringPi:
            self.f = 1000000
            self.d = 15
            self.w = 0
            self.spi_speed = 15600000
            wiringpi.wiringPiSPISetupMode(0, self.spi_speed, 1)
        else:
            print("未成功导入wiringPi!!!")
    
    def set_wave(self, f, d, w):
        if isValidWiringPi:
            self.f = f
            self.d = d
            self.w = w
            reg0 = ((self.d<<4) + self.w) & 255
            K = int(self.f * 2 ** 32 / 1e8)
            reg1 = (K>> 0) & 255
            reg2 = (K>> 8) & 255
            reg3 = (K>>16) & 255
            reg4 = (K>>24) & 255
            print(K)
            wiringpi.wiringPiSPIDataRW(0, bytes([0,reg0]))
            wiringpi.wiringPiSPIDataRW(0, bytes([1,reg1]))
            wiringpi.wiringPiSPIDataRW(0, bytes([2,reg2]))
            wiringpi.wiringPiSPIDataRW(0, bytes([3,reg3]))
            wiringpi.wiringPiSPIDataRW(0, bytes([4,reg4]))
        else:
            print("未成功导入wiringPi!!!")
    
    def trans_reg(self,reg):
        if isValidWiringPi:
            wiringpi.wiringPiSPIDataRW(0, bytes(reg))
        else:
            print("未成功导入wiringPi!!!")
        

if __name__ == '__main__':
    ex = MyWiringPiSPI()
