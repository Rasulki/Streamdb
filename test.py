from googletrans import Translator
import googletrans

def translate_message(message):
    translator = Translator()
    translation = translator.translate(message, dest='ru')
    return translation.text


message = "Hello, how are you?"
translated_message = translate_message(message)
if translated_message:
    print(translated_message)
else:
    print("Translation failed. Please try again later.")
