import click
from radios import GenericFloat, Bladerf, Hackrf
from spectrum_painter import SpectrumPainter

FORMATTERS = {'float': GenericFloat, 'bladerf': Bladerf, 'hackrf': Hackrf}

@click.command()
@click.option('--samplerate', '-s', type=int, default=1000000, help='Samplerate of the radio')
@click.option('--linetime', '-l', type=float, default=0.005, help='Time for each line to show')
@click.option('--output', '-o', type=click.File('w'), help='File to write to (default: stdout)', default='-')
@click.option('--format', type=click.Choice(['float', 'bladerf', 'hackrf']), default='float', help='Output format of samples')
@click.argument('srcs', nargs=-1, type=click.Path(exists=True))
def img2iqstream(samplerate, linetime, output, format, srcs):
    formatter = FORMATTERS[format]()
    painter = SpectrumPainter(Fs=samplerate, T_line=linetime)
    if not srcs:
        return

    for src in srcs:
        iq_samples = painter.convert_image(src)
        target_format = formatter.convert(iq_samples)
        output.write(target_format.tostring())


if __name__ == '__main__':
    img2iqstream()
