import numpy as np
from warnings import warn
from subprocess import Popen, PIPE, STDOUT
from tempfile import mktemp
import os


class Radio(object):
    def __init__(self):
        self.frequency = 446000000
        self.bandwidth = 1000000
        self.samplerate = 1000000

    def _interleave(self, complex_iq):
        # Interleave I and Q
        intlv = np.zeros(2*complex_iq.size, dtype=np.float32)
        intlv[0::2] = np.real(complex_iq)
        intlv[1::2] = np.imag(complex_iq)
        return intlv

    def _clip(self, complex_iq, limit=1.0):
        # Clips amplitude to level
        clipped_samples = np.abs(complex_iq) > limit
        if np.any(clipped_samples):
            clipped = complex_iq
            clipped[clipped_samples] = complex_iq[clipped_samples] / np.abs(complex_iq[clipped_samples])
            warn('Some samples were clipped')
        else:
            clipped = complex_iq
        return clipped

    def transmit(self, complex_iq):
        raise NotImplementedError('transmit not implemented for this radio')

    def convert(self, complex_iq):
        raise NotImplementedError('convert not implemented for this radio')


class GenericFloat(Radio):
    """
    Generic interleaved float32 output for custom conversions
    """
    def convert(self, complex_iq):
        return self._interleave(complex_iq)


class Bladerf(Radio):
    """
    Creates BladeRf formatted samples
    """
    def convert(self, complex_iq):
        intlv = self._interleave(complex_iq)
        clipped = self._clip(intlv, limit=1.0)
        converted = 2047. * clipped
        bladerf_out = converted.astype(np.int16)
        return bladerf_out


class BladeOut(GenericFloat):
    """
    To be used with the bladeout tool, available on GitHub
    """
    def __init__(self):
        super(BladeOut, self).__init__()
        self.txvga1 = -15
        self.txvga2 = 20

    def transmit(self, complex_iq):
        intlv = self.convert(complex_iq)
        bladeout = Popen(['bladeout', '-f', str(self.frequency), '-r', str(self.samplerate), '-b', str(self.bandwidth),
                          '-g', str(self.txvga1), '-G', str(self.txvga2)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout = bladeout.communicate(input=intlv.tostring())
        return stdout


class Hackrf(Radio):
    def __init__(self):
        super(Hackrf, self).__init__()
        self.txvga = 0
        self.rxvga = 0
        self.rxlna = 0

    def convert(self, complex_iq):
        intlv = self._interleave(complex_iq)
        clipped = self._clip(intlv)
        converted = 127. * clipped
        hackrf_out = converted.astype(np.int8)
        return hackrf_out

    def transmit(self, complex_iq):
        hackrf_out = self.convert(complex_iq)
        pipe_file = mktemp()
        os.mkfifo(pipe_file)
        hackout = Popen(['hackrf_transfer', '-f', str(self.frequency), '-s', str(self.samplerate), '-b', str(self.bandwidth),
                          '-x', str(self.txvga), '-t', pipe_file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        pipe = open(pipe_file, 'wb')
        pipe.write(hackrf_out)
        pipe.close()
        hackout.wait()
        sout = hackout.communicate()
        os.unlink(pipe_file)
        return sout