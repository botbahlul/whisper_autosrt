pyinstaller ^
--hidden-import ctranslate2 ^
--hidden-import huggingface_hub ^
--hidden-import tokenizers ^
--hidden-import onnxruntime ^
--hidden-import faster_whisper ^
--onefile whisper_autosrt.py
