import sys

r = open(sys.argv[1], 'r', encoding='utf-8')
w = open(sys.argv[1].replace('.sbv', '_compressed.sbv'), 'w', encoding='utf-8')

sentence = ""
for line in r:
    if line[0] != '0' and len(line) > 1:
        sentence += line.replace('\n', ' ')
        #print(repr(sentence))

        if sentence[len(sentence)-2] == '.':
            sentence += '\n\n'
            w.write(sentence)
            sentence = ''
        #print(line)