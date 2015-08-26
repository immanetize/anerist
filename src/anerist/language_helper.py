from pkgdb2client import PkgDB
import git
import hashlib
import os
import shutil
import errno
import sys

class PublicanHelpers():
    def valid_langs(self):
        language_list = [
            "ar-sa",
            "as-in",
            "ast-es",
            "bn-in",
            "bs-ba",
            "bg-bg",
            "ca-es",
            "zh-cn",
            "zh-hk",
            "zh-tw",
            "cs-CZ",
            "da-DK",
            "fi-FI",
            "fr-FR",
            "de-DE",
            "el-GR",
            "gu-IN",
            "he-IL",
            "hi-IN",
            "hr-HR",
            "hu-HU",
            "id-ID",
            "ia",
            "is-IS",
            "it-IT",
            "ja-JP",
            "kn-IN",
            "ko-KR",
            "lv-LT",
            "lv-LV",
            "ml-IN",
            "mr-IN",
            "nb-NO",
            "nl-NL",
            "or-IN",
            "pa-IN",
            "fa-IR",
            "pl-PL",
            "pt-PT",
            "pt-BR",
            "ro-RO",
            "ru-RU",
            "sr-RS",
            "sr-Latn-RS",
            "si-LK",
            "sk-SK",
            "es-ES",
            "sv-SE",
            "ta-IN",
            "te-IN",
            "uk-UA",
            "de-CH",
            "th-TH"
            ]
        return language_list

