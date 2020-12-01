import sys
import os.path

if len(sys.argv) != 2:
    sys.exit("Wrong number of arguments! Check out readme.md for proper usage.")

if not os.path.isfile(sys.argv[1]):
    sys.exit("Provided file does not exist!")

index_of_dot = sys.argv[1].rfind('.')
file_extension = sys.argv[1][index_of_dot:]

r = open(sys.argv[1], 'r', encoding='utf-8')
w = open(sys.argv[1].replace(file_extension, '_compressed' + file_extension), 'w', encoding='utf-8')

sentence = ""
for line in r:
    # print(repr(line))
    if line[0] != '0' and len(line) > 1:
        sentence += line.replace('\n', ' ')

        if sentence[len(sentence)-2] == '.' or sentence[len(sentence)-1] == '.':
            sentence += '\n\n'
            w.write(sentence)
            sentence = ''
