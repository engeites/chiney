from googletrans import Translator


def translate(text):
    translator = Translator()
    return translator.translate(text, src='zh-cn', dest='ru').text
