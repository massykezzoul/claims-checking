from googletrans import Translator 

trans = Translator()

t = trans.translate( ' Bonjour tout le monde ')

print(f'Source: {t.src}')
print(f'Destination: {t.dest}')
print(f'{t.origin} -> {t.text}')

