# whisper_autosrt <a href="https://pypi.python.org/pypi/whisper_autosrt"><img src="https://img.shields.io/pypi/v/whisper_autosrt.svg"></img></a>
  
### Auto generate subtitle and translated subtitles files for any video / audio files
whisper_autosrt is a simple command line tool made with python to auto generate subtitle/closed caption for any video or audio files using faster_whisper module https://github.com/guillaumekln/faster-whisper which is a reimplementation of OpenAI's Whisper module and translate it automatically for free using a simple unofficial online Google Translate API.

### Installation
If you don't have python on your Windows system you can try the compiled version from this git release assets
https://github.com/botbahlul/whisper_autosrt/releases

If it doesn't run well then you need to install python on your Windows system.

Just extract those ffmpeg.exe, ffprobe.exe, and whisper_autosrt.exe into a folder that has been added to PATH ENVIRONMENT for example in C:\Windows\system32 so you can execute them from any folder.

You can get latest version of ffmpeg from https://www.ffmpeg.org/

In Linux you have to install this script with python (version minimal 3.8.12) and install ffmpeg with your linux package manager, for example in debian based linux distribution you can type :

```
sudo apt update
sudo apt install -y ffmpeg
```

To install this whisper_autosrt, just type :
```
pip install --upgrade whisper_autosrt
```

You can try to compile that whisper_autosrt.py script in win/linux folder into a single executable file with pyinstaller by typing these :
```
pip install pyinstaller
pyinstaller --onefile whisper_autosrt.py
```

The executable compiled file will be placed by pyinstaller into dist subfolder of your current working folder, so you can just rename and put that compiled file into a folder that has been added to your PATH ENVIRONMENT so you can execute it from anywhere. 
Beware that on Linux system the compiled file could be very large (about 2.2GB) because pyinstaller will include all nvidia cuda driver on it.

I was succesfuly compiled it on Windows 10 with pyinstaller-5.1 and Pyhton-3.10.4, and python-3.8.12 on Debian 9.

Another alternative way to install this script with python is by cloning this git (or downloading this git as zip then extract it into a folder), and then just type :

```
pip install wheel
python setup.py bdist_wheel
```

Then check the name of the whl file created in dist folder. In case the filename is whisper_autosrt-0.0.3-py2.py3-none-any.whl then you can install that whl file with pip :
```
cd dist
pip install whisper_autosrt-0.0.3-py2.py3-none-any.whl
```

You can also install this script (or any pip package) in ANDROID DEVICES via PYTHON package in TERMUX APP.

https://github.com/termux/termux-app/releases/tag/v0.118.0

Choose the right apk for your device, install it, then open it

Type these commands to get python, pip, this whisper_autosrt, (and any other pip packages) :

```
termux-setup-storage
pkg update -y
pkg install -y python
pkg install -y ffmpeg
pip install whisper_autosrt
```

### Simple usage example 

```
whisper_autosrt --list-src-languages
whisper_autosrt --list-dst-languages
whisper_autosrt -S zh -D en "Episode 1.mp4"
```

If you don't know exactly what language spoken on the video/audio file, you can try to use \'-S auto\', so this app will try to auto detect the language.
```
whisper_autosrt -S auto -D en ""Episode 1.mp4""
```

For multiple video/audio files you can use wildcard e.g:
```
whisper_autosrt -S zh -D en C:\Movies\*.mp4
```

or separate them with space character e.g:
```
whisper_autosrt -S zh -D en "Episode 1.mp4" "Episode 2.mp4"
```

If you don't need translations just type :
```
whisper_autosrt -S auto "Episode 1.mp4"
```

### Usage

```
usage: whisper_autosrt [-h] [-m MODEL_NAME] [-lm] [-d DEVICE] [-ld] [-ct COMPUTE_TYPE] [-lct] [-t CPU_THREADS] [-nw NUM_WORKERS]
                       [-S SRC_LANGUAGE] [-D DST_LANGUAGE] [-lS] [-lD] [-F FORMAT] [-lF] [-c CONCURRENCY] [-es EMBED_SRC]
                       [-ed EMBED_DST] [-fr FORCE_RECOGNIZE] [-v]
                       [source_path ...]

positional arguments:
  source_path           Path to the video or audio files to generate subtitles files (use wildcard for multiple files or separate
                        them with a space character e.g. "file 1.mp4" "file 2.mp4")

options:
  -h, --help            show this help message and exit
  -m MODEL_NAME, --model-name MODEL_NAME
                        name of whisper model to use
  -lm, --list-models    List of whisper models name
  -d DEVICE, --device DEVICE
                        name of the device to use
  -ld, --list-devices   List of supported devices
  -ct COMPUTE_TYPE, --compute-type COMPUTE_TYPE
                        name of the compute type (quantization) to use
  -lct, --list-compute-types
                        List of supported compute types
  -t CPU_THREADS, --cpu-threads CPU_THREADS
                        Number of threads to use when running on CPU
  -nw NUM_WORKERS, --num-workers NUM_WORKERS
                        Number of concurrent calls when running whisper model
  -S SRC_LANGUAGE, --src-language SRC_LANGUAGE
                        Language code of the audio language spoken in video/audio source_path
  -D DST_LANGUAGE, --dst-language DST_LANGUAGE
                        Desired translation language code for the subtitles
  -lS, --list-src-languages
                        List all available src_languages (whisper supported languages)
  -lD, --list-dst-languages
                        List all available dst_languages (google translate supported languages)
  -F FORMAT, --format FORMAT
                        Desired subtitles format
  -lF, --list-formats   List all supported subtitles formats
  -c CONCURRENCY, --concurrency CONCURRENCY
                        Number of concurrent calls for Google Translate API
  -es EMBED_SRC, --embed-src EMBED_SRC
                        Boolean value (True or False) for embedding original language subtitles file into video file
  -ed EMBED_DST, --embed-dst EMBED_DST
                        Boolean value (True or False) for embedding translated subtitles file into video file
  -fr FORCE_RECOGNIZE, --force-recognize FORCE_RECOGNIZE
                        Boolean value (True or False) for re-recognize media file event if it's already has subtitles stream
  -v, --version         show program's version number and exit
```

### License

MIT

Check my other SPEECH RECOGNITIION + TRANSLATE PROJECTS https://github.com/botbahlul?tab=repositories

Buy me coffee : https://sociabuzz.com/botbahlul/tribe
