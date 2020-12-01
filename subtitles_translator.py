import sys
import os.path
from google_trans_new import google_translator

if len(sys.argv) != 3:
    sys.exit("Wrong number of arguments! Check out readme.md for proper usage.")

if not os.path.isfile(sys.argv[2]):
    sys.exit("Provided file does not exist!")

index_of_dot = sys.argv[2].rfind('.')
file_extension = sys.argv[2][index_of_dot:]

r = open(sys.argv[2], 'r', encoding='utf-8')
w = open(sys.argv[2].replace(file_extension, '_' + sys.argv[1] + file_extension), 'w', encoding='utf-8')
translator = google_translator()

for line in r:
    print(repr(line))
    if line not in ["\n", ""]:
        line += translator.translate(line, lang_tgt=sys.argv[1]) + '\n'

    w.write(line)
