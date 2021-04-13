from setuptools import setup

setup(
    name='spectrum_painter',
    version='0.1',
    py_modules=['spectrum_painter'],
    install_requires=[
        'Click',
        'numpy',
        'imageio',
    ],
    entry_points='''
        [console_scripts]
        spectrum_painter=spectrum_painter.img2iqstream:img2iqstream
    ''',
)
