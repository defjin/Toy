from googletrans import Translator
translator = Translator()
translation = translator.translate('the friends of mine', dest='ko')
print(translation.text)