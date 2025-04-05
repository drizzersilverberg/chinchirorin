from locales import lang
import os

def get_lang(locale, string, replacer={}):
    if locale in lang.keys() and string in lang[locale].keys():
        text = lang[locale][string]

        if bool(replacer):
            for key in replacer.keys():
                text = text.replace(key, str(replacer[key]))

        return text

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')