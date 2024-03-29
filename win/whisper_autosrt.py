from __future__ import absolute_import, print_function, unicode_literals
import argparse
import audioop
import math
import multiprocessing
import os
import subprocess
import sys
import tempfile
import wave
import json
import requests
try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError
from progressbar import ProgressBar, Percentage, Bar, ETA
import pysrt
import six
# ADDITIONAL IMPORT
from glob import glob, escape
import shlex
import time
from datetime import datetime, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")
from faster_whisper import WhisperModel
import ctypes
import shutil


VERSION = "0.1.11"
#marker='█'


class WhisperLanguage:
    def __init__(self):
        self.list_codes = []
        self.list_codes.append("auto")
        self.list_codes.append("af")
        self.list_codes.append("sq")
        self.list_codes.append("am")
        self.list_codes.append("ar")
        self.list_codes.append("hy")
        self.list_codes.append("as")
        self.list_codes.append("az")
        self.list_codes.append("ba")
        self.list_codes.append("eu")
        self.list_codes.append("be")
        self.list_codes.append("bn")
        self.list_codes.append("bs")
        self.list_codes.append("br")
        self.list_codes.append("bg")
        self.list_codes.append("ca")
        self.list_codes.append("zh")
        self.list_codes.append("hr")
        self.list_codes.append("cs")
        self.list_codes.append("da")
        self.list_codes.append("nl")
        self.list_codes.append("en")
        self.list_codes.append("et")
        self.list_codes.append("fo")
        self.list_codes.append("fi")
        self.list_codes.append("fr")
        self.list_codes.append("gl")
        self.list_codes.append("ka")
        self.list_codes.append("de")
        self.list_codes.append("el")
        self.list_codes.append("gu")
        self.list_codes.append("ht")
        self.list_codes.append("ha")
        self.list_codes.append("haw")
        self.list_codes.append("he")
        self.list_codes.append("hi")
        self.list_codes.append("hu")
        self.list_codes.append("is")
        self.list_codes.append("id")
        self.list_codes.append("it")
        self.list_codes.append("ja")
        self.list_codes.append("jv")
        self.list_codes.append("kn")
        self.list_codes.append("kk")
        self.list_codes.append("km")
        self.list_codes.append("ko")
        self.list_codes.append("lo")
        self.list_codes.append("la")
        self.list_codes.append("lv")
        self.list_codes.append("ln")
        self.list_codes.append("lt")
        self.list_codes.append("lb")
        self.list_codes.append("mk")
        self.list_codes.append("mg")
        self.list_codes.append("ms")
        self.list_codes.append("ml")
        self.list_codes.append("mt")
        self.list_codes.append("mi")
        self.list_codes.append("mr")
        self.list_codes.append("mn")
        self.list_codes.append("my")
        self.list_codes.append("ne")
        self.list_codes.append("no")
        self.list_codes.append("nn")
        self.list_codes.append("oc")
        self.list_codes.append("ps")
        self.list_codes.append("fa")
        self.list_codes.append("pl")
        self.list_codes.append("pt")
        self.list_codes.append("pa")
        self.list_codes.append("ro")
        self.list_codes.append("ru")
        self.list_codes.append("sa")
        self.list_codes.append("sr")
        self.list_codes.append("sn")
        self.list_codes.append("sd")
        self.list_codes.append("si")
        self.list_codes.append("sk")
        self.list_codes.append("sl")
        self.list_codes.append("so")
        self.list_codes.append("es")
        self.list_codes.append("su")
        self.list_codes.append("sw")
        self.list_codes.append("sv")
        self.list_codes.append("tl")
        self.list_codes.append("tg")
        self.list_codes.append("ta")
        self.list_codes.append("tt")
        self.list_codes.append("te")
        self.list_codes.append("th")
        self.list_codes.append("bo")
        self.list_codes.append("tr")
        self.list_codes.append("tk")
        self.list_codes.append("uk")
        self.list_codes.append("ur")
        self.list_codes.append("uz")
        self.list_codes.append("vi")
        self.list_codes.append("cy")
        self.list_codes.append("yi")
        self.list_codes.append("yo")

        self.list_names = []
        self.list_names.append("Auto Detect")
        self.list_names.append("Afrikaans")
        self.list_names.append("Albanian")
        self.list_names.append("Amharic")
        self.list_names.append("Arabic")
        self.list_names.append("Armenian")
        self.list_names.append("Assamese")
        self.list_names.append("Azerbaijani")
        self.list_names.append("Bashkir")
        self.list_names.append("Basque")
        self.list_names.append("Belarusian")
        self.list_names.append("Bengali")
        self.list_names.append("Bosnian")
        self.list_names.append("Breton")
        self.list_names.append("Bulgarian")
        self.list_names.append("Catalan")
        self.list_names.append("Chinese")
        self.list_names.append("Croatian")
        self.list_names.append("Czech")
        self.list_names.append("Danish")
        self.list_names.append("Dutch")
        self.list_names.append("English")
        self.list_names.append("Estonian")
        self.list_names.append("Faroese")
        self.list_names.append("Finnish")
        self.list_names.append("French")
        self.list_names.append("Galician")
        self.list_names.append("Georgian")
        self.list_names.append("German")
        self.list_names.append("Greek")
        self.list_names.append("Gujarati")
        self.list_names.append("Haitian Creole")
        self.list_names.append("Hausa")
        self.list_names.append("Hawaiian")
        self.list_names.append("Hebrew")
        self.list_names.append("Hindi")
        self.list_names.append("Hungarian")
        self.list_names.append("Icelandic")
        self.list_names.append("Indonesian")
        self.list_names.append("Italian")
        self.list_names.append("Japanese")
        self.list_names.append("Javanese")
        self.list_names.append("Kannada")
        self.list_names.append("Kazakh")
        self.list_names.append("Khmer")
        self.list_names.append("Korean")
        self.list_names.append("Lao")
        self.list_names.append("Latin")
        self.list_names.append("Latvian")
        self.list_names.append("Lingala")
        self.list_names.append("Lithuanian")
        self.list_names.append("Luxembourgish")
        self.list_names.append("Macedonian")
        self.list_names.append("Malagasy")
        self.list_names.append("Malay")
        self.list_names.append("Malayalam")
        self.list_names.append("Maltese")
        self.list_names.append("Maori")
        self.list_names.append("Marathi")
        self.list_names.append("Mongolian")
        self.list_names.append("Myanmar (Burmese)")
        self.list_names.append("Nepali")
        self.list_names.append("Norwegian")
        self.list_names.append("Nynorsk")
        self.list_names.append("Occitan")
        self.list_names.append("Pashto")
        self.list_names.append("Persian")
        self.list_names.append("Polish")
        self.list_names.append("Portuguese")
        self.list_names.append("Punjabi")
        self.list_names.append("Romanian")
        self.list_names.append("Russian")
        self.list_names.append("Sanskrit")
        self.list_names.append("Serbian")
        self.list_names.append("Shona")
        self.list_names.append("Sindhi")
        self.list_names.append("Sinhala")
        self.list_names.append("Slovak")
        self.list_names.append("Slovenian")
        self.list_names.append("Somali")
        self.list_names.append("Spanish")
        self.list_names.append("Sundanese")
        self.list_names.append("Swahili")
        self.list_names.append("Swedish")
        self.list_names.append("Tagalog")
        self.list_names.append("Tajik")
        self.list_names.append("Tamil")
        self.list_names.append("Tatar")
        self.list_names.append("Telugu")
        self.list_names.append("Thai")
        self.list_names.append("Tibetan")
        self.list_names.append("Turkish")
        self.list_names.append("Turkmen")
        self.list_names.append("Ukrainian")
        self.list_names.append("Urdu")
        self.list_names.append("Uzbek")
        self.list_names.append("Vietnamese")
        self.list_names.append("Welsh")
        self.list_names.append("Yiddish")
        self.list_names.append("Yoruba")

        self.code_of_name = dict(zip(self.list_names, self.list_codes))
        self.name_of_code = dict(zip(self.list_codes, self.list_names))

        self.dict = {
                        'auto': 'Auto Detect',
                        'af': 'Afrikaans',
                        'sq': 'Albanian',
                        'am': 'Amharic',
                        'ar': 'Arabic',
                        'hy': 'Armenian',
                        'as': 'Assamese',
                        'az': 'Azerbaijani',
                        'ba': 'Bashkir',
                        'eu': 'Basque',
                        'be': 'Belarusian',
                        'bn': 'Bengali',
                        'bs': 'Bosnian',
                        'br': 'Breton',
                        'bg': 'Bulgarian',
                        'ca': 'Catalan',
                        'zh': 'Chinese',
                        'hr': 'Croatian',
                        'cs': 'Czech',
                        'da': 'Danish',
                        'nl': 'Dutch',
                        'en': 'English',
                        'et': 'Estonian',
                        'fo': 'Faroese',
                        'fi': 'Finnish',
                        'fr': 'French',
                        'gl': 'Galician',
                        'ka': 'Georgian',
                        'de': 'German',
                        'el': 'Greek',
                        'gu': 'Gujarati',
                        'ht': 'Haitian Creole',
                        'ha': 'Hausa',
                        'haw': 'Hawaiian',
                        'he': 'Hebrew',
                        'hi': 'Hindi',
                        'hu': 'Hungarian',
                        'is': 'Icelandic',
                        'id': 'Indonesian',
                        'it': 'Italian',
                        'ja': 'Japanese',
                        'jv': 'Javanese',
                        'kn': 'Kannada',
                        'kk': 'Kazakh',
                        'km': 'Khmer',
                        'ko': 'Korean',
                        'lo': 'Lao',
                        'la': 'Latin',
                        'lv': 'Latvian',
                        'ln': 'Lingala',
                        'lt': 'Lithuanian',
                        'lb': 'Luxembourgish',
                        'mk': 'Macedonian',
                        'mg': 'Malagasy',
                        'ms': 'Malay',
                        'ml': 'Malayalam',
                        'mt': 'Maltese',
                        'mi': 'Maori',
                        'mr': 'Marathi',
                        'mn': 'Mongolian',
                        'my': 'Myanmar (Burmese)',
                        'ne': 'Nepali',
                        'no': 'Norwegian',
                        'nn': 'Nynorsk',
                        'oc': 'Occitan',
                        'ps': 'Pashto',
                        'fa': 'Persian',
                        'pl': 'Polish',
                        'pt': 'Portuguese',
                        'pa': 'Punjabi',
                        'ro': 'Romanian',
                        'ru': 'Russian',
                        'sa': 'Sanskrit',
                        'sr': 'Serbian',
                        'sn': 'Shona',
                        'sd': 'Sindhi',
                        'si': 'Sinhala',
                        'sk': 'Slovak',
                        'sl': 'Slovenian',
                        'so': 'Somali',
                        'es': 'Spanish',
                        'su': 'Sundanese',
                        'sw': 'Swahili',
                        'sv': 'Swedish',
                        'tl': 'Tagalog',
                        'tg': 'Tajik',
                        'ta': 'Tamil',
                        'tt': 'Tatar',
                        'te': 'Telugu',
                        'th': 'Thai',
                        'bo': 'Tibetan',
                        'tr': 'Turkish',
                        'tk': 'Turkmen',
                        'uk': 'Ukrainian',
                        'ur': 'Urdu',
                        'uz': 'Uzbek',
                        'vi': 'Vietnamese',
                        'cy': 'Welsh',
                        'yi': 'Yiddish',
                        'yo': 'Yoruba',
                    }

    def get_name(self, get_code):
        return self.dict.get(get_code.lower(), "")

    def get_code(self, language):
        for get_code, lang in self.dict.items():
            if lang.lower() == language.lower():
                return get_code
        return ""


class GoogleLanguage:
    def __init__(self):
        self.list_codes = []
        self.list_codes.append("af")
        self.list_codes.append("sq")
        self.list_codes.append("am")
        self.list_codes.append("ar")
        self.list_codes.append("hy")
        self.list_codes.append("as")
        self.list_codes.append("ay")
        self.list_codes.append("az")
        self.list_codes.append("bm")
        self.list_codes.append("eu")
        self.list_codes.append("be")
        self.list_codes.append("bn")
        self.list_codes.append("bho")
        self.list_codes.append("bs")
        self.list_codes.append("bg")
        self.list_codes.append("ca")
        self.list_codes.append("ceb")
        self.list_codes.append("ny")
        self.list_codes.append("zh")
        self.list_codes.append("zh-CN")
        self.list_codes.append("zh-TW")
        self.list_codes.append("co")
        self.list_codes.append("hr")
        self.list_codes.append("cs")
        self.list_codes.append("da")
        self.list_codes.append("dv")
        self.list_codes.append("doi")
        self.list_codes.append("nl")
        self.list_codes.append("en")
        self.list_codes.append("eo")
        self.list_codes.append("et")
        self.list_codes.append("ee")
        self.list_codes.append("fil")
        self.list_codes.append("fi")
        self.list_codes.append("fr")
        self.list_codes.append("fy")
        self.list_codes.append("gl")
        self.list_codes.append("ka")
        self.list_codes.append("de")
        self.list_codes.append("el")
        self.list_codes.append("gn")
        self.list_codes.append("gu")
        self.list_codes.append("ht")
        self.list_codes.append("ha")
        self.list_codes.append("haw")
        self.list_codes.append("he")
        self.list_codes.append("hi")
        self.list_codes.append("hmn")
        self.list_codes.append("hu")
        self.list_codes.append("is")
        self.list_codes.append("ig")
        self.list_codes.append("ilo")
        self.list_codes.append("id")
        self.list_codes.append("ga")
        self.list_codes.append("it")
        self.list_codes.append("ja")
        self.list_codes.append("jv")
        self.list_codes.append("kn")
        self.list_codes.append("kk")
        self.list_codes.append("km")
        self.list_codes.append("rw")
        self.list_codes.append("gom")
        self.list_codes.append("ko")
        self.list_codes.append("kri")
        self.list_codes.append("kmr")
        self.list_codes.append("ckb")
        self.list_codes.append("ky")
        self.list_codes.append("lo")
        self.list_codes.append("la")
        self.list_codes.append("lv")
        self.list_codes.append("ln")
        self.list_codes.append("lt")
        self.list_codes.append("lg")
        self.list_codes.append("lb")
        self.list_codes.append("mk")
        self.list_codes.append("mg")
        self.list_codes.append("ms")
        self.list_codes.append("ml")
        self.list_codes.append("mt")
        self.list_codes.append("mi")
        self.list_codes.append("mr")
        self.list_codes.append("mni-Mtei")
        self.list_codes.append("lus")
        self.list_codes.append("mn")
        self.list_codes.append("my")
        self.list_codes.append("ne")
        self.list_codes.append("no")
        self.list_codes.append("or")
        self.list_codes.append("om")
        self.list_codes.append("ps")
        self.list_codes.append("fa")
        self.list_codes.append("pl")
        self.list_codes.append("pt")
        self.list_codes.append("pa")
        self.list_codes.append("qu")
        self.list_codes.append("ro")
        self.list_codes.append("ru")
        self.list_codes.append("sm")
        self.list_codes.append("sa")
        self.list_codes.append("gd")
        self.list_codes.append("nso")
        self.list_codes.append("sr")
        self.list_codes.append("st")
        self.list_codes.append("sn")
        self.list_codes.append("sd")
        self.list_codes.append("si")
        self.list_codes.append("sk")
        self.list_codes.append("sl")
        self.list_codes.append("so")
        self.list_codes.append("es")
        self.list_codes.append("su")
        self.list_codes.append("sw")
        self.list_codes.append("sv")
        self.list_codes.append("tg")
        self.list_codes.append("ta")
        self.list_codes.append("tt")
        self.list_codes.append("te")
        self.list_codes.append("th")
        self.list_codes.append("ti")
        self.list_codes.append("ts")
        self.list_codes.append("tr")
        self.list_codes.append("tk")
        self.list_codes.append("tw")
        self.list_codes.append("uk")
        self.list_codes.append("ur")
        self.list_codes.append("ug")
        self.list_codes.append("uz")
        self.list_codes.append("vi")
        self.list_codes.append("cy")
        self.list_codes.append("xh")
        self.list_codes.append("yi")
        self.list_codes.append("yo")
        self.list_codes.append("zu")

        self.list_names = []
        self.list_names.append("Afrikaans")
        self.list_names.append("Albanian")
        self.list_names.append("Amharic")
        self.list_names.append("Arabic")
        self.list_names.append("Armenian")
        self.list_names.append("Assamese")
        self.list_names.append("Aymara")
        self.list_names.append("Azerbaijani")
        self.list_names.append("Bambara")
        self.list_names.append("Basque")
        self.list_names.append("Belarusian")
        self.list_names.append("Bengali")
        self.list_names.append("Bhojpuri")
        self.list_names.append("Bosnian")
        self.list_names.append("Bulgarian")
        self.list_names.append("Catalan")
        self.list_names.append("Cebuano")
        self.list_names.append("Chichewa")
        self.list_names.append("Chinese")
        self.list_names.append("Chinese (Simplified)")
        self.list_names.append("Chinese (Traditional)")
        self.list_names.append("Corsican")
        self.list_names.append("Croatian")
        self.list_names.append("Czech")
        self.list_names.append("Danish")
        self.list_names.append("Dhivehi")
        self.list_names.append("Dogri")
        self.list_names.append("Dutch")
        self.list_names.append("English")
        self.list_names.append("Esperanto")
        self.list_names.append("Estonian")
        self.list_names.append("Ewe")
        self.list_names.append("Filipino")
        self.list_names.append("Finnish")
        self.list_names.append("French")
        self.list_names.append("Frisian")
        self.list_names.append("Galician")
        self.list_names.append("Georgian")
        self.list_names.append("German")
        self.list_names.append("Greek")
        self.list_names.append("Guarani")
        self.list_names.append("Gujarati")
        self.list_names.append("Haitian Creole")
        self.list_names.append("Hausa")
        self.list_names.append("Hawaiian")
        self.list_names.append("Hebrew")
        self.list_names.append("Hindi")
        self.list_names.append("Hmong")
        self.list_names.append("Hungarian")
        self.list_names.append("Icelandic")
        self.list_names.append("Igbo")
        self.list_names.append("Ilocano")
        self.list_names.append("Indonesian")
        self.list_names.append("Irish")
        self.list_names.append("Italian")
        self.list_names.append("Japanese")
        self.list_names.append("Javanese")
        self.list_names.append("Kannada")
        self.list_names.append("Kazakh")
        self.list_names.append("Khmer")
        self.list_names.append("Kinyarwanda")
        self.list_names.append("Konkani")
        self.list_names.append("Korean")
        self.list_names.append("Krio")
        self.list_names.append("Kurdish (Kurmanji)")
        self.list_names.append("Kurdish (Sorani)")
        self.list_names.append("Kyrgyz")
        self.list_names.append("Lao")
        self.list_names.append("Latin")
        self.list_names.append("Latvian")
        self.list_names.append("Lingala")
        self.list_names.append("Lithuanian")
        self.list_names.append("Luganda")
        self.list_names.append("Luxembourgish")
        self.list_names.append("Macedonian")
        self.list_names.append("Malagasy")
        self.list_names.append("Malay")
        self.list_names.append("Malayalam")
        self.list_names.append("Maltese")
        self.list_names.append("Maori")
        self.list_names.append("Marathi")
        self.list_names.append("Meiteilon (Manipuri)")
        self.list_names.append("Mizo")
        self.list_names.append("Mongolian")
        self.list_names.append("Myanmar (Burmese)")
        self.list_names.append("Nepali")
        self.list_names.append("Norwegian")
        self.list_names.append("Odiya (Oriya)")
        self.list_names.append("Oromo")
        self.list_names.append("Pashto")
        self.list_names.append("Persian")
        self.list_names.append("Polish")
        self.list_names.append("Portuguese")
        self.list_names.append("Punjabi")
        self.list_names.append("Quechua")
        self.list_names.append("Romanian")
        self.list_names.append("Russian")
        self.list_names.append("Samoan")
        self.list_names.append("Sanskrit")
        self.list_names.append("Scots Gaelic")
        self.list_names.append("Sepedi")
        self.list_names.append("Serbian")
        self.list_names.append("Sesotho")
        self.list_names.append("Shona")
        self.list_names.append("Sindhi")
        self.list_names.append("Sinhala")
        self.list_names.append("Slovak")
        self.list_names.append("Slovenian")
        self.list_names.append("Somali")
        self.list_names.append("Spanish")
        self.list_names.append("Sundanese")
        self.list_names.append("Swahili")
        self.list_names.append("Swedish")
        self.list_names.append("Tajik")
        self.list_names.append("Tamil")
        self.list_names.append("Tatar")
        self.list_names.append("Telugu")
        self.list_names.append("Thai")
        self.list_names.append("Tigrinya")
        self.list_names.append("Tsonga")
        self.list_names.append("Turkish")
        self.list_names.append("Turkmen")
        self.list_names.append("Twi (Akan)")
        self.list_names.append("Ukrainian")
        self.list_names.append("Urdu")
        self.list_names.append("Uyghur")
        self.list_names.append("Uzbek")
        self.list_names.append("Vietnamese")
        self.list_names.append("Welsh")
        self.list_names.append("Xhosa")
        self.list_names.append("Yiddish")
        self.list_names.append("Yoruba")
        self.list_names.append("Zulu")

        # NOTE THAT Google Translate AND Vosk Speech Recognition API USE ISO-639-1 STANDARD CODE ('al', 'af', 'as', ETC)
        # WHEN ffmpeg SUBTITLES STREAMS USE ISO 639-2 STANDARD CODE ('afr', 'alb', 'amh', ETC)

        self.list_ffmpeg_codes = []
        self.list_ffmpeg_codes.append("afr")  # Afrikaans
        self.list_ffmpeg_codes.append("alb")  # Albanian
        self.list_ffmpeg_codes.append("amh")  # Amharic
        self.list_ffmpeg_codes.append("ara")  # Arabic
        self.list_ffmpeg_codes.append("hye")  # Armenian
        self.list_ffmpeg_codes.append("asm")  # Assamese
        self.list_ffmpeg_codes.append("aym")  # Aymara
        self.list_ffmpeg_codes.append("aze")  # Azerbaijani
        self.list_ffmpeg_codes.append("bam")  # Bambara
        self.list_ffmpeg_codes.append("eus")  # Basque
        self.list_ffmpeg_codes.append("bel")  # Belarusian
        self.list_ffmpeg_codes.append("ben")  # Bengali
        self.list_ffmpeg_codes.append("bho")  # Bhojpuri
        self.list_ffmpeg_codes.append("bos")  # Bosnian
        self.list_ffmpeg_codes.append("bul")  # Bulgarian
        self.list_ffmpeg_codes.append("cat")  # Catalan
        self.list_ffmpeg_codes.append("ceb")  # Cebuano
        self.list_ffmpeg_codes.append("nya")  # Chichewa
        self.list_ffmpeg_codes.append("zho")  # Chinese
        self.list_ffmpeg_codes.append("zho-CN")  # Chinese (Simplified)
        self.list_ffmpeg_codes.append("zho-TW")  # Chinese (Traditional)
        self.list_ffmpeg_codes.append("cos")  # Corsican
        self.list_ffmpeg_codes.append("hrv")  # Croatian
        self.list_ffmpeg_codes.append("ces")  # Czech
        self.list_ffmpeg_codes.append("dan")  # Danish
        self.list_ffmpeg_codes.append("div")  # Dhivehi
        self.list_ffmpeg_codes.append("doi")  # Dogri
        self.list_ffmpeg_codes.append("nld")  # Dutch
        self.list_ffmpeg_codes.append("eng")  # English
        self.list_ffmpeg_codes.append("epo")  # Esperanto
        self.list_ffmpeg_codes.append("est")  # Estonian
        self.list_ffmpeg_codes.append("ewe")  # Ewe
        self.list_ffmpeg_codes.append("fil")  # Filipino
        self.list_ffmpeg_codes.append("fin")  # Finnish
        self.list_ffmpeg_codes.append("fra")  # French
        self.list_ffmpeg_codes.append("fry")  # Frisian
        self.list_ffmpeg_codes.append("glg")  # Galician
        self.list_ffmpeg_codes.append("kat")  # Georgian
        self.list_ffmpeg_codes.append("deu")  # German
        self.list_ffmpeg_codes.append("ell")  # Greek
        self.list_ffmpeg_codes.append("grn")  # Guarani
        self.list_ffmpeg_codes.append("guj")  # Gujarati
        self.list_ffmpeg_codes.append("hat")  # Haitian Creole
        self.list_ffmpeg_codes.append("hau")  # Hausa
        self.list_ffmpeg_codes.append("haw")  # Hawaiian
        self.list_ffmpeg_codes.append("heb")  # Hebrew
        self.list_ffmpeg_codes.append("hin")  # Hindi
        self.list_ffmpeg_codes.append("hmn")  # Hmong
        self.list_ffmpeg_codes.append("hun")  # Hungarian
        self.list_ffmpeg_codes.append("isl")  # Icelandic
        self.list_ffmpeg_codes.append("ibo")  # Igbo
        self.list_ffmpeg_codes.append("ilo")  # Ilocano
        self.list_ffmpeg_codes.append("ind")  # Indonesian
        self.list_ffmpeg_codes.append("gle")  # Irish
        self.list_ffmpeg_codes.append("ita")  # Italian
        self.list_ffmpeg_codes.append("jpn")  # Japanese
        self.list_ffmpeg_codes.append("jav")  # Javanese
        self.list_ffmpeg_codes.append("kan")  # Kannada
        self.list_ffmpeg_codes.append("kaz")  # Kazakh
        self.list_ffmpeg_codes.append("khm")  # Khmer
        self.list_ffmpeg_codes.append("kin")  # Kinyarwanda
        self.list_ffmpeg_codes.append("kok")  # Konkani
        self.list_ffmpeg_codes.append("kor")  # Korean
        self.list_ffmpeg_codes.append("kri")  # Krio
        self.list_ffmpeg_codes.append("kmr")  # Kurdish (Kurmanji)
        self.list_ffmpeg_codes.append("ckb")  # Kurdish (Sorani)
        self.list_ffmpeg_codes.append("kir")  # Kyrgyz
        self.list_ffmpeg_codes.append("lao")  # Lao
        self.list_ffmpeg_codes.append("lat")  # Latin
        self.list_ffmpeg_codes.append("lav")  # Latvian
        self.list_ffmpeg_codes.append("lin")  # Lingala
        self.list_ffmpeg_codes.append("lit")  # Lithuanian
        self.list_ffmpeg_codes.append("lug")  # Luganda
        self.list_ffmpeg_codes.append("ltz")  # Luxembourgish
        self.list_ffmpeg_codes.append("mkd")  # Macedonian
        self.list_ffmpeg_codes.append("mlg")  # Malagasy
        self.list_ffmpeg_codes.append("msa")  # Malay
        self.list_ffmpeg_codes.append("mal")  # Malayalam
        self.list_ffmpeg_codes.append("mlt")  # Maltese
        self.list_ffmpeg_codes.append("mri")  # Maori
        self.list_ffmpeg_codes.append("mar")  # Marathi
        self.list_ffmpeg_codes.append("mni-Mtei")  # Meiteilon (Manipuri)
        self.list_ffmpeg_codes.append("lus")  # Mizo
        self.list_ffmpeg_codes.append("mon")  # Mongolian
        self.list_ffmpeg_codes.append("mya")  # Myanmar (Burmese)
        self.list_ffmpeg_codes.append("nep")  # Nepali
        self.list_ffmpeg_codes.append("nor")  # Norwegian
        self.list_ffmpeg_codes.append("ori")  # Odiya (Oriya)
        self.list_ffmpeg_codes.append("orm")  # Oromo
        self.list_ffmpeg_codes.append("pus")  # Pashto
        self.list_ffmpeg_codes.append("fas")  # Persian
        self.list_ffmpeg_codes.append("pol")  # Polish
        self.list_ffmpeg_codes.append("por")  # Portuguese
        self.list_ffmpeg_codes.append("pan")  # Punjabi
        self.list_ffmpeg_codes.append("que")  # Quechua
        self.list_ffmpeg_codes.append("ron")  # Romanian
        self.list_ffmpeg_codes.append("rus")  # Russian
        self.list_ffmpeg_codes.append("smo")  # Samoan
        self.list_ffmpeg_codes.append("san")  # Sanskrit
        self.list_ffmpeg_codes.append("gla")  # Scots Gaelic
        self.list_ffmpeg_codes.append("nso")  # Sepedi
        self.list_ffmpeg_codes.append("srp")  # Serbian
        self.list_ffmpeg_codes.append("sot")  # Sesotho
        self.list_ffmpeg_codes.append("sna")  # Shona
        self.list_ffmpeg_codes.append("snd")  # Sindhi
        self.list_ffmpeg_codes.append("sin")  # Sinhala
        self.list_ffmpeg_codes.append("slk")  # Slovak
        self.list_ffmpeg_codes.append("slv")  # Slovenian
        self.list_ffmpeg_codes.append("som")  # Somali
        self.list_ffmpeg_codes.append("spa")  # Spanish
        self.list_ffmpeg_codes.append("sun")  # Sundanese
        self.list_ffmpeg_codes.append("swa")  # Swahili
        self.list_ffmpeg_codes.append("swe")  # Swedish
        self.list_ffmpeg_codes.append("tgk")  # Tajik
        self.list_ffmpeg_codes.append("tam")  # Tamil
        self.list_ffmpeg_codes.append("tat")  # Tatar
        self.list_ffmpeg_codes.append("tel")  # Telugu
        self.list_ffmpeg_codes.append("tha")  # Thai
        self.list_ffmpeg_codes.append("tir")  # Tigrinya
        self.list_ffmpeg_codes.append("tso")  # Tsonga
        self.list_ffmpeg_codes.append("tur")  # Turkish
        self.list_ffmpeg_codes.append("tuk")  # Turkmen
        self.list_ffmpeg_codes.append("twi")  # Twi (Akan)
        self.list_ffmpeg_codes.append("ukr")  # Ukrainian
        self.list_ffmpeg_codes.append("urd")  # Urdu
        self.list_ffmpeg_codes.append("uig")  # Uyghur
        self.list_ffmpeg_codes.append("uzb")  # Uzbek
        self.list_ffmpeg_codes.append("vie")  # Vietnamese
        self.list_ffmpeg_codes.append("wel")  # Welsh
        self.list_ffmpeg_codes.append("xho")  # Xhosa
        self.list_ffmpeg_codes.append("yid")  # Yiddish
        self.list_ffmpeg_codes.append("yor")  # Yoruba
        self.list_ffmpeg_codes.append("zul")  # Zulu

        self.code_of_name = dict(zip(self.list_names, self.list_codes))
        self.code_of_ffmpeg_code = dict(zip(self.list_ffmpeg_codes, self.list_codes))

        self.name_of_code = dict(zip(self.list_codes, self.list_names))
        self.name_of_ffmpeg_code = dict(zip(self.list_ffmpeg_codes, self.list_names))

        self.ffmpeg_code_of_name = dict(zip(self.list_names, self.list_ffmpeg_codes))
        self.ffmpeg_code_of_code = dict(zip(self.list_codes, self.list_ffmpeg_codes))

        self.dict = {
                        'af': 'Afrikaans',
                        'sq': 'Albanian',
                        'am': 'Amharic',
                        'ar': 'Arabic',
                        'hy': 'Armenian',
                        'as': 'Assamese',
                        'ay': 'Aymara',
                        'az': 'Azerbaijani',
                        'bm': 'Bambara',
                        'eu': 'Basque',
                        'be': 'Belarusian',
                        'bn': 'Bengali',
                        'bho': 'Bhojpuri',
                        'bs': 'Bosnian',
                        'bg': 'Bulgarian',
                        'ca': 'Catalan',
                        'ceb': 'Cebuano',
                        'ny': 'Chichewa',
                        'zh': 'Chinese',
                        'zh-CN': 'Chinese (Simplified)',
                        'zh-TW': 'Chinese (Traditional)',
                        'co': 'Corsican',
                        'hr': 'Croatian',
                        'cs': 'Czech',
                        'da': 'Danish',
                        'dv': 'Dhivehi',
                        'doi': 'Dogri',
                        'nl': 'Dutch',
                        'en': 'English',
                        'eo': 'Esperanto',
                        'et': 'Estonian',
                        'ee': 'Ewe',
                        'fil': 'Filipino',
                        'fi': 'Finnish',
                        'fr': 'French',
                        'fy': 'Frisian',
                        'gl': 'Galician',
                        'ka': 'Georgian',
                        'de': 'German',
                        'el': 'Greek',
                        'gn': 'Guarani',
                        'gu': 'Gujarati',
                        'ht': 'Haitian Creole',
                        'ha': 'Hausa',
                        'haw': 'Hawaiian',
                        'he': 'Hebrew',
                        'hi': 'Hindi',
                        'hmn': 'Hmong',
                        'hu': 'Hungarian',
                        'is': 'Icelandic',
                        'ig': 'Igbo',
                        'ilo': 'Ilocano',
                        'id': 'Indonesian',
                        'ga': 'Irish',
                        'it': 'Italian',
                        'ja': 'Japanese',
                        'jv': 'Javanese',
                        'kn': 'Kannada',
                        'kk': 'Kazakh',
                        'km': 'Khmer',
                        'rw': 'Kinyarwanda',
                        'gom': 'Konkani',
                        'ko': 'Korean',
                        'kri': 'Krio',
                        'kmr': 'Kurdish (Kurmanji)',
                        'ckb': 'Kurdish (Sorani)',
                        'ky': 'Kyrgyz',
                        'lo': 'Lao',
                        'la': 'Latin',
                        'lv': 'Latvian',
                        'ln': 'Lingala',
                        'lt': 'Lithuanian',
                        'lg': 'Luganda',
                        'lb': 'Luxembourgish',
                        'mk': 'Macedonian',
                        'mg': 'Malagasy',
                        'ms': 'Malay',
                        'ml': 'Malayalam',
                        'mt': 'Maltese',
                        'mi': 'Maori',
                        'mr': 'Marathi',
                        'mni-Mtei': 'Meiteilon (Manipuri)',
                        'lus': 'Mizo',
                        'mn': 'Mongolian',
                        'my': 'Myanmar (Burmese)',
                        'ne': 'Nepali',
                        'no': 'Norwegian',
                        'or': 'Odiya (Oriya)',
                        'om': 'Oromo',
                        'ps': 'Pashto',
                        'fa': 'Persian',
                        'pl': 'Polish',
                        'pt': 'Portuguese',
                        'pa': 'Punjabi',
                        'qu': 'Quechua',
                        'ro': 'Romanian',
                        'ru': 'Russian',
                        'sm': 'Samoan',
                        'sa': 'Sanskrit',
                        'gd': 'Scots Gaelic',
                        'nso': 'Sepedi',
                        'sr': 'Serbian',
                        'st': 'Sesotho',
                        'sn': 'Shona',
                        'sd': 'Sindhi',
                        'si': 'Sinhala',
                        'sk': 'Slovak',
                        'sl': 'Slovenian',
                        'so': 'Somali',
                        'es': 'Spanish',
                        'su': 'Sundanese',
                        'sw': 'Swahili',
                        'sv': 'Swedish',
                        'tg': 'Tajik',
                        'ta': 'Tamil',
                        'tt': 'Tatar',
                        'te': 'Telugu',
                        'th': 'Thai',
                        'ti': 'Tigrinya',
                        'ts': 'Tsonga',
                        'tr': 'Turkish',
                        'tk': 'Turkmen',
                        'tw': 'Twi (Akan)',
                        'uk': 'Ukrainian',
                        'ur': 'Urdu',
                        'ug': 'Uyghur',
                        'uz': 'Uzbek',
                        'vi': 'Vietnamese',
                        'cy': 'Welsh',
                        'xh': 'Xhosa',
                        'yi': 'Yiddish',
                        'yo': 'Yoruba',
                        'zu': 'Zulu',
                    }

        self.ffmpeg_dict = {
                                'af': 'afr', # Afrikaans
                                'sq': 'alb', # Albanian
                                'am': 'amh', # Amharic
                                'ar': 'ara', # Arabic
                                'hy': 'arm', # Armenian
                                'as': 'asm', # Assamese
                                'ay': 'aym', # Aymara
                                'az': 'aze', # Azerbaijani
                                'bm': 'bam', # Bambara
                                'eu': 'baq', # Basque
                                'be': 'bel', # Belarusian
                                'bn': 'ben', # Bengali
                                'bho': 'bho', # Bhojpuri
                                'bs': 'bos', # Bosnian
                                'bg': 'bul', # Bulgarian
                                'ca': 'cat', # Catalan
                                'ceb': 'ceb', # Cebuano
                                'ny': 'nya', # Chichewa
                                'zh': 'chi', # Chinese
                                'zh-CN': 'chi', # Chinese (Simplified)
                                'zh-TW': 'chi', # Chinese (Traditional)
                                'co': 'cos', # Corsican
                                'hr': 'hrv', # Croatian
                                'cs': 'cze', # Czech
                                'da': 'dan', # Danish
                                'dv': 'div', # Dhivehi
                                'doi': 'doi', # Dogri
                                'nl': 'dut', # Dutch
                                'en': 'eng', # English
                                'eo': 'epo', # Esperanto
                                'et': 'est', # Estonian
                                'ee': 'ewe', # Ewe
                                'fil': 'fil', # Filipino
                                'fi': 'fin', # Finnish
                                'fr': 'fre', # French
                                'fy': 'fry', # Frisian
                                'gl': 'glg', # Galician
                                'ka': 'geo', # Georgian
                                'de': 'ger', # German
                                'el': 'gre', # Greek
                                'gn': 'grn', # Guarani
                                'gu': 'guj', # Gujarati
                                'ht': 'hat', # Haitian Creole
                                'ha': 'hau', # Hausa
                                'haw': 'haw', # Hawaiian
                                'he': 'heb', # Hebrew
                                'hi': 'hin', # Hindi
                                'hmn': 'hmn', # Hmong
                                'hu': 'hun', # Hungarian
                                'is': 'ice', # Icelandic
                                'ig': 'ibo', # Igbo
                                'ilo': 'ilo', # Ilocano
                                'id': 'ind', # Indonesian
                                'ga': 'gle', # Irish
                                'it': 'ita', # Italian
                                'ja': 'jpn', # Japanese
                                'jv': 'jav', # Javanese
                                'kn': 'kan', # Kannada
                                'kk': 'kaz', # Kazakh
                                'km': 'khm', # Khmer
                                'rw': 'kin', # Kinyarwanda
                                'gom': 'kok', # Konkani
                                'ko': 'kor', # Korean
                                'kri': 'kri', # Krio
                                'kmr': 'kur', # Kurdish (Kurmanji)
                                'ckb': 'kur', # Kurdish (Sorani)
                                'ky': 'kir', # Kyrgyz
                                'lo': 'lao', # Lao
                                'la': 'lat', # Latin
                                'lv': 'lav', # Latvian
                                'ln': 'lin', # Lingala
                                'lt': 'lit', # Lithuanian
                                'lg': 'lug', # Luganda
                                'lb': 'ltz', # Luxembourgish
                                'mk': 'mac', # Macedonian
                                'mg': 'mlg', # Malagasy
                                'ms': 'may', # Malay
                                'ml': 'mal', # Malayalam
                                'mt': 'mlt', # Maltese
                                'mi': 'mao', # Maori
                                'mr': 'mar', # Marathi
                                'mni-Mtei': 'mni', # Meiteilon (Manipuri)
                                'lus': 'lus', # Mizo
                                'mn': 'mon', # Mongolian
                                'my': 'bur', # Myanmar (Burmese)
                                'ne': 'nep', # Nepali
                                'no': 'nor', # Norwegian
                                'or': 'ori', # Odiya (Oriya)
                                'om': 'orm', # Oromo
                                'ps': 'pus', # Pashto
                                'fa': 'per', # Persian
                                'pl': 'pol', # Polish
                                'pt': 'por', # Portuguese
                                'pa': 'pan', # Punjabi
                                'qu': 'que', # Quechua
                                'ro': 'rum', # Romanian
                                'ru': 'rus', # Russian
                                'sm': 'smo', # Samoan
                                'sa': 'san', # Sanskrit
                                'gd': 'gla', # Scots Gaelic
                                'nso': 'nso', # Sepedi
                                'sr': 'srp', # Serbian
                                'st': 'sot', # Sesotho
                                'sn': 'sna', # Shona
                                'sd': 'snd', # Sindhi
                                'si': 'sin', # Sinhala
                                'sk': 'slo', # Slovak
                                'sl': 'slv', # Slovenian
                                'so': 'som', # Somali
                                'es': 'spa', # Spanish
                                'su': 'sun', # Sundanese
                                'sw': 'swa', # Swahili
                                'sv': 'swe', # Swedish
                                'tg': 'tgk', # Tajik
                                'ta': 'tam', # Tamil
                                'tt': 'tat', # Tatar
                                'te': 'tel', # Telugu
                                'th': 'tha', # Thai
                                'ti': 'tir', # Tigrinya
                                'ts': 'tso', # Tsonga
                                'tr': 'tur', # Turkish
                                'tk': 'tuk', # Turkmen
                                'tw': 'twi', # Twi (Akan)
                                'uk': 'ukr', # Ukrainian
                                'ur': 'urd', # Urdu
                                'ug': 'uig', # Uyghur
                                'uz': 'uzb', # Uzbek
                                'vi': 'vie', # Vietnamese
                                'cy': 'wel', # Welsh
                                'xh': 'xho', # Xhosa
                                'yi': 'yid', # Yiddish
                                'yo': 'yor', # Yoruba
                                'zu': 'zul', # Zulu
                           }

    def get_code_of_name(self, name):
        return self.code_of_name[name]

    def get_code_of_ffmpeg_code(self, ffmpeg_code):
        return self.code_of_ffmpeg_code[ffmpeg_code]

    def get_name_of_code(self, code):
        return self.name_of_code[code]

    def get_name_of_ffmpeg_code(self, ffmpeg_code):
        return self.name_of_ffmpeg_code[ffmpeg_code]

    def get_ffmpeg_code_of_name(self, name):
        return self.ffmpeg_code_of_name[name]

    def get_ffmpeg_code_of_code(self, code):
        return self.ffmpeg_code_of_code[code]


google_unsupported_languages = ["auto", "ba", "br", "fo", "nn", "oc", "tl", "bo"]


class WavConverter:
    @staticmethod
    def which(program):
        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    @staticmethod
    def ffprobe_check():
        if WavConverter.which("ffprobe"):
            return "ffprobe"
        if WavConverter.which("ffprobe.exe"):
            return "ffprobe.exe"
        return None

    @staticmethod
    def ffmpeg_check():
        if WavConverter.which("ffmpeg"):
            return "ffmpeg"
        if WavConverter.which("ffmpeg.exe"):
            return "ffmpeg.exe"
        return None

    def __init__(self, channels=1, rate=48000, progress_callback=None, error_messages_callback=None):
        self.channels = channels
        self.rate = rate
        self.progress_callback = progress_callback
        self.error_messages_callback = error_messages_callback

    def __call__(self, media_filepath):
        temp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)

        if "\\" in media_filepath:
            media_filepath = media_filepath.replace("\\", "/")

        if not os.path.isfile(media_filepath):
            if self.error_messages_callback:
                self.error_messages_callback(f"The given file does not exist: '{media_filepath}'")
            else:
                print(f"The given file does not exist: '{media_filepath}'")
                raise Exception(f"Invalid file: '{media_filepath}'")

        if not self.ffprobe_check():
            if self.error_messages_callback:
                self.error_messages_callback("Cannot find ffprobe executable")
            else:
                print("Cannot find ffprobe executable")
                raise Exception("Dependency not found: ffprobe")

        if not self.ffmpeg_check():
            if self.error_messages_callback:
                self.error_messages_callback("Cannot find ffmpeg executable")
            else:
                print("Cannot find ffmpeg executable")
                raise Exception("Dependency not found: ffmpeg")

        ffmpeg_command = [
                            'ffmpeg',
                            '-hide_banner',
                            '-loglevel', 'error',
                            '-v', 'error',
                            '-y',
                            '-i', media_filepath,
                            '-ac', str(self.channels),
                            '-ar', str(self.rate),
                            '-progress', '-', '-nostats',
                            temp.name
                         ]

        try:
            media_file_display_name = os.path.basename(media_filepath).split('/')[-1]
            info = f"Converting '{media_file_display_name}' to a temporary WAV file"
            start_time = time.time()

            ffprobe_command = [
                                'ffprobe',
                                '-hide_banner',
                                '-v', 'error',
                                '-loglevel', 'error',
                                '-show_entries',
                                'format=duration',
                                '-of', 'default=noprint_wrappers=1:nokey=1',
                                media_filepath
                              ]

            ffprobe_process = None
            if sys.platform == "win32":
                ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True)

            total_duration = float(ffprobe_process.strip())

            process = None
            if sys.platform == "win32":
                process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                if process.stdout is None:
                    continue

                stderr_line = (process.stdout.readline().decode("utf-8", errors="replace").strip())
 
                if stderr_line == '' and process.poll() is not None:
                    break

                if "out_time=" in stderr_line:
                    time_str = stderr_line.split('time=')[1].split()[0]
                    current_duration = sum(float(x) * 1000 * 60 ** i for i, x in enumerate(reversed(time_str.split(":"))))

                    if current_duration>0 and current_duration<=total_duration*1000:
                        percentage = int(current_duration*100/(int(float(total_duration))*1000))
                        if self.progress_callback and percentage <= 100:
                            self.progress_callback(info, media_file_display_name, percentage, start_time)

            temp.close()

            return temp.name, self.rate

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


class SpeechRegionFinder:
    def percentile(self, arr, percent):
        arr = sorted(arr)
        k = (len(arr) - 1) * percent
        f = math.floor(k)
        c = math.ceil(k)
        if f == c: return arr[int(k)]
        d0 = arr[int(f)] * (c - k)
        d1 = arr[int(c)] * (k - f)
        return d0 + d1

    #def __init__(self, frame_width=4096, min_region_size=0.5, max_region_size=6):
    def __init__(self, frame_width=4096, min_region_size=0.5, max_region_size=6, error_messages_callback=None):
        self.frame_width = frame_width
        self.min_region_size = min_region_size
        self.max_region_size = max_region_size
        self.error_messages_callback = error_messages_callback

    def __call__(self, wav_filepath):
        try:
            reader = wave.open(wav_filepath)
            sample_width = reader.getsampwidth()
            rate = reader.getframerate()
            n_channels = reader.getnchannels()
            total_duration = reader.getnframes() / rate
            chunk_duration = float(self.frame_width) / rate
            n_chunks = int(total_duration / chunk_duration)
            energies = []
            for i in range(n_chunks):
                chunk = reader.readframes(self.frame_width)
                energies.append(audioop.rms(chunk, sample_width * n_channels))
            threshold = self.percentile(energies, 0.2)
            elapsed_time = 0
            regions = []
            region_start = None
            for energy in energies:
                is_silence = energy <= threshold
                max_exceeded = region_start and elapsed_time - region_start >= self.max_region_size
                if (max_exceeded or is_silence) and region_start:
                    if elapsed_time - region_start >= self.min_region_size:
                        regions.append((region_start, elapsed_time))
                        region_start = None
                elif (not region_start) and (not is_silence):
                    region_start = elapsed_time
                elapsed_time += chunk_duration
            return regions

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(f"SpeechRegionFinder: {e}")
            else:
                print(e)
            return


class SentenceTranslator(object):
    def __init__(self, src, dst, patience=-1, timeout=30, error_messages_callback=None):
        self.src = src
        self.dst = dst
        self.patience = patience
        self.timeout = timeout
        self.error_messages_callback = error_messages_callback

    def __call__(self, sentence):
        try:
            translated_sentence = []
            # handle the special case: empty string.
            if not sentence:
                return None
            translated_sentence = self.GoogleTranslate(sentence, src=self.src, dst=self.dst, timeout=self.timeout)
            fail_to_translate = translated_sentence[-1] == '\n'
            while fail_to_translate and patience:
                translated_sentence = self.GoogleTranslate(translated_sentence, src=self.src, dst=self.dst, timeout=self.timeout).text
                if translated_sentence[-1] == '\n':
                    if patience == -1:
                        continue
                    patience -= 1
                else:
                    fail_to_translate = False

            return translated_sentence

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return

    def GoogleTranslate(self, text, src, dst, timeout=30):
        url = 'https://translate.googleapis.com/translate_a/'
        params = 'single?client=gtx&sl='+src+'&tl='+dst+'&dt=t&q='+text;
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Referer': 'https://translate.google.com',}

        try:
            response = requests.get(url+params, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                response_json = response.json()[0]
                length = len(response_json)
                translation = ""
                for i in range(length):
                    translation = translation + response_json[i][0]
                return translation
            return

        except requests.exceptions.ConnectionError:
            with httpx.Client() as client:
                response = client.get(url+params, headers=headers, timeout=self.timeout)
                if response.status_code == 200:
                    response_json = response.json()[0]
                    length = len(response_json)
                    translation = ""
                    for i in range(length):
                        translation = translation + response_json[i][0]
                    return translation
                return

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


class SubtitleFormatter:
    supported_formats = ['srt', 'vtt', 'json', 'raw']

    def __init__(self, format_type, error_messages_callback=None):
        self.format_type = format_type.lower()
        self.error_messages_callback = error_messages_callback

    def __call__(self, subtitles, padding_before=0, padding_after=0):
        try:
            if self.format_type == 'srt':
                return self.srt_formatter(subtitles, padding_before, padding_after)
            elif self.format_type == 'vtt':
                return self.vtt_formatter(subtitles, padding_before, padding_after)
            elif self.format_type == 'json':
                return self.json_formatter(subtitles)
            elif self.format_type == 'raw':
                return self.raw_formatter(subtitles)
            else:
                if error_messages_callback:
                    error_messages_callback(f"Unsupported format type: '{self.format_type}'")
                else:
                    raise ValueError(f"Unsupported format type: '{self.format_type}'")

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return

    def srt_formatter(self, subtitles, padding_before=0, padding_after=0):
        """
        Serialize a list of subtitles according to the SRT format, with optional time padding.
        """
        sub_rip_file = pysrt.SubRipFile()
        for i, ((start, end), text) in enumerate(subtitles, start=1):
            item = pysrt.SubRipItem()
            item.index = i
            item.text = six.text_type(text)
            item.start.seconds = max(0, start - padding_before)
            item.end.seconds = end + padding_after
            sub_rip_file.append(item)
        return '\n'.join(six.text_type(item) for item in sub_rip_file)

    def vtt_formatter(self, subtitles, padding_before=0, padding_after=0):
        """
        Serialize a list of subtitles according to the VTT format, with optional time padding.
        """
        text = self.srt_formatter(subtitles, padding_before, padding_after)
        text = 'WEBVTT\n\n' + text.replace(',', '.')
        return text

    def json_formatter(self, subtitles):
        """
        Serialize a list of subtitles as a JSON blob.
        """
        subtitle_dicts = [
            {
                'start': start,
                'end': end,
                'content': text,
            }
            for ((start, end), text)
            in subtitles
        ]
        return json.dumps(subtitle_dicts)

    def raw_formatter(self, subtitles):
        """
        Serialize a list of subtitles as a newline-delimited string.
        """
        return ' '.join(text for (_rng, text) in subtitles)


class SubtitleWriter:
    def __init__(self, regions, transcripts, format, error_messages_callback=None):
        self.regions = regions
        self.transcripts = transcripts
        self.format = format
        self.timed_subtitles = [(r, t) for r, t in zip(self.regions, self.transcripts) if t]
        self.error_messages_callback = error_messages_callback

    def get_timed_subtitles(self):
        return self.timed_subtitles

    def write(self, declared_subtitle_filepath):
        try:
            formatter = SubtitleFormatter(self.format)
            formatted_subtitles = formatter(self.timed_subtitles)
            saved_subtitle_filepath = declared_subtitle_filepath
            if saved_subtitle_filepath:
                subtitle_file_base, subtitle_file_ext = os.path.splitext(saved_subtitle_filepath)
                if not subtitle_file_ext:
                    saved_subtitle_filepath = f"{subtitle_file_base}.{self.format}"
                else:
                    saved_subtitle_filepath = declared_subtitle_filepath
            with open(saved_subtitle_filepath, 'wb') as f:
                f.write(formatted_subtitles.encode("utf-8"))
            #with open(saved_subtitle_filepath, 'a') as f:
            #    f.write("\n")

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


class SubtitleStreamParser:
    @staticmethod
    def which(program):
        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    @staticmethod
    def ffprobe_check():
        if SubtitleStreamParser.which("ffprobe"):
            return "ffprobe"
        if SubtitleStreamParser.which("ffprobe.exe"):
            return "ffprobe.exe"
        return None

    def __init__(self, error_messages_callback=None):
        self.error_messages_callback = error_messages_callback
        self._indexes = []
        self._languages = []
        self._timed_subtitles = []
        self._number_of_streams = 0


    def get_subtitle_streams(self, media_filepath):

        ffprobe_cmd = [
                        'ffprobe',
                        '-hide_banner',
                        '-v', 'error',
                        '-loglevel', 'error',
                        '-print_format', 'json',
                        '-show_entries', 'stream=index:stream_tags=language',
                        '-select_streams', 's',
                        media_filepath
                      ]

        try:
            result = None
            if sys.platform == "win32":
                result = subprocess.run(ffprobe_cmd, stdin=open(os.devnull), capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                result = subprocess.run(ffprobe_cmd, stdin=open(os.devnull), capture_output=True, text=True)

            output = result.stdout

            streams = json.loads(output)['streams']

            subtitle_streams = []
            empty_stream_exists = False

            for index, stream in enumerate(streams, start=1):
                language = stream['tags'].get('language')
                subtitle_streams.append({'index': index, 'language': language})

                # Check if 'No subtitles' stream exists
                if language == 'No subtitles':
                    empty_stream_exists = True

            # Append 'No subtitles' stream if it exists
            if not empty_stream_exists:
                subtitle_streams.append({'index': len(streams) + 1, 'language': 'No subtitles'})

            return subtitle_streams

        except FileNotFoundError:
            if self.error_messages_callback:
                msg = 'ffprobe not found. Make sure it is installed and added to the system PATH.'
                self.error_messages_callback(msg)
            else:
                print(msg)
            return None

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return None

    def get_timed_subtitles(self, media_filepath, subtitle_stream_index):

        ffmpeg_cmd = [
                        'ffmpeg',
                        '-hide_banner',
                        '-loglevel', 'error',
                        '-v', 'error',
                        '-i', media_filepath,
                        '-map', f'0:s:{subtitle_stream_index-1}',
                        '-f', 'srt',
                        '-'
                     ]

        try:
            result = None
            if sys.platform == "win32":
                result = subprocess.run(ffmpeg_cmd, stdin=open(os.devnull), capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                result = subprocess.run(ffmpeg_cmd, stdin=open(os.devnull), capture_output=True, text=True)

            output = result.stdout

            timed_subtitles = []
            subtitle_data = []
            lines = output.strip().split('\n')
            #print(lines)
            subtitles = []
            subtitles = None
            subtitle_blocks = []
            block = []
            for line in lines:
                if line.strip() == '':
                    subtitle_blocks.append(block)
                    block = []
                else:
                    block.append(line.strip())
            subtitle_blocks.append(block)

            # Parse each subtitles block and store as tuple in timed_subtitles list
            for block in subtitle_blocks:
                if block:
                    # Extract start and end times from subtitles block
                    start_time_str, end_time_str = block[1].split(' --> ')
                    time_format = '%H:%M:%S,%f'
                    start_time_time_delta = datetime.strptime(start_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                    start_time_total_seconds = start_time_time_delta.total_seconds()
                    end_time_time_delta = datetime.strptime(end_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                    end_time_total_seconds = end_time_time_delta.total_seconds()
                    # Extract subtitles text from subtitles block
                    subtitles = ' '.join(block[2:])
                    timed_subtitles.append(((start_time_total_seconds, end_time_total_seconds), subtitles))
            return timed_subtitles

        except FileNotFoundError:
            if self.error_messages_callback:
                msg = 'ffmpeg not found. Make sure it is installed and added to the system PATH.'
                self.error_messages_callback(msg)
            else:
                print(msg)
            return None

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return None

    def number_of_streams(self):
        return self._number_of_streams

    def indexes(self):
        return self._indexes

    def languages(self):
        return self._languages

    def timed_subtitles(self):
        return self._timed_subtitles

    def index_of_language(self, language):
        for i in range(self.number_of_streams()):
            if self.languages()[i] == language:
                return i+1
            return

    def language_of_index(self, index):
        return self.languages()[index-1]

    def timed_subtitles_of_index(self, index):
        return self.timed_subtitles()[index-1]

    def timed_subtitles_of_language(self, language):
        for i in range(self.number_of_streams()):
            if self.languages()[i] == language:
                return self.timed_subtitles()[i]

    def __call__(self, media_filepath):
        if "\\" in media_filepath:
            media_filepath = media_filepath.replace("\\", "/")

        if not self.ffprobe_check():
            if self.error_messages_callback:
                self.error_messages_callback("Cannot find ffprobe executable")
            else:
                print("Cannot find ffprobe executable")
                raise Exception("Dependency not found: ffprobe")

        subtitle_streams = self.get_subtitle_streams(media_filepath)
        subtitle_streams_data = []
        if subtitle_streams:
            for subtitle_stream in subtitle_streams:
                subtitle_stream_index = subtitle_stream['index']
                subtitle_stream_language = subtitle_stream['language']
                #print(f"Stream Index: {subtitle_stream_index}, Language: {subtitle_stream_language}")
                subtitle_streams_data.append((subtitle_stream_index, subtitle_stream_language))

        subtitle_data = []
        subtitle_contents = []

        for subtitle_stream_index in range(len(subtitle_streams)):
            index, language = subtitle_streams_data[subtitle_stream_index]
            self._indexes.append(index)
            self._languages.append(language)
            self._timed_subtitles.append(self.get_timed_subtitles(media_filepath, subtitle_stream_index+1))
            subtitle_data.append((index, language, self.get_timed_subtitles(media_filepath, subtitle_stream_index+1)))

        self._number_of_streams = len(subtitle_data)

        return subtitle_data


class MediaSubtitleRenderer:
    @staticmethod
    def which(program):
        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    @staticmethod
    def ffmpeg_check():
        if MediaSubtitleRenderer.which("ffmpeg"):
            return "ffmpeg"
        if MediaSubtitleRenderer.which("ffmpeg.exe"):
            return "ffmpeg.exe"
        return None

    @staticmethod
    def ffprobe_check():
        if MediaSubtitleRenderer.which("ffprobe"):
            return "ffprobe"
        if MediaSubtitleRenderer.which("ffprobe.exe"):
            return "ffprobe.exe"
        return None

    def __init__(self, subtitle_path=None, language=None, output_path=None, progress_callback=None, error_messages_callback=None):
        self.subtitle_path = subtitle_path
        self.language = language
        self.output_path = output_path
        self.progress_callback = progress_callback
        self.error_messages_callback = error_messages_callback

    def __call__(self, media_filepath):
        if "\\" in media_filepath:
            media_filepath = media_filepath.replace("\\", "/")

        if "\\" in self.subtitle_path:
            self.subtitle_path = self.subtitle_path.replace("\\", "/")

        if "\\" in self.output_path:
            self.output_path = self.output_path.replace("\\", "/")

        if not os.path.isfile(media_filepath):
            if self.error_messages_callback:
                self.error_messages_callback(f"The given file does not exist: '{media_filepath}'")
            else:
                print(f"The given file does not exist: '{media_filepath}'")
                raise Exception(f"Invalid file: '{media_filepath}'")

        if not self.ffprobe_check():
            if self.error_messages_callback:
                self.error_messages_callback("Cannot find ffprobe executable")
            else:
                print("Cannot find ffprobe executable")
                raise Exception("Dependency not found: ffprobe")

        if not self.ffmpeg_check():
            if self.error_messages_callback:
                self.error_messages_callback("Cannot find ffmpeg executable")
            else:
                print("Cannot find ffmpeg executable")
                raise Exception("Dependency not found: ffmpeg")

        try:
            scale_switch = "'trunc(iw/2)*2'\:'trunc(ih/2)*2'"
            ffmpeg_command = [
                                'ffmpeg',
                                '-hide_banner',
                                '-loglevel', 'error',
                                '-v', 'error',
                                '-y',
                                '-i', media_filepath,
                                '-vf', f'subtitles={shlex.quote(self.subtitle_path)},scale={scale_switch}',
                                '-c:v', 'libx264',
                                '-crf', '23',
                                '-preset', 'medium',
                                '-c:a', 'copy',
                                '-progress', '-', '-nostats',
                                self.output_path
                             ]

            media_file_display_name = os.path.basename(media_filepath).split('/')[-1]
            info = f"Rendering subtitles file into '{media_file_display_name}'"
            start_time = time.time()

            ffprobe_command = [
                                'ffprobe',
                                '-hide_banner',
                                '-v', 'error',
                                '-loglevel', 'error',
                                '-show_entries',
                                'format=duration',
                                '-of', 'default=noprint_wrappers=1:nokey=1',
                                media_filepath
                              ]

            ffprobe_process = None
            if sys.platform == "win32":
                ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True)

            total_duration = float(ffprobe_process.strip())

            process = None
            if sys.platform == "win32":
                process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                if process.stdout is None:
                    continue

                stderr_line = (process.stdout.readline().decode("utf-8", errors="replace").strip())
 
                if stderr_line == '' and process.poll() is not None:
                    break

                if "out_time=" in stderr_line:
                    time_str = stderr_line.split('time=')[1].split()[0]
                    current_duration = sum(float(x) * 1000 * 60 ** i for i, x in enumerate(reversed(time_str.split(":"))))

                    if current_duration>0 and current_duration<=total_duration*1000:
                        percentage = int(current_duration*100/(int(float(total_duration))*1000))
                        if self.progress_callback and percentage <= 100:
                            self.progress_callback(info, media_file_display_name, percentage, start_time)

            if os.path.isfile(self.output_path):
                return self.output_path
            else:
                return None

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


class MediaSubtitleEmbedder:
    @staticmethod
    def which(program):
        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    @staticmethod
    def ffprobe_check():
        if MediaSubtitleEmbedder.which("ffprobe"):
            return "ffprobe"
        if MediaSubtitleEmbedder.which("ffprobe.exe"):
            return "ffprobe.exe"
        return None

    @staticmethod
    def ffmpeg_check():
        if MediaSubtitleEmbedder.which("ffmpeg"):
            return "ffmpeg"
        if MediaSubtitleEmbedder.which("ffmpeg.exe"):
            return "ffmpeg.exe"
        return None

    def __init__(self, subtitle_path=None, language=None, output_path=None, progress_callback=None, error_messages_callback=None):
        self.subtitle_path = subtitle_path
        self.language = language
        self.output_path = output_path
        self.progress_callback = progress_callback
        self.error_messages_callback = error_messages_callback

    def get_existing_subtitle_language(self, media_filepath):
        # Run ffprobe to get stream information
        if "\\" in media_filepath:
            media_filepath = media_filepath.replace("\\", "/")

        command = [
                    'ffprobe',
                    '-hide_banner',
                    '-v', 'error',
                    '-loglevel', 'error',
                    '-of', 'json',
                    '-show_entries',
                    'format:stream',
                    media_filepath
                  ]

        output = None
        if sys.platform == "win32":
            output = subprocess.run(command, stdin=open(os.devnull), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            output = subprocess.run(command, stdin=open(os.devnull), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        metadata = json.loads(output.stdout)
        streams = metadata['streams']

        # Find the subtitle stream with language metadata
        subtitle_languages = []
        for stream in streams:
            if stream['codec_type'] == 'subtitle' and 'tags' in stream and 'language' in stream['tags']:
                language = stream['tags']['language']
                subtitle_languages.append(language)

        return subtitle_languages

    def __call__(self, media_filepath):
        if "\\" in media_filepath:
            media_filepath = media_filepath.replace("\\", "/")

        if "\\" in self.subtitle_path:
            self.subtitle_path = self.subtitle_path.replace("\\", "/")

        if "\\" in self.output_path:
            self.output_path = self.output_path.replace("\\", "/")

        if not os.path.isfile(media_filepath):
            if self.error_messages_callback:
                self.error_messages_callback(f"The given file does not exist: '{media_filepath}'")
            else:
                print(f"The given file does not exist: '{media_filepath}'")
                raise Exception(f"Invalid file: '{media_filepath}'")

        if not self.ffprobe_check():
            if self.error_messages_callback:
                self.error_messages_callback("Cannot find ffprobe executable")
            else:
                print("Cannot find ffprobe executable")
                raise Exception("Dependency not found: ffprobe")

        if not self.ffmpeg_check():
            if self.error_messages_callback:
                self.error_messages_callback("Cannot find ffmpeg executable")
            else:
                print("Cannot find ffmpeg executable")
                raise Exception("Dependency not found: ffmpeg")

        try:
            existing_languages = self.get_existing_subtitle_language(media_filepath)
            if self.language in existing_languages:
                # THIS 'print' THINGS WILL MAKE progresbar screwed up!
                #msg = (f"'{self.language}' subtitle stream already existed in '{media_filepath}'")
                #if self.error_messages_callback:
                #    self.error_messages_callback(msg)
                #else:
                #    print(msg)
                return

            else:
                # Determine the next available subtitle index
                next_index = len(existing_languages)

                ffmpeg_command = [
                                    'ffmpeg',
                                    '-hide_banner',
                                    '-loglevel', 'error',
                                    '-v', 'error',
                                    '-y',
                                    '-i', media_filepath,
                                    '-sub_charenc', 'UTF-8',
                                    '-i', self.subtitle_path,
                                    '-c:v', 'copy',
                                    '-c:a', 'copy',
                                    '-scodec', 'mov_text',
                                    '-metadata:s:s:' + str(next_index), f'language={shlex.quote(self.language)}',
                                    '-map', '0',
                                    '-map', '1',
                                    '-progress', '-', '-nostats',
                                    self.output_path
                                 ]

                subtitle_file_display_name = os.path.basename(self.subtitle_path).split('/')[-1]
                media_file_display_name = os.path.basename(media_filepath).split('/')[-1]
                info = f"Embedding '{self.language}' subtitles file '{subtitle_file_display_name}' into '{media_file_display_name}'"
                start_time = time.time()

                ffprobe_command = [
                                    'ffprobe',
                                    '-hide_banner',
                                    '-v', 'error',
                                    '-loglevel', 'error',
                                    '-show_entries',
                                    'format=duration',
                                    '-of', 'default=noprint_wrappers=1:nokey=1',
                                    media_filepath
                                  ]

                ffprobe_process = None
                if sys.platform == "win32":
                    ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True)

                total_duration = float(ffprobe_process.strip())

                process = None
                if sys.platform == "win32":
                    process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                while True:
                    if process.stdout is None:
                        continue

                    stderr_line = (process.stdout.readline().decode("utf-8", errors="replace").strip())
 
                    if stderr_line == '' and process.poll() is not None:
                        break

                    if "out_time=" in stderr_line:
                        time_str = stderr_line.split('time=')[1].split()[0]
                        current_duration = sum(float(x) * 1000 * 60 ** i for i, x in enumerate(reversed(time_str.split(":"))))

                        if current_duration>0 and current_duration<=total_duration*1000:
                            percentage = int(current_duration*100/(int(float(total_duration))*1000))
                            if self.progress_callback and percentage <= 100:
                                self.progress_callback(info, media_file_display_name, percentage, start_time)

                if os.path.isfile(self.output_path):
                    return self.output_path
                else:
                    return None

                if os.path.isfile(self.output_path):
                    return self.output_path
                else:
                    return None

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


class MediaSubtitleRemover:
    @staticmethod
    def which(program):
        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    @staticmethod
    def ffprobe_check():
        if MediaSubtitleRemover.which("ffprobe"):
            return "ffprobe"
        if MediaSubtitleRemover.which("ffprobe.exe"):
            return "ffprobe.exe"
        return None

    @staticmethod
    def ffmpeg_check():
        if MediaSubtitleRemover.which("ffmpeg"):
            return "ffmpeg"
        if MediaSubtitleRemover.which("ffmpeg.exe"):
            return "ffmpeg.exe"
        return None

    def __init__(self, output_path=None, progress_callback=None, error_messages_callback=None):
        self.output_path = output_path
        self.progress_callback = progress_callback
        self.error_messages_callback = error_messages_callback

    def __call__(self, media_filepath):
        if "\\" in media_filepath:
            media_filepath = media_filepath.replace("\\", "/")

        if "\\" in self.output_path:
            self.output_path = self.output_path.replace("\\", "/")

        if not os.path.isfile(media_filepath):
            if self.error_messages_callback:
                self.error_messages_callback(f"The given file does not exist: '{media_filepath}'")
            else:
                print(f"The given file does not exist: '{media_filepath}'")
                raise Exception(f"Invalid file: '{media_filepath}'")

        if not self.ffprobe_check():
            if self.error_messages_callback:
                self.error_messages_callback("Cannot find ffprobe executable")
            else:
                print("Cannot find ffprobe executable")
                raise Exception("Dependency not found: ffprobe")

        if not self.ffmpeg_check():
            if self.error_messages_callback:
                self.error_messages_callback("Cannot find ffmpeg executable")
            else:
                print("Cannot find ffmpeg executable")
                raise Exception("Dependency not found: ffmpeg")

        try:
            ffmpeg_command = [
                                'ffmpeg',
                                '-hide_banner',
                                '-loglevel', 'error',
                                '-v', 'error',
                                '-y',
                                '-i', media_filepath,
                                '-c', 'copy',
                                '-sn',
                                '-progress', '-', '-nostats',
                                self.output_path
                             ]

            media_file_display_name = os.path.basename(media_filepath).split('/')[-1]
            info = f"Removing subtitles streams from '{media_file_display_name}'"
            start_time = time.time()

            ffprobe_command = [
                                'ffprobe',
                                '-hide_banner',
                                '-v', 'error',
                                '-loglevel', 'error',
                                '-show_entries',
                                'format=duration',
                                '-of', 'default=noprint_wrappers=1:nokey=1',
                                media_filepath
                              ]

            ffprobe_process = None
            if sys.platform == "win32":
                ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True)

            total_duration = float(ffprobe_process.strip())

            process = None
            if sys.platform == "win32":
                process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                if process.stdout is None:
                    continue

                stderr_line = (process.stdout.readline().decode("utf-8", errors="replace").strip())
 
                if stderr_line == '' and process.poll() is not None:
                    break

                if "out_time=" in stderr_line:
                    time_str = stderr_line.split('time=')[1].split()[0]
                    current_duration = sum(float(x) * 1000 * 60 ** i for i, x in enumerate(reversed(time_str.split(":"))))

                    if current_duration>0 and current_duration<=total_duration*1000:
                        percentage = int(current_duration*100/(int(float(total_duration))*1000))
                        if self.progress_callback and percentage <= 100:
                            self.progress_callback(info, media_file_display_name, percentage, start_time)

            if os.path.isfile(self.output_path):
                return self.output_path
            else:
                return None

            if os.path.isfile(self.output_path):
                return self.output_path
            else:
                return None

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


class SRTFileReader:
    def __init__(self, srt_file_path, error_messages_callback=None):
        self.timed_subtitles = self(srt_file_path)
        self.error_messages_callback = error_messages_callback

    @staticmethod
    def __call__(srt_file_path):
        try:
            """
            Read SRT formatted subtitles file and return subtitles as list of tuples
            """
            timed_subtitles = []
            with open(srt_file_path, 'r') as srt_file:
                lines = srt_file.readlines()
                # Split the subtitles file into subtitles blocks
                subtitle_blocks = []
                block = []
                for line in lines:
                    if line.strip() == '':
                        subtitle_blocks.append(block)
                        block = []
                    else:
                        block.append(line.strip())
                subtitle_blocks.append(block)

                # Parse each subtitles block and store as tuple in timed_subtitles list
                for block in subtitle_blocks:
                    if block:
                        # Extract start and end times from subtitles block
                        start_time_str, end_time_str = block[1].split(' --> ')
                        time_format = '%H:%M:%S,%f'
                        start_time_time_delta = datetime.strptime(start_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                        start_time_total_seconds = start_time_time_delta.total_seconds()
                        end_time_time_delta = datetime.strptime(end_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                        end_time_total_seconds = end_time_time_delta.total_seconds()
                        # Extract subtitles text from subtitles block
                        subtitles = ' '.join(block[2:])
                        timed_subtitles.append(((start_time_total_seconds, end_time_total_seconds), subtitles))
                return timed_subtitles

        except KeyboardInterrupt:
            if self.error_messages_callback:
                self.error_messages_callback("Cancelling all tasks")
            else:
                print("Cancelling all tasks")
            return

        except Exception as e:
            if self.error_messages_callback:
                self.error_messages_callback(e)
            else:
                print(e)
            return


def has_subtitles(media_filepath, error_messages_callback=None):
    def which(program):
        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    def ffmpeg_check():
        if which("ffmpeg"):
            return "ffmpeg"
        if which("ffmpeg.exe"):
            return "ffmpeg.exe"
        return None

    if "\\" in media_filepath:
        media_filepath = media_filepath.replace("\\", "/")

    if not os.path.isfile(media_filepath):
        if error_messages_callback:
           error_messages_callback(f"The given file does not exist: '{media_filepath}'")
        else:
            print(f"The given file does not exist: '{media_filepath}'")
            raise Exception(f"Invalid file: '{media_filepath}'")
    if not ffmpeg_check():
        if error_messages_callback:
            error_messages_callback("Cannot find ffmpeg executable")
        else:
            print("Cannot find ffmpeg executable")
            raise Exception("Dependency not found: ffmpeg")

    try:
        if "\\" in media_filepath:
            media_filepath = media_filepath.replace("\\", "/")

        ffmpeg_cmd = [
                        'ffmpeg',
                        '-hide_banner',
                        '-v', 'error',
                        '-loglevel', 'error',
                        '-y',
                        '-i', media_filepath,
                        '-map', '0:s:0',
                        '-f', 'srt',
                        '-'
                     ]

        result = None
        if sys.platform == "win32":
            result = subprocess.run(ffmpeg_cmd, stdin=open(os.devnull), capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            result = subprocess.run(ffmpeg_cmd, stdin=open(os.devnull), capture_output=True, text=True)

        if result.stdout:
            return True  # Subtitles detected
        else:
            return False  # No subtitles detected

    except Exception as e:
        if self.error_messages_callback:
            self.error_messages_callback(e)
        else:
            print(e)
        return False


def change_code_page(code_page):
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleOutputCP(code_page)
    kernel32.SetConsoleCP(code_page)


def stop_ffmpeg_windows(error_messages_callback=None):
    try:
        tasklist_output = subprocess.check_output(['tasklist'], creationflags=subprocess.CREATE_NO_WINDOW).decode('utf-8')
        ffmpeg_pid = None
        for line in tasklist_output.split('\n'):
            if "ffmpeg" in line:
                ffmpeg_pid = line.split()[1]
                break
        if ffmpeg_pid:
            devnull = open(os.devnull, 'w')
            subprocess.Popen(['taskkill', '/F', '/T', '/PID', ffmpeg_pid], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

    except KeyboardInterrupt:
        if error_messages_callback:
            error_messages_callback("Cancelling all tasks")
        else:
            print("Cancelling all tasks")
        return

    except Exception as e:
        if error_messages_callback:
            error_messages_callback(e)
        else:
            print(e)
        return


def stop_ffmpeg_linux(error_messages_callback=None):
    process_name = 'ffmpeg'
    try:
        output = subprocess.check_output(['ps', '-ef'])
        pid = [line.split()[1] for line in output.decode('utf-8').split('\n') if process_name in line][0]
        subprocess.call(['kill', '-9', str(pid)])
    except IndexError:
        pass

    except KeyboardInterrupt:
        if error_messages_callback:
            error_messages_callback("Cancelling all tasks")
        else:
            print("Cancelling all tasks")
        return

    except Exception as e:
        if error_messages_callback:
            error_messages_callback(e)
        else:
            print(e)
        return


def remove_temp_files(extension, error_messages_callback=None):
    try:
        temp_dir = tempfile.gettempdir()
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith("." + extension):
                    os.remove(os.path.join(root, file))
    except KeyboardInterrupt:
        if error_messages_callback:
            error_messages_callback("Cancelling all tasks")
        else:
            print("Cancelling all tasks")
        return

    except Exception as e:
        if error_messages_callback:
            error_messages_callback(e)
        else:
            print(e)
        return


def is_same_language(src, dst, error_messages_callback=None):
    try:
        return src.split("-")[0] == dst.split("-")[0]
    except Exception as e:
        if error_messages_callback:
            error_messages_callback(e)
        else:
            print(e)
        return


def check_file_type(media_filepath, error_messages_callback=None):
    def which(program):
        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    def ffprobe_check():
        if which("ffprobe"):
            return "ffprobe"
        if which("ffprobe.exe"):
            return "ffprobe.exe"
        return None

    if "\\" in media_filepath:
        media_filepath = media_filepath.replace("\\", "/")

    if not os.path.isfile(media_filepath):
        if error_messages_callback:
           error_messages_callback(f"The given file does not exist: '{media_filepath}'")
        else:
            print(f"The given file does not exist: '{media_filepath}'")
            raise Exception(f"Invalid file: '{media_filepath}'")
    if not ffprobe_check():
        if error_messages_callback:
            error_messages_callback("Cannot find ffprobe executable")
        else:
            print("Cannot find ffprobe executable")
            raise Exception("Dependency not found: ffprobe")

    try:
        ffprobe_cmd = [
                        'ffprobe',
                        '-hide_banner',
                        '-loglevel', 'error',
                        '-v', 'error',
                        '-show_format',
                        '-show_streams',
                        '-print_format',
                        'json',
                        media_filepath
                      ]

        output = None

        if sys.platform == "win32":
            output = subprocess.check_output(ffprobe_cmd, stdin=open(os.devnull), stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW).decode('utf-8')
        else:
            output = subprocess.check_output(ffprobe_cmd, stdin=open(os.devnull), stderr=subprocess.PIPE).decode('utf-8')

        data = json.loads(output)

        if 'streams' in data:
            for stream in data['streams']:
                if 'codec_type' in stream and stream['codec_type'] == 'audio':
                    return 'audio'
                elif 'codec_type' in stream and stream['codec_type'] == 'video':
                    return 'video'

    except (subprocess.CalledProcessError, json.JSONDecodeError):
        pass

    except Exception as e:
        if error_messages_callback:
            error_messages_callback(e)
        else:
            print(e)

    return None


def get_existing_subtitle_language(media_path):
    def which(program):
        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    def ffprobe_check():
        if which("ffprobe"):
            return "ffprobe"
        if which("ffprobe.exe"):
            return "ffprobe.exe"
        return None

    if "\\" in media_filepath:
        media_filepath = media_filepath.replace("\\", "/")

    if not os.path.isfile(media_filepath):
        if error_messages_callback:
           error_messages_callback(f"The given file does not exist: '{media_filepath}'")
        else:
            print(f"The given file does not exist: '{media_filepath}'")
            raise Exception(f"Invalid file: '{media_filepath}'")
    if not ffprobe_check():
        if error_messages_callback:
            error_messages_callback("Cannot find ffprobe executable")
        else:
            print("Cannot find ffprobe executable")
            raise Exception("Dependency not found: ffprobe")

    try:
        # Run ffprobe to get stream information
        command = [
                    'ffprobe',
                    '-hide_banner',
                    '-v', 'error',
                    '-loglevel', 'error',
                    '-of', 'json',
                    '-show_entries',
                    'format:stream',
                    media_path
                  ]

        output = None
        if sys.platform == "win32":
            output = subprocess.run(command, stdin=open(os.devnull), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            output = subprocess.run(command, stdin=open(os.devnull), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        metadata = json.loads(output.stdout)
        streams = metadata['streams']

        # Find the subtitles stream with language metadata
        subtitle_languages = []
        for stream in streams:
            if stream['codec_type'] == 'subtitles' and 'tags' in stream and 'language' in stream['tags']:
                language = stream['tags']['language']
                subtitle_languages.append(language)

        return subtitle_languages

    except Exception as e:
        if self.error_messages_callback:
            self.error_messages_callback(e)
        else:
            print(e)
        return None


def render_subtitle_to_media(media_filepath, media_type, media_ext, subtitle_path, output_path, error_messages_callback=None):
    def which(program):
        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    def ffprobe_check():
        if which("ffprobe"):
            return "ffprobe"
        if which("ffprobe.exe"):
            return "ffprobe.exe"
        return None

    def ffmpeg_check():
        if which("ffmpeg"):
            return "ffmpeg"
        if which("ffmpeg.exe"):
            return "ffmpeg.exe"
        return None

    if "\\" in media_filepath:
        media_filepath = media_filepath.replace("\\", "/")

    if not os.path.isfile(media_filepath):
        if error_messages_callback:
           error_messages_callback(f"The given file does not exist: '{media_filepath}'")
        else:
            print(f"The given file does not exist: '{media_filepath}'")
            raise Exception(f"Invalid file: '{media_filepath}'")
    if not ffprobe_check():
        if error_messages_callback:
            error_messages_callback("Cannot find ffprobe executable")
        else:
            print("Cannot find ffprobe executable")
            raise Exception("Dependency not found: ffprobe")
    if not ffmpeg_check():
        if error_messages_callback:
            error_messages_callback("Cannot find ffmpeg executable")
        else:
            print("Cannot find ffmpeg executable")
            raise Exception("Dependency not found: ffmpeg")

    try:
        if "\\" in media_filepath:
            media_filepath = media_filepath.replace("\\", "/")

        if "\\" in subtitle_path:
            subtitle_path = subtitle_path.replace("\\", "/")

        if "\\" in output_path:
            output_path = output_path.replace("\\", "/")

        scale_switch = "'trunc(iw/2)*2':'trunc(ih/2)*2'"
        ffmpeg_command = [
                            'ffmpeg',
                            '-y',
                            '-i', media_filepath,
                            '-vf', f'subtitles={shlex.quote(self.subtitle_path)},scale={scale_switch}',
                            '-c:v', 'libx264',
                            '-crf', '23',
                            '-preset', 'medium',
                            '-c:a', 'copy',
                            self.output_path
                         ]

        ffprobe_command = [
                            'ffprobe',
                            '-hide_banner',
                            '-v', 'error',
                            '-loglevel', 'error',
                            '-show_entries',
                            'format=duration',
                            '-of', 'default=noprint_wrappers=1:nokey=1',
                            media_filepath
                          ]

        ffprobe_process = None
        if sys.platform == "win32":
            ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True)

        total_duration = float(ffprobe_process.strip())

        widgets = [f"Rendering '{language_code}' subtitles into {media_type} : ", Percentage(), ' ', Bar(marker="#"), ' ', ETA()]
        pbar = ProgressBar(widgets=widgets, maxval=100).start()
        percentage = 0

        process = None
        if sys.platform == "win32":
            process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            if process.stdout is None:
                continue

            stderr_line = (process.stdout.readline().decode("utf-8", errors="replace").strip())
 
            if stderr_line == '' and process.poll() is not None:
                break

            if "out_time=" in stderr_line:
                time_str = stderr_line.split('time=')[1].split()[0]
                current_duration = sum(float(x) * 1000 * 60 ** i for i, x in enumerate(reversed(time_str.split(":"))))

                if current_duration>0 and current_duration<=total_duration*1000:
                    percentage = int(current_duration*100/(int(float(total_duration))*1000))
                    if percentage <= 100:
                        pbar.update(percentage)

        pbar.finish()
        return output_path

    except Exception as e:
        if error_messages_callback:
            error_messages_callback(e)
        else:
            print(e)
        return None


def embed_subtitle_to_media(media_filepath, media_type, subtitle_path, language_code, output_path, error_messages_callback=None):
    def which(program):
        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    def ffmpeg_check():
        if which("ffmpeg"):
            return "ffmpeg"
        if which("ffmpeg.exe"):
            return "ffmpeg.exe"
        return None

    if "\\" in media_filepath:
        media_filepath = media_filepath.replace("\\", "/")

    if not os.path.isfile(media_filepath):
        if error_messages_callback:
           error_messages_callback(f"The given file does not exist: '{media_filepath}'")
        else:
            print(f"The given file does not exist: '{media_filepath}'")
            raise Exception(f"Invalid file: '{media_filepath}'")
    if not ffmpeg_check():
        if error_messages_callback:
            error_messages_callback("Cannot find ffmpeg executable")
        else:
            print("Cannot find ffmpeg executable")
            raise Exception("Dependency not found: ffmpeg")

    try:
        if "\\" in media_filepath:
            media_filepath = media_filepath.replace("\\", "/")

        if "\\" in subtitle_path:
            subtitle_path = subtitle_path.replace("\\", "/")

        if "\\" in output_path:
            output_path = output_path.replace("\\", "/")

        existing_languages = get_existing_subtitle_language(media_filepath)
        if language_code in existing_languages:
            #print(f"'{language_code}' subtitles stream already existed in '{media_filepath}'")
            return

        else:
            # Determine the next available subtitles index
            next_index = len(existing_languages)

            ffmpeg_command = [
                                'ffmpeg',
                                '-hide_banner',
                                '-loglevel', 'error',
                                '-v', 'error',
                                '-y',
                                '-i', media_filepath,
                                '-sub_charenc', 'UTF-8',
                                '-i', subtitle_path,
                                '-c:v', 'copy',
                                '-c:a', 'copy',
                                '-scodec', 'mov_text',
                                '-metadata:s:s:' + str(next_index), f'language={shlex.quote(language_code)}',
                                '-map', '0',
                                '-map', '1',
                                output_path
                             ]

            ffprobe_command = [
                                'ffprobe',
                                '-hide_banner',
                                '-v', 'error',
                                '-loglevel', 'error',
                                '-show_entries',
                                'format=duration',
                                '-of', 'default=noprint_wrappers=1:nokey=1',
                                media_filepath
                             ]

            ffprobe_process = None
            if sys.platform == "win32":
                ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True)

            total_duration = float(ffprobe_process.strip())

            widgets = [f"Embedding '{language_code}' subtitles into {media_type} : ", Percentage(), ' ', Bar(marker="#"), ' ', ETA()]
            pbar = ProgressBar(widgets=widgets, maxval=100).start()
            percentage = 0

            process = None
            if sys.platform == "win32":
                process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                if process.stdout is None:
                    continue

                stderr_line = (process.stdout.readline().decode("utf-8", errors="replace").strip())
 
                if stderr_line == '' and process.poll() is not None:
                    break

                if "out_time=" in stderr_line:
                    time_str = stderr_line.split('time=')[1].split()[0]
                    current_duration = sum(float(x) * 1000 * 60 ** i for i, x in enumerate(reversed(time_str.split(":"))))

                    if current_duration>0 and current_duration<=total_duration*1000:
                        percentage = int(current_duration*100/(int(float(total_duration))*1000))
                        if percentage <= 100:
                            pbar.update(percentage)
            pbar.finish()

            return output_path

        return

    except Exception as e:
        if error_messages_callback:
            error_messages_callback(e)
        else:
            print(e)
        return None


def remove_subtitles_from_media(media_filepath, output_path, progress_callback=None, error_messages_callback=None):
    def which(program):
        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    def ffmpeg_check():
        if which("ffmpeg"):
            return "ffmpeg"
        if which("ffmpeg.exe"):
            return "ffmpeg.exe"
        return None

    if "\\" in media_filepath:
        media_filepath = media_filepath.replace("\\", "/")

    if not os.path.isfile(media_filepath):
        if error_messages_callback:
           error_messages_callback(f"The given file does not exist: '{media_filepath}'")
        else:
            print(f"The given file does not exist: '{media_filepath}'")
            raise Exception(f"Invalid file: '{media_filepath}'")
    if not ffmpeg_check():
        if error_messages_callback:
            error_messages_callback("Cannot find ffmpeg executable")
        else:
            print("Cannot find ffmpeg executable")
            raise Exception("Dependency not found: ffmpeg")

    try:
        if "\\" in media_filepath:
            media_filepath = media_filepath.replace("\\", "/")

        if "\\" in output_path:
            output_path = output_path.replace("\\", "/")

        ffmpeg_command = [
                            'ffmpeg',
                            '-hide_banner',
                            '-loglevel', 'error',
                            '-v', 'error',
                            '-y',
                            '-i', media_filepath,
                            '-c', 'copy',
                            '-sn',
                            '-progress', '-', '-nostats',
                            self.output_path
                         ]

        ffprobe_command = [
                            'ffprobe',
                            '-hide_banner',
                            '-v', 'error',
                            '-loglevel', 'error',
                            '-show_entries',
                            'format=duration',
                            '-of', 'default=noprint_wrappers=1:nokey=1',
                            media_filepath
                          ]

        ffprobe_process = None
        if sys.platform == "win32":
            ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            ffprobe_process = subprocess.check_output(ffprobe_command, stdin=open(os.devnull), universal_newlines=True)

        total_duration = float(ffprobe_process.strip())

        widgets = ["Removing subtitles streams from file : ", Percentage(), ' ', Bar(marker="#"), ' ', ETA()]
        pbar = ProgressBar(widgets=widgets, maxval=100).start()
        percentage = 0

        process = None
        if sys.platform == "win32":
            process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            if process.stdout is None:
                continue

            stderr_line = (process.stdout.readline().decode("utf-8", errors="replace").strip())
 
            if stderr_line == '' and process.poll() is not None:
                break

            if "out_time=" in stderr_line:
                time_str = stderr_line.split('time=')[1].split()[0]
                current_duration = sum(float(x) * 1000 * 60 ** i for i, x in enumerate(reversed(time_str.split(":"))))
                if current_duration>0 and current_duration<=total_duration*1000:
                    percentage = int(current_duration*100/(int(float(total_duration))*1000))
                    if percentage <= 100:
                        pbar.update(percentage)
        pbar.finish()

        return output_path

    except KeyboardInterrupt:
        if error_messages_callback:
            error_messages_callback("Cancelling all tasks")
        else:
            print("Cancelling all tasks")
        return

    except Exception as e:
        if error_messages_callback:
            error_messages_callback(e)
        else:
            print(e)
        return None


def show_progress(info, media_file_display_name, progress, start_time):
    global pbar
    pbar.update(progress)


def show_error_messages(messages):
    print(messages)


def main():
    global pbar

    whisper_models = [
                        "tiny.en",
                        "tiny",
                        "base.en",
                        "base",
                        "small.en",
                        "small",
                        "medium.en",
                        "medium",
                        "large-v1",
                        "large-v2",
                        "large"
                     ]

    devices = ["auto", "cuda", "cpu"]

    compute_types = ["default", "auto", "int8", "int8_float16", "int16", "float16", "float32"]

    if sys.platform == "win32":
        change_code_page(65001)
        stop_ffmpeg_windows(error_messages_callback=show_error_messages)
    else:
        stop_ffmpeg_linux(error_messages_callback=show_error_messages)

    remove_temp_files("wav", error_messages_callback=show_error_messages)

    parser = argparse.ArgumentParser()
    parser.add_argument('source_path', help="Path to the video or audio files to generate subtitles files (use wildcard for multiple files or separate them with a space character e.g. \"file 1.mp4\" \"file 2.mp4\")", nargs='*')
    parser.add_argument('-m', '--model-name', default="small", help="name of whisper model to use")
    parser.add_argument('-lm', '--list-models', help="List of whisper models name", action='store_true')
    parser.add_argument('-d', '--device', default="auto", help="name of the device to use")
    parser.add_argument('-ld', '--list-devices', help="List of supported devices", action='store_true')
    parser.add_argument('-ct', '--compute-type', default="auto", help="name of the compute type (quantization) to use")
    parser.add_argument('-lct', '--list-compute-types', help="List of supported compute types", action='store_true')
    parser.add_argument('-t', '--cpu-threads', default=0, help="Number of threads to use when running on CPU")
    parser.add_argument('-nw', '--num-workers', default=1, help="Number of concurrent calls when running whisper model")
    parser.add_argument('-S', '--src-language', help="Language code of the audio language spoken in video/audio source_path", default="auto")
    parser.add_argument('-D', '--dst-language', help="Desired translation language code for the subtitles", default=None)
    parser.add_argument('-lS', '--list-src-languages', help="List all available src_languages (whisper supported languages)", action='store_true')
    parser.add_argument('-lD', '--list-dst-languages', help="List all available dst_languages (google translate supported languages)", action='store_true')
    parser.add_argument('-F', '--format', help="Desired subtitles format", default="srt")
    parser.add_argument('-lF', '--list-formats', help="List all supported subtitles formats", action='store_true')
    parser.add_argument('-c', '--concurrency', help="Number of concurrent calls for Google Translate API", type=int, default=10)
    parser.add_argument('-es', '--embed-src', help="Boolean value (True or False) for embedding original language subtitles file into video file", type=bool, default=False)
    parser.add_argument('-ed', '--embed-dst', help="Boolean value (True or False) for embedding translated subtitles file into video file", type=bool, default=False)
    parser.add_argument('-fr', '--force-recognize', help="Boolean value (True or False) for re-recognize media file event if it's already has subtitles stream", type=bool, default=False)
    parser.add_argument('-v', '--version', action='version', version=VERSION)

    args = parser.parse_args()

    src_language = args.src_language
    dst_language = args.dst_language

    model_name = args.model_name
    if model_name.endswith(".en"):
        print(f"{model_name} is an English-only model, forcing English detection.")
        args.src_language = "en"
    elif args.src_language != "auto":
        args.src_language = src_language

    model = WhisperModel(model_name, device=args.device, compute_type=args.compute_type, cpu_threads=int(args.cpu_threads), num_workers=int(args.num_workers))

    if args.list_models:
        print("List of whisper models:")
        for model_name in whisper_models:
            print(model_name)
        return 0

    if args.list_devices:
        print("List of supported devices:")
        for device in devices:
            print(device)
        return 0

    if args.list_compute_types:
        print("List of supported compute types:")
        for compute_type in compute_types:
            print(compute_type)
        return 0

    whisper_language = WhisperLanguage()
    google_language = GoogleLanguage()
    google_unsupported_languages = ["auto", "ba", "br", "fo", "nn", "oc", "tl", "bo"]

    if args.list_src_languages:
        print("List of whisper supported languages:")
        for whisper_code, whisper_language in (whisper_language.name_of_code.items()):
            print("%-8s : %s" %(whisper_code, whisper_language))
        return 0

    if args.list_dst_languages:
        print("List of google translate supported languages:")
        for google_code, google_language in sorted(google_language.name_of_code.items()):
            print("%-8s : %s" %(google_code, google_language))
        return 0

    if args.src_language not in whisper_language.name_of_code.keys():
        print("Source language is not supported. Run with --list-whisper-languages to see all whisper supported languages.")
        return 1

    if args.dst_language:
        if not args.dst_language in google_language.name_of_code.keys():
            print("Destination language is not supported. Run with --list-google-languages to see all google translate supported languages.")
            return 1
        if not is_same_language(args.src_language, args.dst_language, error_messages_callback=show_error_messages):
            do_translate = True
        else:
            do_translate = False
    else:
        do_translate = False

    if args.list_formats:
        print("List of supported subtitles formats:")
        for subtitle_format in SubtitleFormatter.supported_formats:
            print(f"{subtitle_format}")
        return 0

    if args.format not in SubtitleFormatter.supported_formats:
        print("Subtitles format is not supported. Run with --list-formats to see all supported formats.")
        return 1

    if not args.source_path:
        parser.print_help(sys.stderr)
        return 1

    completed_tasks = 0
    media_filepaths = []
    arg_filepaths = []
    invalid_media_filepaths = []
    not_exist_filepaths = []
    argpath = None
    media_type = None
    media_format = None

    args_source_path = args.source_path
    subtitle_format = args.format

    if (not "*" in str(args_source_path)) and (not "?" in str(args_source_path)):
        for filepath in args_source_path:
            fpath = Path(filepath)
            if not os.path.isfile(fpath):
                not_exist_filepaths.append(filepath)

    if sys.platform == "win32":
        for i in range(len(args.source_path)):
            if ("[" or "]") in args.source_path[i]:
                placeholder = "#TEMP#"
                args_source_path[i] = args.source_path[i].replace("[", placeholder)
                args_source_path[i] = args_source_path[i].replace("]", "[]]")
                args_source_path[i] = args_source_path[i].replace(placeholder, "[[]")

    for arg in args_source_path:
        if not sys.platform == "win32" :
            arg = escape(arg)

        arg_filepaths += glob(arg)

    if arg_filepaths:
        for argpath in arg_filepaths:
            if os.path.isfile(argpath):
                if check_file_type(argpath, error_messages_callback=show_error_messages) == 'video':
                    media_filepaths.append(argpath)
                elif check_file_type(argpath, error_messages_callback=show_error_messages) == 'audio':
                    media_filepaths.append(argpath)
                else:
                    invalid_media_filepaths.append(argpath)
            else:
                not_exist_filepaths.append(argpath)

        if invalid_media_filepaths:
            for invalid_media_filepath in invalid_media_filepaths:
                msg = f"'{invalid_media_filepath}' is not valid video or audio files"
                print(msg)

    if not_exist_filepaths:
        for not_exist_filepath in not_exist_filepaths:
            msg = f"'{not_exist_filepath}' is not exist"
            print(msg)
        if (not "*" in str(args_source_path)) and (not "?" in str(args_source_path)):
            sys.exit(0)

    if not arg_filepaths and not not_exist_filepaths:
        print("No any files matching filenames you typed")
        sys.exit(0)

    pool = multiprocessing.Pool(args.concurrency)

    transcribe_end_time = None
    transcribe_elapsed_time = None
    transcribe_start_time = time.time()
    task = "transcribe"
    total_duration = 0

    src_subtitle_filepath = None
    dst_subtitle_filepath = None
    ffmpeg_src_language_code = None
    ffmpeg_dst_language_code = None
    embedded_media_filepath = None

    if args.src_language in google_unsupported_languages and do_translate:
        task = "translate"
        src_language = "en"

    removed_media_filepaths = []
    processed_list = []

    dst_language = args.dst_language


    # CHECK SUBTITLE STREAM PART
    if args.force_recognize == False:

        print("CHECKING EXISTING SUBTITLES STREAMS")
        print("===================================")

        # CHECKING ffmpeg_src_language_code SUBTITLES STREAM ONLY, IF EXISTS WE PRINT IT AND EXTRACT IT
        if do_translate == False:

            for media_filepath in media_filepaths:

                print(f"Checking '{media_filepath}'")

                media_type = check_file_type(media_filepath, error_messages_callback=show_error_messages)
                if media_type == "audio":
                    print("Audio file won't has subtitles streams, skip checking\n")
                    continue

                if args.src_language == "auto":
                    try:
                        widgets = ["Converting to a temporary WAV file      : ", Percentage(), ' ', Bar(), ' ', ETA()]
                        pbar = ProgressBar(widgets=widgets, maxval=100).start()
                        wav_converter = WavConverter(progress_callback=show_progress, error_messages_callback=show_error_messages)
                        wav_filepath, sample_rate = wav_converter(media_filepath)
                        pbar.finish()

                        region_finder = SpeechRegionFinder(frame_width=4096, min_region_size=0.5, max_region_size=6, error_messages_callback=show_error_messages)
                        regions = region_finder(wav_filepath)

                        if regions:
                            segments, info = model.transcribe(wav_filepath)
                            src_language = info.language
                            print(f"Detected language                       : {info.language} (probability = {info.language_probability})")
                        else:
                            print("No speech regions found")
                            sys.exit(1)

                    except KeyboardInterrupt:
                        pbar.finish()
                        pool.terminate()
                        pool.close()
                        pool.join()
                        print("Cancelling all tasks")

                        if sys.platform == "win32":
                            stop_ffmpeg_windows(error_messages_callback=show_error_messages)
                        else:
                            stop_ffmpeg_linux(error_messages_callback=show_error_messages)

                        remove_temp_files("wav")
                        sys.exit(1)

                    except Exception as e:
                        if not KeyboardInterrupt in str(e):
                            pbar.finish()
                            pool.terminate()
                            pool.close()
                            pool.join()
                            print(e)

                            if sys.platform == "win32":
                                stop_ffmpeg_windows(error_messages_callback=show_error_messages)
                            else:
                                stop_ffmpeg_linux(error_messages_callback=show_error_messages)

                            remove_temp_files("wav")
                            sys.exit(1)

                else:
                    src_language = args.src_language

                if src_language in google_unsupported_languages and args.force_recognize==False:
                    print("Language is not supported by Google Translate API")
                    print(f"Removing '{media_filepath}' from speech recognition process list")
                    removed_media_filepaths.append(media_filepath)

                    #print("removed_media_filepaths = ", removed_media_filepaths)
                    #print("media_filepaths = ", media_filepaths)
                    #print("processed_list = ", processed_list)
                    #print("len(removed_media_filepaths) = ", len(removed_media_filepaths))
                    #print("len(media_filepaths) = ", len(media_filepaths))
                    #print("len(processed_list) = ", len(processed_list))
                    #print("")

                else:
                    ffmpeg_src_language_code = google_language.ffmpeg_code_of_code[src_language]

                    subtitle_stream_parser = SubtitleStreamParser(error_messages_callback=show_error_messages)
                    subtitle_streams_data = subtitle_stream_parser(media_filepath)

                    if subtitle_streams_data and subtitle_streams_data != []:

                        src_subtitle_stream_timed_subtitles = subtitle_stream_parser.timed_subtitles_of_language(ffmpeg_src_language_code)

                        if ffmpeg_src_language_code in subtitle_stream_parser.languages():
                            print(f"Is '{ffmpeg_src_language_code}' subtitles stream exist         : Yes")

                            subtitle_stream_regions = []
                            subtitle_stream_transcripts = []
                            for entry in src_subtitle_stream_timed_subtitles:
                                subtitle_stream_regions.append(entry[0])
                                subtitle_stream_transcripts.append(entry[1])

                            base, ext = os.path.splitext(media_filepath)
                            src_subtitle_filepath = f"{base}.{src_language}.{subtitle_format}"

                            print(f"Extracting '{ffmpeg_src_language_code}' subtitles stream as    : '{src_subtitle_filepath}'")

                            writer = SubtitleWriter(subtitle_stream_regions, subtitle_stream_transcripts, subtitle_format, error_messages_callback=show_error_messages)
                            writer.write(src_subtitle_filepath)

                            # no translate process as instructed in command arguments

                            # if args.embed_src is True we can't embed it because dst subtitles stream already exist
                            if args.embed_src == True and src_subtitle_stream_timed_subtitles and src_subtitle_stream_timed_subtitles != []:
                                print(f"No need to embed '{ffmpeg_src_language_code}' subtitles stream because it's already existed")

                            if args.force_recognize == False:
                                print(f"Removing '{media_filepath}' from speech recognition process list")
                                removed_media_filepaths.append(media_filepath)

                                #print("removed_media_filepaths = ", removed_media_filepaths)
                                #print("media_filepaths = ", media_filepaths)
                                #print("processed_list = ", processed_list)
                                #print("len(removed_media_filepaths) = ", len(removed_media_filepaths))
                                #print("len(media_filepaths) = ", len(media_filepaths))
                                #print("len(processed_list) = ", len(processed_list))
                                #print("")

                            if os.path.isfile(src_subtitle_filepath):
                                completed_tasks += 1
                                #print(f"args.force_recognize == False, do_translate == False, media_type == 'video', subtitle stream = exist : completed_tasks = {completed_tasks}")

                        else:
                            print(f"Is '{ffmpeg_src_language_code}' subtitles stream exist         : No")

                print("")

            #print("removed_media_filepaths = ", removed_media_filepaths)
            #print("media_filepaths = ", media_filepaths)
            #print("processed_list = ", processed_list)
            #print("len(removed_media_filepaths) = ", len(removed_media_filepaths))
            #print("len(media_filepaths) = ", len(media_filepaths))
            #print("len(processed_list) = ", len(processed_list))
            #print("")

            if not media_filepaths:
                transcribe_end_time = time.time()
                transcribe_elapsed_time = transcribe_end_time - transcribe_start_time
                transcribe_elapsed_time_seconds = timedelta(seconds=int(transcribe_elapsed_time))
                transcribe_elapsed_time_str = str(transcribe_elapsed_time_seconds)
                hour, minute, second = transcribe_elapsed_time_str.split(":")
                msg = "Total running time                      : %s:%s:%s" %(hour.zfill(2), minute, second)
                print(msg)
                sys.exit(0)

        # CHECKING ffmpeg_src_language_code AND ffmpeg_dst_language_code SUBTITLES STREAMS, IF EXISTS WE PRINT IT AND EXTRACT IT
        # IF ONE OF THEM (ffmpeg_src_language_code OR ffmpeg_dst_language_code) NOT EXIST, WE TRANSLATE IT AND THEN EMBED IT
        elif do_translate == True:
            for media_filepath in media_filepaths:

                print(f"Checking '{media_filepath}'")

                media_type = check_file_type(media_filepath, error_messages_callback=show_error_messages)
                if media_type == "audio":
                    print("Audio file won't has subtitles streams, skip checking\n")
                    continue

                if args.src_language == "auto":
                    try:
                        widgets = ["Converting to a temporary WAV file      : ", Percentage(), ' ', Bar(), ' ', ETA()]
                        pbar = ProgressBar(widgets=widgets, maxval=100).start()
                        wav_converter = WavConverter(progress_callback=show_progress, error_messages_callback=show_error_messages)
                        wav_filepath, sample_rate = wav_converter(media_filepath)
                        pbar.finish()

                        region_finder = SpeechRegionFinder(frame_width=4096, min_region_size=0.5, max_region_size=6, error_messages_callback=show_error_messages)
                        regions = region_finder(wav_filepath)

                        if regions:
                            segments, info = model.transcribe(wav_filepath)
                            src_language = info.language
                            print(f"Detected language                       : {info.language} (probability = {info.language_probability})")
                        else:
                            print("No speech regions found")
                            sys.exit(1)


                    except KeyboardInterrupt:
                        pbar.finish()
                        pool.terminate()
                        pool.close()
                        pool.join()
                        print("Cancelling all tasks")

                        if sys.platform == "win32":
                            stop_ffmpeg_windows(error_messages_callback=show_error_messages)
                        else:
                            stop_ffmpeg_linux(error_messages_callback=show_error_messages)

                        remove_temp_files("wav")
                        sys.exit(1)

                    except Exception as e:
                        if not KeyboardInterrupt in str(e):
                            pbar.finish()
                            pool.terminate()
                            pool.close()
                            pool.join()
                            print(e)

                            if sys.platform == "win32":
                                stop_ffmpeg_windows(error_messages_callback=show_error_messages)
                            else:
                                stop_ffmpeg_linux(error_messages_callback=show_error_messages)

                            remove_temp_files("wav")
                            sys.exit(1)

                else:
                    src_language = args.src_language

                if src_language in google_unsupported_languages and args.force_recognize==False:
                    print(f"Language '{src_language}' is not supported by Google Translate API")
                    print(f"Removing '{media_filepath}' from speech recognition process list")
                    removed_media_filepaths.append(media_filepath)

                    #print("removed_media_filepaths = ", removed_media_filepaths)
                    #print("media_filepaths = ", media_filepaths)
                    #print("processed_list = ", processed_list)
                    #print("len(removed_media_filepaths) = ", len(removed_media_filepaths))
                    #print("len(media_filepaths) = ", len(media_filepaths))
                    #print("len(processed_list) = ", len(processed_list))
                    #print("")

                else:
                    ffmpeg_src_language_code = google_language.ffmpeg_code_of_code[src_language]
                    ffmpeg_dst_language_code = google_language.ffmpeg_code_of_code[dst_language]

                    subtitle_stream_parser = SubtitleStreamParser(error_messages_callback=show_error_messages)
                    subtitle_streams_data = subtitle_stream_parser(media_filepath)

                    if subtitle_streams_data and subtitle_streams_data != []:

                        src_subtitle_stream_timed_subtitles = subtitle_stream_parser.timed_subtitles_of_language(ffmpeg_src_language_code)
                        dst_subtitle_stream_timed_subtitles = subtitle_stream_parser.timed_subtitles_of_language(ffmpeg_dst_language_code)

                        # ffmpeg_src_language_code subtitles stream exist, we print it and extract it
                        if ffmpeg_src_language_code in subtitle_stream_parser.languages():
                            print(f"Is '{ffmpeg_src_language_code}' subtitles stream exist         : Yes")

                            subtitle_stream_regions = []
                            subtitle_stream_transcripts = []
                            for entry in src_subtitle_stream_timed_subtitles:
                                subtitle_stream_regions.append(entry[0])
                                subtitle_stream_transcripts.append(entry[1])

                            base, ext = os.path.splitext(media_filepath)
                            src_subtitle_filepath = f"{base}.{src_language}.{subtitle_format}"

                            print(f"Extracting '{ffmpeg_src_language_code}' subtitles stream as    : '{src_subtitle_filepath}'")

                            writer = SubtitleWriter(subtitle_stream_regions, subtitle_stream_transcripts, subtitle_format, error_messages_callback=show_error_messages)
                            writer.write(src_subtitle_filepath)

                        # ffmpeg_src_language_code subtitles stream not exist, just print it
                        else:
                            print(f"Is '{ffmpeg_src_language_code}' subtitles stream exist         : No")

                        # ffmpeg_src_language_code subtitles stream exist, we print it and extract it
                        if ffmpeg_dst_language_code in subtitle_stream_parser.languages():
                            print(f"Is '{ffmpeg_dst_language_code}' subtitles stream exist         : Yes")

                            subtitle_stream_regions = []
                            subtitle_stream_transcripts = []
                            for entry in dst_subtitle_stream_timed_subtitles:
                                subtitle_stream_regions.append(entry[0])
                                subtitle_stream_transcripts.append(entry[1])
                            base, ext = os.path.splitext(media_filepath)
                            dst_subtitle_filepath = f"{base}.{dst_language}.{subtitle_format}"
                            writer = SubtitleWriter(subtitle_stream_regions, subtitle_stream_transcripts, subtitle_format, error_messages_callback=show_error_messages)
                            print(f"Extracting '{ffmpeg_dst_language_code}' subtitles stream as    : '{dst_subtitle_filepath}'")
                            writer.write(dst_subtitle_filepath)

                        # ffmpeg_dst_language_code subtitles stream not exist, just print it
                        else:
                            print(f"Is '{ffmpeg_dst_language_code}' subtitles stream exist         : No")

                        # ffmpeg_src_language_code subtitles stream = not exist,
                        # ffmpeg_dst_language_code subtitles stream = exist,
                        # so we translate it from 'dst_language' to 'src_language'
                        if ffmpeg_dst_language_code in subtitle_stream_parser.languages() and ffmpeg_src_language_code not in subtitle_stream_parser.languages():

                            if dst_subtitle_stream_timed_subtitles and dst_subtitle_stream_timed_subtitles != []:
                                prompt = "Translating from %s to %s   : " %(dst_language.center(8), src_language.center(8))
                                widgets = [prompt, Percentage(), ' ', Bar(), ' ', ETA()]
                                pbar = ProgressBar(widgets=widgets, maxval=len(dst_subtitle_stream_timed_subtitles)).start()

                                transcript_translator = SentenceTranslator(src=dst_language, dst=src_language, error_messages_callback=show_error_messages)

                                translated_subtitle_stream_transcripts = []
                                for i, translated_subtitle_stream_transcript in enumerate(pool.imap(transcript_translator, subtitle_stream_transcripts)):
                                    translated_subtitle_stream_transcripts.append(translated_subtitle_stream_transcript)
                                    pbar.update(i)
                                pbar.finish()

                                base, ext = os.path.splitext(media_filepath)
                                src_subtitle_filepath = f"{base}.{src_language}.{subtitle_format}"

                                translation_writer = SubtitleWriter(subtitle_stream_regions, translated_subtitle_stream_transcripts, subtitle_format, error_messages_callback=show_error_messages)
                                translation_writer.write(src_subtitle_filepath)

                                print(f"Translated subtitles file saved as      : '{src_subtitle_filepath}'")

                                if args.force_recognize == False:
                                    print(f"Removing '{media_filepath}' from speech recognition process list")
                                    removed_media_filepaths.append(media_filepath)

                                    #print("removed_media_filepaths = ", removed_media_filepaths)
                                    #print("media_filepaths = ", media_filepaths)
                                    #print("processed_list = ", processed_list)
                                    #print("len(removed_media_filepaths) = ", len(removed_media_filepaths))
                                    #print("len(media_filepaths) = ", len(media_filepaths))
                                    #print("len(processed_list) = ", len(processed_list))
                                    #print("")

                                if args.embed_src and dst_subtitle_stream_timed_subtitles and dst_subtitle_stream_timed_subtitles != []:
                                    ffmpeg_src_language_code = google_language.ffmpeg_code_of_code[src_language]

                                    base, ext = os.path.splitext(media_filepath)

                                    if ext[1:] == "ts":
                                        media_format = "mp4"
                                    else:
                                        media_format = ext[1:]

                                    src_tmp_embedded_media_filepath = f"{base}.{ffmpeg_src_language_code}.tmp.embedded.{media_format}"
                                    embedded_media_filepath = f"{base}.{ffmpeg_src_language_code}.embedded.{media_format}"

                                    widgets = [f"Embedding '{ffmpeg_src_language_code}' subtitles into {media_type}    : ", Percentage(), ' ', Bar(marker="#"), ' ', ETA()]
                                    pbar = ProgressBar(widgets=widgets, maxval=100).start()
                                    subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=src_subtitle_filepath, language=ffmpeg_src_language_code, output_path=src_tmp_embedded_media_filepath, progress_callback=show_progress, error_messages_callback=show_error_messages)
                                    src_tmp_output = subtitle_embedder(media_filepath)
                                    pbar.finish()

                                    if os.path.isfile(src_tmp_output):
                                        shutil.copy(src_tmp_output, embedded_media_filepath)
                                        os.remove(src_tmp_output)

                                    if os.path.isfile(embedded_media_filepath):
                                        print(f"Subtitles embedded {media_type} file saved as  : '{embedded_media_filepath}'")

                                # if args.embed_dst is True we can't embed it because dst subtitles stream already exist
                                if args.embed_dst == True and dst_subtitle_stream_timed_subtitles and dst_subtitle_stream_timed_subtitles != []:
                                    print(f"No need to embed '{ffmpeg_dst_language_code}' subtitles stream because it's already existed")

                        # ffmpeg_src_language_code subtitles stream = exist,
                        # ffmpeg_dst_language_code subtitles stream = not exist,
                        # so we translate it from 'src_language' to 'dst_language'
                        if ffmpeg_dst_language_code not in subtitle_stream_parser.languages() and ffmpeg_src_language_code in subtitle_stream_parser.languages():

                            if src_subtitle_stream_timed_subtitles and src_subtitle_stream_timed_subtitles != []:
                                prompt = "Translating from %s to %s   : " %(src_language.center(8), dst_language.center(8))
                                widgets = [prompt, Percentage(), ' ', Bar(), ' ', ETA()]
                                pbar = ProgressBar(widgets=widgets, maxval=len(src_subtitle_stream_timed_subtitles)).start()

                                transcript_translator = SentenceTranslator(src=src_language, dst=dst_language, error_messages_callback=show_error_messages)

                                translated_subtitle_stream_transcripts = []
                                for i, translated_subtitle_stream_transcript in enumerate(pool.imap(transcript_translator, subtitle_stream_transcripts)):
                                    translated_subtitle_stream_transcripts.append(translated_subtitle_stream_transcript)
                                    pbar.update(i)
                                pbar.finish()

                                base, ext = os.path.splitext(media_filepath)
                                dst_subtitle_filepath = f"{base}.{dst_language}.{subtitle_format}"

                                translation_writer = SubtitleWriter(subtitle_stream_regions, translated_subtitle_stream_transcripts, subtitle_format, error_messages_callback=show_error_messages)
                                translation_writer.write(dst_subtitle_filepath)

                                print(f"Translated subtitles file saved as      : '{dst_subtitle_filepath}'")

                                if args.force_recognize == False:
                                    print(f"Removing '{media_filepath}' from speech recognition process list")
                                    removed_media_filepaths.append(media_filepath)

                                    #print("removed_media_filepaths = ", removed_media_filepaths)
                                    #print("media_filepaths = ", media_filepaths)
                                    #print("processed_list = ", processed_list)
                                    #print("len(removed_media_filepaths) = ", len(removed_media_filepaths))
                                    #print("len(media_filepaths) = ", len(media_filepaths))
                                    #print("len(processed_list) = ", len(processed_list))
                                    #print("")

                                if args.embed_dst == True and src_subtitle_stream_timed_subtitles and src_subtitle_stream_timed_subtitles != []:
                                    ffmpeg_dst_language_code = google_language.ffmpeg_code_of_code[dst_language]

                                    base, ext = os.path.splitext(media_filepath)

                                    if ext[1:] == "ts":
                                        media_format = "mp4"
                                    else:
                                        media_format = ext[1:]

                                    dst_tmp_embedded_media_filepath = f"{base}.{ffmpeg_dst_language_code}.tmp.embedded.{media_format}"
                                    embedded_media_filepath = f"{base}.{ffmpeg_dst_language_code}.embedded.{media_format}"

                                    widgets = [f"Embedding '{ffmpeg_dst_language_code}' subtitles into {media_type}    : ", Percentage(), ' ', Bar(marker="#"), ' ', ETA()]
                                    pbar = ProgressBar(widgets=widgets, maxval=100).start()
                                    subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=dst_subtitle_filepath, language=ffmpeg_dst_language_code, output_path=dst_tmp_embedded_media_filepath, progress_callback=show_progress, error_messages_callback=show_error_messages)
                                    dst_tmp_output = subtitle_embedder(media_filepath)
                                    pbar.finish()

                                    if os.path.isfile(dst_tmp_output):
                                        shutil.copy(dst_tmp_output, embedded_media_filepath)
                                        os.remove(dst_tmp_output)

                                    if os.path.isfile(embedded_media_filepath):
                                        print(f"Subtitles embedded {media_type} file saved as  : '{embedded_media_filepath}'")

                                # if args.embed_src is True then no need to embed it because src subtitles stream already exist
                                if args.embed_src == True and src_subtitle_stream_timed_subtitles and src_subtitle_stream_timed_subtitles != []:
                                    print(f"No need to embed '{ffmpeg_src_language_code}' subtitles stream because it's already existed")

                        # ffmpeg_dst_language_code subtitles stream = exist,
                        # ffmpeg_src_language_code subtitles stream = exist,
                        # so we remove media_filepath from the list of files to be processed
                        elif ffmpeg_dst_language_code in subtitle_stream_parser.languages() and ffmpeg_src_language_code in subtitle_stream_parser.languages():

                            # remove media_filepath from transcribe processed_list because all needed srt files already saved
                            if args.force_recognize == False:
                                print(f"Removing '{media_filepath}' from speech recognition process list")
                                removed_media_filepaths.append(media_filepath)

                                #print("removed_media_filepaths = ", removed_media_filepaths)
                                #print("media_filepaths = ", media_filepaths)
                                #print("processed_list = ", processed_list)
                                #print("len(removed_media_filepaths) = ", len(removed_media_filepaths))
                                #print("len(media_filepaths) = ", len(media_filepaths))
                                #print("len(processed_list) = ", len(processed_list))
                                #print("")

                            # no need to translate becouse both languages subtitles files already saved

                            # if args.embed_src is True we can't embed it because dst subtitles stream already exist
                            if args.embed_src == True and src_subtitle_stream_timed_subtitles and src_subtitle_stream_timed_subtitles != []:
                                print(f"No need to embed '{ffmpeg_src_language_code}' subtitles stream because it's already existed")

                            # if args.embed_dst is True we can't embed it because dst subtitles stream already exist
                            if args.embed_dst == True and dst_subtitle_stream_timed_subtitles and dst_subtitle_stream_timed_subtitles != []:
                                print(f"No need to embed '{ffmpeg_dst_language_code}' subtitles stream because it's already existed")

                        if (src_subtitle_filepath and os.path.isfile(src_subtitle_filepath)) or (dst_subtitle_filepath and os.path.isfile(dst_subtitle_filepath)):
                            if args.force_recognize == False:
                                completed_tasks += 1
                                #print(f"\nargs.force_recognize == False, do_translate == True, media_type == 'video', subtitle stream = exist : completed_tasks = {completed_tasks}\n")

                print("")
            print("")

            #print("removed_media_filepaths = ", removed_media_filepaths)
            #print("media_filepaths = ", media_filepaths)
            #print("processed_list = ", processed_list)
            #print("len(removed_media_filepaths) = ", len(removed_media_filepaths))
            #print("len(media_filepaths) = ", len(media_filepaths))
            #print("len(processed_list) = ", len(processed_list))
            #print("")

            if not media_filepaths:
                transcribe_end_time = time.time()
                transcribe_elapsed_time = transcribe_end_time - transcribe_start_time
                transcribe_elapsed_time_seconds = timedelta(seconds=int(transcribe_elapsed_time))
                transcribe_elapsed_time_str = str(transcribe_elapsed_time_seconds)
                hour, minute, second = transcribe_elapsed_time_str.split(":")
                msg = "Total running time                      : %s:%s:%s" %(hour.zfill(2), minute, second)
                print(msg)
                sys.exit(0)


    if args.force_recognize == True:
        # SUBTITLES STREAMS REMOVER PART (IF args.force_recognize == True)
        print("FORCE RECOGNIZE FLAG CHECK")
        print("==========================")

        # if args.force_recognize is true then we need to remove subtitle streams and save it as new media file to processed with transcribe
        for media_filepath in media_filepaths:

            print(f"Checking '{media_filepath}'")

            media_type = check_file_type(media_filepath, error_messages_callback=show_error_messages)

            if media_type == "video" and args.force_recognize == True:

                force_recognize_media_file_format = None

                base, ext = os.path.splitext(media_filepath)
                if ext[1:] == "ts":
                    force_recognize_media_file_format = "mp4"
                else:
                    force_recognize_media_file_format = ext[1:]

                #print(f"media_filepath = {media_filepath}")
                subtitle_stream_parser = SubtitleStreamParser()
                subtitle_streams_data = subtitle_stream_parser(media_filepath)
                #print(f"subtitle_streams_data = {subtitle_streams_data}")
                #print(f"subtitle_stream_parser.timed_subtitles_of_index(1) = {subtitle_stream_parser.timed_subtitles_of_index(1)}")

                if subtitle_streams_data and subtitle_stream_parser.timed_subtitles_of_index(1) != []:

                    tmp_subtitle_removed_media_filepath = f"{base}.tmp.subtitles.removed.media_filepath.{force_recognize_media_file_format}"
                    subtitle_removed_media_filepath = f"{base}.force.recognize.{force_recognize_media_file_format}"

                    widgets = ["Removing subtitles streams from file    : ", Percentage(), ' ', Bar(marker="#"), ' ', ETA()]
                    pbar = ProgressBar(widgets=widgets, maxval=100).start()
                    subtitle_remover = MediaSubtitleRemover(output_path=tmp_subtitle_removed_media_filepath, progress_callback=show_progress, error_messages_callback=show_error_messages)
                    tmp_output = subtitle_remover(media_filepath)
                    pbar.finish()

                    if os.path.isfile(tmp_output):
                        shutil.copy(tmp_output, subtitle_removed_media_filepath)
                        os.remove(tmp_output)

                        processed_list.append(subtitle_removed_media_filepath)

                    print(f"Subtitles removed {media_type} file saved as   : '{subtitle_removed_media_filepath}'")

                else:
                    print("Nothing to remove")
                    if (media_filepath not in processed_list) and (media_filepath not in removed_media_filepaths):
                        processed_list.append(media_filepath)

                        #print("removed_media_filepaths = ", removed_media_filepaths)
                        #print("media_filepaths = ", media_filepaths)
                        #print("processed_list = ", processed_list)
                        #print("len(removed_media_filepaths) = ", len(removed_media_filepaths))
                        #print("len(media_filepaths) = ", len(media_filepaths))
                        #print("len(processed_list) = ", len(processed_list))
                        #print("")

            else:
                if media_type == "video":
                    print("force_recognize is false")

                if media_type == "audio":
                    print(f"'{media_filepath}' is audio file, nothing to remove")

                if media_filepath not in processed_list and media_filepath not in removed_media_filepaths:
                    processed_list.append(media_filepath)
                    #print("removed_media_filepaths = ", removed_media_filepaths)
                    #print("media_filepaths = ", media_filepaths)
                    #print("processed_list = ", processed_list)
                    #print("len(removed_media_filepaths) = ", len(removed_media_filepaths))
                    #print("len(media_filepaths) = ", len(media_filepaths))
                    #print("len(processed_list) = ", len(processed_list))
                    #print("")

            print("")


    if args.force_recognize == False and processed_list == []:
        for media_filepath in media_filepaths:
            if media_filepath not in removed_media_filepaths:
                processed_list.append(media_filepath)


    if processed_list:
        # START THE TRANSCRIBE PROCESS
        print("PERFORMING SPEECH RECOGNITION FOR MEDIA FILES THAT HAVE NO SUBTITLES STREAMS OR FORCED TO BE RECOGNIZED")
        print("=======================================================================================================")

        for media_filepath in processed_list:
            print(f"Processing '{media_filepath}'")

            media_type = check_file_type(media_filepath, error_messages_callback=show_error_messages)

            try:
                widgets = ["Converting to a temporary WAV file      : ", Percentage(), ' ', Bar(), ' ', ETA()]
                pbar = ProgressBar(widgets=widgets, maxval=100).start()
                wav_converter = WavConverter(progress_callback=show_progress, error_messages_callback=show_error_messages)
                wav_filepath, sample_rate = wav_converter(media_filepath)
                pbar.finish()

                region_finder = SpeechRegionFinder(frame_width=4096, min_region_size=0.5, max_region_size=6, error_messages_callback=show_error_messages)
                regions = region_finder(wav_filepath)

                if regions == None:
                    print("No speech regions found")
                    sys.exit(1)

                if args.src_language == "auto":
                    segments, info = model.transcribe(wav_filepath)
                    src_language = info.language
                    print(f"Detected language                       : {info.language} (probability = {info.language_probability})")
                    total_duration = int(info.duration * 10) / 10
                    #print("total_duration = ", total_duration)

                    ffmpeg_src_language_code = google_language.ffmpeg_code_of_code[src_language]

                    if src_language in google_unsupported_languages and do_translate:
                        task = "translate"
                        src_language = "en"

                else:
                    segments, info = model.transcribe(wav_filepath, language=src_language, task=task)
                    total_duration = info.duration
                    #print("total_duration = ", total_duration)

                if segments:
                    widgets = ["Performing speech recognition           : ", Percentage(), ' ', Bar(marker='#'), ' ', ETA()]
                    pbar = ProgressBar(widgets=widgets, maxval=100).start()
                    timed_subtitles = []
                    regions = []
                    transcripts = []
                    segment_start = None
                    segment_end = None
                    for segment in segments:
                        segment_start = segment.start
                        if (segment.end>total_duration):
                            segment_end = int(total_duration*10)/10
                        else:
                            segment_end = segment.end

                        progress = int(round(float(segment_end))*100/total_duration)
                        #print("progress = ", progress)
                        #print("info.duration = ", info.duration)
                        #print("(segment_start, segment_end) = ", (segment_start, segment_end))
                        #print("segment.text = ", segment.text)
                        regions.append((segment_start, segment_end))
                        transcripts.append(segment.text)
                        pbar.update(progress)
                    pbar.finish()
                    timed_subtitles = [(r, t) for r, t in zip(regions, transcripts) if t]

                    base, ext = os.path.splitext(media_filepath)
                    src_subtitle_filepath = f"{base}.{src_language}.{subtitle_format}"

                    writer = SubtitleWriter(regions, transcripts, subtitle_format, error_messages_callback=show_error_messages)
                    writer.write(src_subtitle_filepath)

                    if do_translate == True:
                        timed_subtitles = writer.timed_subtitles
                        created_regions = []
                        created_subtitles = []
                        for entry in timed_subtitles:
                            created_regions.append(entry[0])
                            created_subtitles.append(entry[1])

                        prompt = "Translating from %s to %s   : " %(src_language.center(8), dst_language.center(8))
                        widgets = [prompt, Percentage(), ' ', Bar(marker='#'), ' ', ETA()]
                        pbar = ProgressBar(widgets=widgets, maxval=len(timed_subtitles)).start()

                        transcript_translator = SentenceTranslator(src=src_language, dst=dst_language, error_messages_callback=show_error_messages)

                        translated_subtitles = []
                        for i, translated_subtitle in enumerate(pool.imap(transcript_translator, created_subtitles)):
                            translated_subtitles.append(translated_subtitle)
                            pbar.update(i)
                        pbar.finish()

                        base, ext = os.path.splitext(media_filepath)
                        dst_subtitle_filepath = f"{base}.{dst_language}.{subtitle_format}"
                        translation_writer = SubtitleWriter(created_regions, translated_subtitles, subtitle_format, error_messages_callback=show_error_messages)
                        translation_writer.write(dst_subtitle_filepath)

                        print(f"Original subtitles file saved as        : '{src_subtitle_filepath}'")
                        print(f"Translated subtitles file saved as      : '{dst_subtitle_filepath}'")

                        if media_type == "audio":
                            completed_tasks += 1
                            #print(f"\nmedia_filepath = {media_filepath}, do_translate == True, media_type == 'audio' : completed_tasks = {completed_tasks}\n")

                        elif media_type == "video" and args.embed_src == False and args.embed_dst == False:
                            completed_tasks += 1
                            #print(f"\nmedia_filepath = {media_filepath}, do_translate == True, media_type == 'video', args.embed_src == False and args.embed_dst == False : completed_tasks = {completed_tasks}\n")

                    elif do_translate == False:
                        print(f"Subtitles file saved as                 : '{src_subtitle_filepath}'")

                        if media_type == "audio":
                            completed_tasks += 1
                            #print(f"\nmedia_filepath = {media_filepath}, do_translate == False, media_type == 'audio' : completed_tasks = {completed_tasks}\n")

                        elif media_type == "video" and args.embed_src == False:
                            completed_tasks += 1
                            #print(f"\nmedia_filepath = {media_filepath}, do_translate == False, media_type == 'video', args.embed_src == False : completed_tasks = {completed_tasks}\n")


                    # EMBEDDING SUBTITLES FILE

                    embedded_media_filepath = None

                    if do_translate == False:

                        media_type = check_file_type(media_filepath, error_messages_callback=show_error_messages)

                        if media_type == "audio" and args.embed_src == True:
                            print("Subtitles can only be embedded into video file, not audio file")

                        if media_type == "video" and args.embed_src == True:

                            ffmpeg_src_language_code = google_language.ffmpeg_code_of_code[src_language]

                            base, ext = os.path.splitext(media_filepath)

                            if ext[1:] == "ts":
                                media_format = "mp4"
                            else:
                                media_format = ext[1:]

                            src_tmp_embedded_media_filepath = f"{base}.{ffmpeg_src_language_code}.tmp.embedded.{media_format}"
                            embedded_media_filepath = f"{base}.{ffmpeg_src_language_code}.embedded.{media_format}"

                            widgets = [f"Embedding '{ffmpeg_src_language_code}' subtitles into {media_type}    : ", Percentage(), ' ', Bar(marker="#"), ' ', ETA()]
                            pbar = ProgressBar(widgets=widgets, maxval=100).start()
                            subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=src_subtitle_filepath, language=ffmpeg_src_language_code, output_path=src_tmp_embedded_media_filepath, progress_callback=show_progress, error_messages_callback=show_error_messages)
                            src_tmp_output = subtitle_embedder(media_filepath)
                            pbar.finish()

                            if os.path.isfile(src_tmp_output):
                                shutil.copy(src_tmp_output, embedded_media_filepath)
                                os.remove(src_tmp_output)
                                print(f"Subtitles embedded {media_type} file saved as  : '{embedded_media_filepath}'")
                                completed_tasks += 1
                                #print(f"\ndo_translate == False, media_type == 'video', args.embed_src == True: completed_tasks = {completed_tasks}\n")


                    elif do_translate == True:

                        media_type = check_file_type(media_filepath, error_messages_callback=show_error_messages)

                        if media_type == "audio" and (args.embed_src == True or args.embed_src == True):
                            print("Subtitles can only be embedded into video file, not audio file")

                        if media_type == "video" and args.embed_src == True and args.embed_dst == True:

                            ffmpeg_src_language_code = google_language.ffmpeg_code_of_code[src_language]
                            ffmpeg_dst_language_code = google_language.ffmpeg_code_of_code[dst_language]

                            base, ext = os.path.splitext(media_filepath)

                            if ext[1:] == "ts":
                                media_format = "mp4"
                            else:
                                media_format = ext[1:]

                            src_tmp_embedded_media_filepath = f"{base}.{ffmpeg_src_language_code}.tmp.embedded.{media_format}"
                            src_dst_tmp_embedded_media_filepath = f"{base}.{ffmpeg_src_language_code}.{ffmpeg_dst_language_code}.tmp.embedded.{media_format}"
                            embedded_media_filepath = f"{base}.{ffmpeg_src_language_code}.{ffmpeg_dst_language_code}.embedded.{media_format}"

                            widgets = [f"Embedding '{ffmpeg_src_language_code}' subtitles into {media_type}    : ", Percentage(), ' ', Bar(marker="#"), ' ', ETA()]
                            pbar = ProgressBar(widgets=widgets, maxval=100).start()
                            subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=src_subtitle_filepath, language=ffmpeg_src_language_code, output_path=src_tmp_embedded_media_filepath, progress_callback=show_progress, error_messages_callback=show_error_messages)
                            src_tmp_output = subtitle_embedder(media_filepath)
                            pbar.finish()

                            if os.path.isfile(src_tmp_output) and os.path.isfile(dst_subtitle_filepath):
                                widgets = [f"Embedding '{ffmpeg_dst_language_code}' subtitles into {media_type}    : ", Percentage(), ' ', Bar(marker="#"), ' ', ETA()]
                                pbar = ProgressBar(widgets=widgets, maxval=100).start()
                                subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=dst_subtitle_filepath, language=ffmpeg_dst_language_code, output_path=src_dst_tmp_embedded_media_filepath, progress_callback=show_progress, error_messages_callback=show_error_messages)
                                src_dst_tmp_output = subtitle_embedder(src_tmp_output)
                                pbar.finish()

                            if os.path.isfile(src_dst_tmp_output):
                                shutil.copy(src_dst_tmp_output, embedded_media_filepath)
                                print(f"Subtitles embedded {media_type} file saved as  : '{embedded_media_filepath}'")
                                completed_tasks += 1
                                #print(f"\ndo_translate == True, media_type == 'video', args.embed_src == True and args.embed_dst == True : completed_tasks = {completed_tasks}\n")

                            else:
                                print("Unknown error!")

                            if os.path.isfile(src_dst_tmp_output):
                                os.remove(src_dst_tmp_output)
                            if os.path.isfile(src_tmp_output):
                                os.remove(src_tmp_output)

                        elif media_type == "video" and args.embed_src == True and args.embed_dst == False:

                            ffmpeg_src_language_code = google_language.ffmpeg_code_of_code[src_language]

                            base, ext = os.path.splitext(media_filepath)

                            if ext[1:] == "ts":
                                media_format = "mp4"
                            else:
                                media_format = ext[1:]

                            src_tmp_embedded_media_filepath = f"{base}.{ffmpeg_src_language_code}.tmp.embedded.{media_format}"
                            embedded_media_filepath = f"{base}.{ffmpeg_src_language_code}.embedded.{media_format}"

                            widgets = [f"Embedding '{ffmpeg_src_language_code}' subtitles into {media_type}    : ", Percentage(), ' ', Bar(marker="#"), ' ', ETA()]
                            pbar = ProgressBar(widgets=widgets, maxval=100).start()
                            subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=src_subtitle_filepath, language=ffmpeg_src_language_code, output_path=src_tmp_embedded_media_filepath, progress_callback=show_progress, error_messages_callback=show_error_messages)
                            src_tmp_output = subtitle_embedder(media_filepath)
                            pbar.finish()

                            if os.path.isfile(src_tmp_output):
                                shutil.copy(src_tmp_output, embedded_media_filepath)
                                os.remove(src_tmp_embedded_media_filepath)
                                print(f"Subtitles embedded {media_type} file saved as  : '{embedded_media_filepath}'")
                                completed_tasks += 1
                                #print(f"\ndo_translate == True, media_type == 'video', args.embed_src == True and args.embed_dst == False : completed_tasks = {completed_tasks}\n")

                            else:
                                print("Unknown error!")

                        elif media_type == "video" and args.embed_src == False and args.embed_dst == True:

                            ffmpeg_dst_language_code = google_language.ffmpeg_code_of_code[dst_language]

                            base, ext = os.path.splitext(media_filepath)

                            if ext[1:] == "ts":
                                media_format = "mp4"
                            else:
                                media_format = ext[1:]

                            dst_tmp_embedded_media_filepath = f"{base}.{ffmpeg_dst_language_code}.tmp.embedded.{media_format}"
                            embedded_media_filepath = f"{base}.{ffmpeg_dst_language_code}.embedded.{media_format}"

                            widgets = [f"Embedding '{ffmpeg_dst_language_code}' subtitles into {media_type}    : ", Percentage(), ' ', Bar(marker="#"), ' ', ETA()]
                            pbar = ProgressBar(widgets=widgets, maxval=100).start()
                            subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=dst_subtitle_filepath, language=ffmpeg_dst_language_code, output_path=dst_tmp_embedded_media_filepath, progress_callback=show_progress, error_messages_callback=show_error_messages)
                            dst_tmp_output = subtitle_embedder(media_filepath)
                            pbar.finish()

                            if os.path.isfile(dst_tmp_output):
                                shutil.copy(dst_tmp_output, embedded_media_filepath)
                                os.remove(dst_tmp_output)
                                print(f"Subtitles embedded {media_type} file saved as  : '{embedded_media_filepath}'")
                                completed_tasks += 1
                                #print(f"\ndo_translate == True, media_type == 'video', args.embed_src == False and args.embed_dst == True : completed_tasks = {completed_tasks}\n")

                            else:
                                print("Unknown error!")

                print("")

            except KeyboardInterrupt:
                pbar.finish()
                pool.terminate()
                pool.close()
                pool.join()
                print("Cancelling all tasks")

                if sys.platform == "win32":
                    stop_ffmpeg_windows(error_messages_callback=show_error_messages)
                else:
                    stop_ffmpeg_linux(error_messages_callback=show_error_messages)

                remove_temp_files("wav")
                return 1

            except Exception as e:
                if not KeyboardInterrupt in str(e):
                    pbar.finish()
                    pool.terminate()
                    pool.close()
                    pool.join()
                    print(e)

                    if sys.platform == "win32":
                        stop_ffmpeg_windows(error_messages_callback=show_error_messages)
                    else:
                        stop_ffmpeg_linux(error_messages_callback=show_error_messages)

                    remove_temp_files("wav")
                    return 1

    #print(f"len(media_filepaths) = {len(media_filepaths)}")
    #print(f"len(processed_list) = {len(processed_list)}")
    #print(f"completed_tasks = {completed_tasks}")

    if len(media_filepaths)>0 and len(processed_list)>0 and completed_tasks == len(media_filepaths) + len(processed_list):
        transcribe_end_time = time.time()
        transcribe_elapsed_time = transcribe_end_time - transcribe_start_time
        transcribe_elapsed_time_seconds = timedelta(seconds=int(transcribe_elapsed_time))
        transcribe_elapsed_time_str = str(transcribe_elapsed_time_seconds)
        hour, minute, second = transcribe_elapsed_time_str.split(":")
        msg = "Total running time                      : %s:%s:%s" %(hour.zfill(2), minute, second)
        print(msg)
    elif len(media_filepaths)>0 and completed_tasks == len(media_filepaths):
        transcribe_end_time = time.time()
        transcribe_elapsed_time = transcribe_end_time - transcribe_start_time
        transcribe_elapsed_time_seconds = timedelta(seconds=int(transcribe_elapsed_time))
        transcribe_elapsed_time_str = str(transcribe_elapsed_time_seconds)
        hour, minute, second = transcribe_elapsed_time_str.split(":")
        msg = "Total running time                      : %s:%s:%s" %(hour.zfill(2), minute, second)
        print(msg)


    if pool:
        pool.close()
        pool.join()
        pool = None

    if sys.platform == "win32":
        stop_ffmpeg_windows(error_messages_callback=show_error_messages)
    else:
        stop_ffmpeg_linux(error_messages_callback=show_error_messages)

    remove_temp_files("wav")


if __name__ == '__main__':
    multiprocessing.freeze_support()
    sys.exit(main())
