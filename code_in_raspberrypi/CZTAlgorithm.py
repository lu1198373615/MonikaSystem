import numpy as np
from numpy.fft import fft, ifft


class CZTAlgorithm:
    def __init__(self):
        self.transfer_point = 256
        self.hanning256 = np.array([0.5 - 0.5 * np.cos(2 * np.pi * n / (self.transfer_point - 1))
                                    for n in range(self.transfer_point)])
        self.x1 = np.linspace(0, (self.transfer_point-1) / self.transfer_point, self.transfer_point)
        self.x2 = np.linspace(-(self.transfer_point-1) / self.transfer_point, (self.transfer_point-1)
                              / self.transfer_point, 2 * self.transfer_point - 1)

    def czt(self, fi, f1, f2):
        K = (f2-f1) / (self.transfer_point/self.transfer_point)
        si = np.exp(- 1j * np.pi * K * self.x1 ** 2)
        a = np.exp(-1j * 2 * np.pi * f1 * self.x1)
        y = si * a * fi[0:self.transfer_point] * self.hanning256
        fy = fft(y, self.transfer_point * 2)
        mf = np.exp(1j * np.pi * K * self.x2 ** 2)
        fv = fft(mf, self.transfer_point * 2)
        fy = fv * fy
        g = ifft(fy, self.transfer_point * 2)
        g1 = g[self.transfer_point: self.transfer_point * 2]
        g2 = g1 * si
        return g2

    def fft_czt(self, fi):
        h_fft = np.abs(fft(fi[0:self.transfer_point], self.transfer_point))
        h_fft = h_fft[0: int(self.transfer_point / 2)]
        p1 = np.where(h_fft == np.max(h_fft))[0]
        if (p1[0]==0 | p1[0]==1):
            h_czt = np.abs(self.czt(fi, 0, 2 * (self.transfer_point / self.transfer_point)))
            p2 = np.where(h_czt == np.max(h_czt))[0]
            return (p2[0] + 1) * 1e8 / self.transfer_point / self.transfer_point
        else:
            h_czt = np.abs(self.czt(fi, (p1[0]-1) * (self.transfer_point / self.transfer_point), (p1[0]+1)
                                    * (self.transfer_point / self.transfer_point)))
            p2 = np.where(h_czt == np.max(h_czt))[0]
            return (p1[0] - 1) * 1e8 / self.transfer_point + (p2[0] + 1) * 2e8 / self.transfer_point / self.transfer_point


if __name__ == '__main__':
    c = CZTAlgorithm()
    x1 = np.linspace(0, 2570/100, 2571)
    fi = np.exp(1j * 2 * 3.4 * np.pi * x1)
    hp = c.fft_czt(fi)
    print(hp)
