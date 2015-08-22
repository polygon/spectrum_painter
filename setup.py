from setuptools import setup

setup(
    name='spectrum_painter',
    version='0.1',
    py_modules=['spectrum_painter'],
    install_requires=[
        'Click',
        'numpy',
        'scipy',
    ],
    entry_points='''
        [console_scripts]
        img2iqstream=spectrum_painter.img2iqstream:img2iqstream
    ''',
)
