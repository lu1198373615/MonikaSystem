import numpy as np
from numpy.fft import fft


class ApFFTAlgorithm:
    def __init__(self):
        self.transfer_point = 256
        self.hanning256 = np.array([0.5 - 0.5 * np.cos(2 * np.pi * n / (self.transfer_point - 1))
                                    for n in range(self.transfer_point)])
        self.conv_win = np.convolve(self.hanning256, self.hanning256)

    def apFFT(self, fi):
        x1 = fi[0: 2 * self.transfer_point - 1] * self.conv_win
        x2 = x1[self.transfer_point - 1: 2 * self.transfer_point - 1] + np.hstack((0, x1[0: self.transfer_point - 1]))
        hp = fft(x2, self.transfer_point)
        ha = np.abs(hp)
        ha = ha[0: int(self.transfer_point / 2)]
        point = np.where(ha == np.max(ha))[0]
        # print(point, hp[point[0]])
        return point, hp[point[0]]

    def time_shift_apFFT(self, fi):
        K1, Y1 = self.apFFT(fi[0: 2 * self.transfer_point - 1])
        K2, Y2 = self.apFFT(fi[self.transfer_point: 3 * self.transfer_point - 1])
        vv = Y2 * (np.real(Y1) - 1j*np.imag(Y1))
        coa = np.arctan2(np.imag(vv), np.real(vv)) / np.pi / 2
        return K1, coa

    def time_shift_apFFT_improved(self, fi):
        K1, coa1 = self.time_shift_apFFT(fi)
        if np.abs(coa1) > 0.1:
            fs = np.linspace(0 / self.transfer_point, (3 * self.transfer_point - 2) / self.transfer_point, 3 * self.transfer_point - 1)
            fs = np.exp(-1j * 2 * coa1 * np.pi * fs)
            K2, coa2 = self.time_shift_apFFT(fi[0:3 * self.transfer_point - 1] * fs)
            return K2, coa2, coa1
        else:
            return K1, coa1, 0

    def frequency_measurement(self, fi):
        A, B, C = self.time_shift_apFFT_improved(fi)
        return A + B + C


if __name__ == '__main__':
    c = ApFFTAlgorithm()
    x1 = np.linspace(-383/c.transfer_point, 383/c.transfer_point, 767)
    fi = np.exp(1j * 2 * 5.23456 * np.pi * x1)
    f = c.frequency_measurement(fi)
    print(f)
