import sys
from googletrans import Translator

r = open(sys.argv[1], 'r', encoding='utf-8')
w = open(sys.argv[1].replace('.sbv', '_en.sbv'), 'w', encoding='utf-8')
translator = Translator(service_urls=['translate.google.com'])

for line in r:
    if line == "\n":
        w.write(line)
    else:
        line += translator.translate(line, src='pl', dest='en').text + '\n'
        w.write(line)
    #print(line)
