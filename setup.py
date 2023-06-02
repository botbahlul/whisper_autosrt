from __future__ import unicode_literals
import sys
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='setuptools')
warnings.filterwarnings("ignore", category=UserWarning, module='setuptools')
warnings.filterwarnings("ignore", message=".*is deprecated*")

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from whisper_autosrt import VERSION

long_description = (
    'whisper_autosrt is a command line utility for automatic speech recognition and subtitle generation. '
    'It takes video or audio files as input, generate transcriptions for them and optionally translates  '
    'them to a different language, and finally saves the resulting subtitles file to disk.               '
    'It supports a variety of input and output languages and can currently produce subtitles in SRT, VTT,'
    'JSON, and RAW format.'
)

install_requires=[
    "requests>=2.3.0",
    "httpx>=0.24.0",
    "urllib3 >=1.26.0,<3.0",
    "pysrt>=1.0.1",
    "six>=1.11.0",
    "progressbar2>=3.34.3",
    "faster_whisper>=0.6.0",
]

setup(
    name="whisper_autosrt",
    version=VERSION,
    description="a command line utility for automatic speech recognition and subtitle generation",
    long_description = long_description,
    author="Bot Bahlul",
    author_email="bot.bahlul@gmail.com",
    url="https://github.com/botbahlul/whisper_autosrt",
    packages=["whisper_autosrt"],
    entry_points={
        "console_scripts": [
            "whisper_autosrt = whisper_autosrt:main",
        ],
    },
    install_requires=install_requires,
    license=open("LICENSE").read()
)
