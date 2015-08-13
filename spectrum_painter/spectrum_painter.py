import numpy as np
import scipy.ndimage as img


class SpectrumPainter(object):
    def __init__(self, Fs=1000000, T_line=0.005):
        self.NFFT = 4096
        self.Fs = Fs
        self.T_line = T_line

    @property
    def repetitions(self):
        return int(np.ceil(self.T_line * self.Fs / self.NFFT))

    def convert_image(self, filename):
        pic = img.imread(filename)
        if pic.shape[1] != self.NFFT/2:
            raise ValueError('Picture width (%i) must match FFT size (%i)' % (pic.size[1], self.NFFT))
        ffts = (np.flipud(np.repeat(pic[:, :, 0], self.repetitions, axis=0) / 16.)**2.) / 256.
        fftall = np.zeros((ffts.shape[0], self.NFFT))
        fftall[:, self.NFFT/4:-self.NFFT/4] = ffts

        phases = 2*np.pi*np.random.rand(*fftall.shape)
        rffts = fftall * np.exp(1j*phases)
        timedata = np.fft.ifft(np.fft.ifftshift(rffts, axes=1), axis=1) / np.sqrt(float(self.NFFT))
        linear = timedata.flatten()
        linear = linear / np.max(np.abs(linear))
        return linear