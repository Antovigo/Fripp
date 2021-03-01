from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'Fripp real-time audio looper'
LONG_DESCRIPTION = 'Fripp: real-time, cross-platform audio looper'

# Setting up
setup(
        name="Fripp", 
        version=VERSION,
        author="Antoine Vigouroux",
        author_email="<antvig@protonmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['sounddevice', 'numpy', 'soundfile', 'PySimpleGUI'], 
        
        keywords=['looper', 'audio', 'music'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3"
        ]
)
