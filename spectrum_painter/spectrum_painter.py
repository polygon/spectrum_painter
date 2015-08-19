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
        # Set FFT size to be double the image size so that the edge of the spectrum stays clear
        # preventing some bandfilter artifacts
        self.NFFT = 2*pic.shape[1]

        # Repeat image lines until each one comes often enough to reach the desired line time
        ffts = (np.flipud(np.repeat(pic[:, :, 0], self.repetitions, axis=0) / 16.)**2.) / 256.

        # Embed image in center bins of the FFT
        fftall = np.zeros((ffts.shape[0], self.NFFT))
        startbin = int(self.NFFT/4)
        fftall[:, startbin:(startbin+pic.shape[1])] = ffts

        # Generate random phase vectors for the FFT bins, this is important to prevent high peaks in the output
        # The phases won't be visible in the spectrum
        phases = 2*np.pi*np.random.rand(*fftall.shape)
        rffts = fftall * np.exp(1j*phases)

        # Perform the FFT per image line, then concatenate them to form the final signal
        timedata = np.fft.ifft(np.fft.ifftshift(rffts, axes=1), axis=1) / np.sqrt(float(self.NFFT))
        linear = timedata.flatten()
        linear = linear / np.max(np.abs(linear))
        return linear