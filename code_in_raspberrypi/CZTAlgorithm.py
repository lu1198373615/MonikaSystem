import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl


class CZTAlgorithm:
    def __init__(self):
        self.hanning256 = np.array([0, 1, 1, 2, 4, 5, 7, 10, 12, 15, 18, 22, 26, 30, 34, 39, 44, 49, 54, 60, 66, 72, 79,
                               86, 93, 100, 107, 115, 123, 132, 140, 149, 158, 167, 176, 186, 195, 205, 215, 226, 236,
                               247, 258, 268, 280, 291, 302, 314, 325, 337, 349, 361, 373, 385, 397, 409, 421, 434,
                               446, 458, 471, 483, 496, 508, 521, 533, 546, 558, 571, 583, 596, 608, 620, 632, 644,
                               656, 668, 680, 692, 704, 715, 727, 738, 749, 760, 771, 782, 792, 802, 813, 823, 833,
                               842, 852, 861, 870, 879, 887, 896, 904, 912, 919, 927, 934, 941, 948, 954, 960, 966,
                               972, 977, 982, 987, 991, 995, 999, 1003, 1006, 1009, 1012, 1014, 1017, 1018, 1020,
                               1021, 1022, 1023, 1023, 1023, 1023, 1022, 1021, 1020, 1018, 1017, 1014, 1012, 1009,
                               1006, 1003, 999, 995, 991, 987, 982, 977, 972, 966, 960, 954, 948, 941, 934, 927, 919,
                               912, 904, 896, 887, 879, 870, 861, 852, 842, 833, 823, 813, 802, 792, 782, 771, 760,
                               749, 738, 727, 715, 704, 692, 680, 668, 656, 644, 632, 620, 608, 596, 583, 571, 558,
                               546, 533, 521, 508, 496, 483, 471, 458, 446, 434, 421, 409, 397, 385, 373, 361, 349,
                               337, 325, 314, 302, 291, 280, 268, 258, 247, 236, 226, 215, 205, 195, 186, 176, 167,
                               158, 149, 140, 132, 123, 115, 107, 100, 93, 86, 79, 72, 66, 60, 54, 49, 44, 39, 34,
                               30, 26, 22, 18, 15, 12, 10, 7, 5, 4, 2, 1, 1, 0])
        self.x1 = np.linspace(0, 255 / 100, 256)
        self.x2 = np.linspace(-255 / 100, 255 / 100, 511)

    def czt(self, fi, f1, f2):
        K = (f2-f1) / (256/100)
        si = np.exp(- 1j * np.pi * K * self.x1 ** 2)
        a = np.exp(-1j * 2 * np.pi * f1 * self.x1)
        y = si * a * fi[0:256] * self.hanning256
        fy = fft(y, 512)
        mf = np.exp(1j * np.pi * K * self.x2 ** 2)
        fv = fft(mf, 512)
        fy = fv * fy
        g = ifft(fy, 512)
        g1 = g[256:512]
        g2 = g1 * si
        return g2

    def fft_czt(self, fi):
        h_fft = np.abs(fft(fi[0:256], 256))[0:128]
        p1 = np.where(h_fft == np.max(h_fft))[0]
        if (p1[0]==0 | p1[0]==1):
            h_czt = np.abs(self.czt(fi, 0, 2 * (100 / 256)))
            p2 = np.where(h_czt == np.max(h_czt))[0]
            print('p1[0] =', p1[0], 'p2[0] =', p2[0])
            return (p2[0] + 1) * 1e8 / 256 / 256
        else:
            h_czt = np.abs(self.czt(fi, (p1[0]-1) * (100 / 256), (p1[0]+1) * (100 / 256)))
            p2 = np.where(h_czt == np.max(h_czt))[0]
            print('p1[0] =', p1[0], 'p2[0] =', p2[0])
            return (p1[0] - 1) * 1e8 / 256 + (p2[0] + 1) * 2e8 / 256 / 256

    def czt_accumulation(self, fi, interval=400):
        h_fft = np.abs(fft(fi, 256))[0:128]
        p1 = np.where(h_fft == np.max(h_fft))[0]
        if (p1[0] == 0 | p1[0] == 1):
            h_czt = np.zeros(256)
            for i in range(0, int(len(fi) / interval)):
                g2 = np.abs(self.czt(fi[100 + i * interval:356 + i * interval], 0, 2 * (100 / 256)))
                h_czt = h_czt + g2
            p2 = np.where(h_czt == np.max(h_czt))[0]
            #print('p1[0] =', p1[0], 'p2[0] =', p2[0])
            return (p2[0] + 1) * 1e8 / 256 / 256
        else:
            h_czt = np.zeros(256)
            for i in range(0, int(len(fi) / interval)):
                g2 = np.abs(self.czt(fi[100 + i * interval:356 + i * interval], (p1[0] - 1) * (100 / 256), (p1[0] + 1) * (100 / 256)))
                h_czt = h_czt + g2
            p2 = np.where(h_czt == np.max(h_czt))[0]
            #print('p1[0] =', p1[0], 'p2[0] =', p2[0])
            return (p1[0] - 1) * 1e8 / 256 + (p2[0] + 1) * 2e8 / 256 / 256


if __name__ == '__main__':
    c = CZTAlgorithm()
    x1 = np.linspace(0, 2570/100, 2571)
    fi = np.exp(1j * 2 * 9.2 * np.pi * x1)
    hp = c.czt_accumulation(fi)
    # plt.plot(np.real(hp))
    # plt.plot(np.imag(hp))
    # plt.plot(np.abs(hp))
    # plt.title('hp')
    # plt.show()
    # hp = np.abs(hp)
    # ppp = np.where(hp==np.max(hp))[0]
    print(hp)

