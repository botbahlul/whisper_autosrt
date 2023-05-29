export LD_LIBRARY_PATH=/usr/local/lib/python3.8/site-packages/Pillow.libs:/usr/local/lib/python3.8/site-packages/nvidia/nvtx/lib/:/usr/local/lib/python3.8/site-packages/numpy.libs/:/usr/lib/x86_64-linux-gnu/:/usr/local/lib/python3.8/site-packages/tokenizers.libs/:/usr/local/lib/python3.8/site-packages/ctranslate2.libs/:/usr/local/lib/python3.8/site-packages/av.libs/:$LD_LIBRARY_PATH
pyinstaller --python=/usr/local/bin/python3.8 \
--hidden-import ctranslate2 \
--hidden-import huggingface_hub \
--hidden-import tokenizers \
--hidden-import onnxruntime \
--hidden-import faster_whisper \
--onefile whisper_autosrt.py
