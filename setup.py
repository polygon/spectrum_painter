from setuptools import setup

setup(
    name='spectrum_painter',
    version='0.1',
    packages=['spectrum_painter'],
    install_requires=[
        'Click',
        'numpy',
        'imageio',
        'Scipy',
    ],
    entry_points='''
        [console_scripts]
        spectrum_painter=spectrum_painter.img2iqstream:img2iqstream
    ''',
)
