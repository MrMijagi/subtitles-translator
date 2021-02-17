import sys
import os.path
from google_trans_new import google_translator

translator = google_translator()


# returns the closest position to one of the characters from list
def find_closest(line, chars):
    min_position = -1

    for char in chars:
        tmp = line.find(char)
        if tmp != -1 and tmp < min_position:
            min_position = tmp

    return min_position


# returns scaled position of character (which must be space)
#     I like eating strawberries in summer.
#                        +----->
#     scaled position -> |      | <- first space after the word
def get_position(sentence, ratio):
    position = int(ratio * len(sentence))

    while sentence[position] != ' ':
        position += 1

    return position


# This class takes each line of .srt file and returns True if the line contains transcription
# or False if the line contains timecode or other metadata
class SRTFilter:
    def __init__(self):
        self.counter = 1
        self.header = True

    def feed_filter(self, line):
        if self.header:
            if str(self.counter) == line:
                self.counter += 1
            else:
                self.header = False
        else:
            if line == '':
                self.header = True
            else:
                return True

        return False


# This class holds one line of transcription. It manages list of Sentences (class below).
class Subtitle:
    def __init__(self, line, sentence=None, sentence_index=0):
        self.line = line
        self.sentences = [[Sentence(), 0] if sentence is None else [sentence, sentence_index]]
        self.create_sentences()

    def create_sentences(self):
        position = find_closest(self.line, '.?!')

        while position != -1:
            if position + 1 == len(self.line):
                self.sentences[-1][0].add_to_sentence(self.line)
                self.line = ''
            else:
                self.sentences[-1][0].add_to_sentence(self.line[:position + 1])
                self.sentences.append([Sentence(), 0])
                self.line = self.line[position + 1:]

            position = find_closest(self.line, '.?!')

        self.sentences[-1][0].add_to_sentence(self.line)
        self.line = ''

    def get_last_sentence(self):
        return self.sentences[-1]

    def is_last_closed(self):
        return self.sentences[-1][0].closed

    def __str__(self):
        return (''.join([sentence[0].translated_parts[sentence[1]] for sentence in self.sentences]) + '\n').lstrip()


# This class holds pieces of sentences across lines of transcription.
# For example with this .srt file:
# 1
# 00:00:10,450 --> 00:00:12,550
# I like
#
# 2
# 00:00:13,330 --> 00:00:15,760
# eating strawberries
#
# 3
# 00:00:16,720 --> 00:00:20,990
# at midnight. Are
# strawberries red?
#
# There are 4 Subtitle objects that hold 4 lines of transcription
# and there are two Sentence objects that hold both sentences:
#  - I like | eating strawberries | at midnight.
#  - Are | strawberries red?
# Then both sentences get translated and divided into pieces so the length of each piece matches the original.
# Subtitle objects remember which piece of each sentence it holds and then puts it up together in str() function.
class Sentence:
    def __init__(self, sentence=''):
        self.sentence = sentence
        self.markers = []
        self.marker_ratios = []
        self.closed = False
        self.translated = ''
        self.translated_parts = []

    def add_to_sentence(self, part):
        self.sentence += part
        if self.has_ending():
            self.closed = True
            self.marker_ratios = [marker / len(self.sentence) for marker in self.markers]
            self.translated = translator.translate(self.sentence, lang_tgt=sys.argv[1])
            self.create_parts()
        else:
            self.markers.append(len(self.sentence))

    def has_ending(self):
        return self.sentence[len(self.sentence) - 2] in '.?!' or self.sentence[len(self.sentence) - 1] in '.?!'

    def create_parts(self):
        self.markers = [0]

        for marker_ratio in self.marker_ratios:
            self.markers.append(get_position(self.translated, marker_ratio))

        for i in range(len(self.markers) - 1):
            start_position = self.markers[i]
            end_position = self.markers[i + 1]
            self.translated_parts.append(self.translated[start_position:end_position])

        start_position = self.markers[len(self.markers) - 1]
        end_position = len(self.translated)
        self.translated_parts.append(self.translated[start_position:end_position])


def main():
    if not os.path.isfile(sys.argv[2]):
        sys.exit("Provided file does not exist!")

    index_of_dot = sys.argv[2].rfind('.')
    file_extension = sys.argv[2][index_of_dot:]

    r = open(sys.argv[2], 'r', encoding='utf-8')
    w = open(sys.argv[2].replace(file_extension, '_' + sys.argv[1] + file_extension), 'w', encoding='utf-8')

    subtitles = []
    last_sentence = Sentence()
    last_index = 0
    srt_filter = SRTFilter()

    for line in r:
        # print(repr(line))
        if srt_filter.feed_filter(line.rstrip()):
            subtitles.append(Subtitle(line.replace('\n', ' '), last_sentence, last_index))

            if subtitles[-1].is_last_closed():
                last_sentence = Sentence()
                last_index = 0
            else:
                last_sentence, last_index = subtitles[-1].get_last_sentence()
                last_index += 1

    r = open(sys.argv[2], 'r', encoding='utf-8')
    srt_filter = SRTFilter()

    for line in r:
        # print(repr(line))
        if srt_filter.feed_filter(line.rstrip()):
            w.write(str(subtitles.pop(0)))
        else:
            w.write(line)


if __name__ == "__main__":
    main()
