import wiringpi
import struct

class MyWiringPiSPI:
    def __init__(self):
        self.f = 1000000
        self.d = 15
        self.w = 0
        wiringpi.wiringPiSPISetupMode(0,15600000,1)
    
    def set_wave(self, f, d, w):
        self.f = f
        self.d = d
        self.w = w
        reg0 = ((self.d<<4) + self.w) & 255
        K = int(self.f * 42.95)
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
    
    def trans_reg(self,reg):
        wiringpi.wiringPiSPIDataRW(0, bytes(reg))
        

if __name__ == '__main__':
    ex = MyWiringPiSPI()

        
        
        
        
