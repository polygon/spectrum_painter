import click
from radios import BladeOut
from spectrum_painter import SpectrumPainter


@click.command()
@click.option('--samplerate', '-s', type=int, default=1000000, help='Samplerate of the radio')
@click.option('--linetime', '-l', type=float, default=0.005, help='Time for each line to show')
@click.option('--output', '-o', type=click.File('w'), help='File to write to (default: stdout)', default='-')
@click.argument('srcs', nargs=-1, type=click.Path(exists=True))
def img2iqstream(samplerate, linetime, output, srcs):
    bo = BladeOut()
    sp = SpectrumPainter(Fs=samplerate, T_line=linetime)
    if not srcs:
        return
    while True:
        for src in srcs:
            linear = sp.convert_image(src)
            blade = bo.convert(linear)
            output.write(blade.tostring())


if __name__ == '__main__':
    img2iqstream()