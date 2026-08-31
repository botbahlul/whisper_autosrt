export LD_LIBRARY_PATH=/usr/local/lib/python3.10/site-packages/Pillow.libs:/usr/local/lib/python3.10/site-packages/nvidia/nvtx/lib/:/usr/local/lib/python3.10/site-packages/numpy.libs/:/usr/lib/x86_64-linux-gnu/:/usr/local/lib/python3.10/site-packages/tokenizers.libs/:/usr/local/lib/python3.10/site-packages/ctranslate2.libs/:/usr/local/lib/python3.10/site-packages/av.libs/:$LD_LIBRARY_PATH

folder1="./build"
folder2="./dist"
file1="./*.spec"

if [ -d "$folder1" ]; then
	rm -rf "$folder1"
fi

if [ -d "$folder2" ]; then
	rm -rf "$folder2"
fi

if [ -f "$file1" ]; then
	rm -f "$file1"
fi

pyinstaller --python=/usr/local/bin/python3.10 \
--exclude-module pkg_resources \
--collect-all faster_whisper \
--hidden-import ctranslate2 \
--hidden-import huggingface_hub \
--hidden-import tokenizers \
--hidden-import onnxruntime \
--hidden-import faster_whisper \
--hidden-import argparse \
--hidden-import appdirs \
--hidden-import tqdm \
--onefile whisper_autosrt.py

