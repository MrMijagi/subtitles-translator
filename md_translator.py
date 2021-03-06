# General idea of translating is simple:
# We want to translate everything except html and markdown tags.
# In case like tag <code> (or ``` in markdown) we usually want to keep the original text,
# and in others (like <div>) we want to translate the text inside.
# Script reads the entire text to translate and starts searching for the first tag that appears.
# Then it determines if he should translate the text inside or not.
# If he has to translate the text it's important to keep in mind that inside content of this tag
# there can be another one nested inside (that's why I used recursion).
# All translated text goes into output variable and gets saved into file at the end.

import sys
from google_trans_new import google_translator

tags_with_inside = [["<span", "</span>"],
                    ["<a", "</a>"],
                    ["**", "**"],
                    ["[", "]"],
                    ["<div", "</div>"],
                    ["<pre", "</pre>"]]
tags_to_ignore = [["<img", ">"],
                  ["<image", ">"],
                  ["```", "```"],
                  ["`", "`", ],
                  ["<!--", "-->"],
                  ["<code", "</code>"]]

tags = tags_to_ignore + tags_with_inside

translator = google_translator()


# this method should definitely be optimized but for now it's enough
def find_first_tag(line):
    min_index = len(line) + 1
    found_tag = ["", ""]
    for tag in tags:
        tmp = line.find(tag[0])
        if tmp != -1 and tmp < min_index:
            min_index = tmp
            found_tag = tag

    return found_tag


def translate_clear_text(text):
    if text == "":
        return text
    else:
        return translator.translate(text, lang_tgt=sys.argv[1]).strip()


# removes whitespace characters from start and end of the string
def translate_unstripped_test(text):
    all_len = len(text)
    left_len = len(text) - len(text.lstrip())
    right_len = len(text) - len(text.rstrip())

    if all_len == left_len:  # the entire string is whitespaces
        return text
    else:
        return text[:left_len] \
                      + translate_clear_text(text[left_len:all_len - right_len]) \
                      + text[all_len - right_len:]


# Since the translator 'eats' new line, I have to save them
def translate_text(text):
    translated = ''

    while len(text) > 0:
        index = text.find('\n')

        if index != -1:
            text_to_translate = text[:index]
            text = text[index + 1:]

            translated += translate_unstripped_test(text_to_translate)
            translated += '\n'
        else:
            translated += translate_unstripped_test(text)
            text = ''

    return translated


def filter_text(input_text):
    output = ""

    while len(input_text) > 0:
        tag = find_first_tag(input_text)

        if tag[0] != "":  # tag was found
            if tag in tags_to_ignore:  # skip the inside, translate the rest
                # pass text before tag and tag itself to output
                # text before |<a| PARAMETERS>text inside</span> text after
                #      fst    snd            input_text
                fst, snd, input_text = input_text.partition(tag[0])
                output += translate_text(fst) + snd

                # pass text before closing tag and closing tag itself to output
                # text before <a| PARAMETERS>text inside|</span>| text after
                #                          fst             snd    input_text
                fst, snd, input_text = input_text.partition(tag[1])
                output += fst + snd
            else:  # tag in tags_with_inside: pass text inside of tag to filter , translate the rest
                # pass text before tag and tag itself (without parameters) to output
                # text before |<a| PARAMETERS>text inside</span> text after
                #      fst    snd            input_text
                fst, snd, input_text = input_text.partition(tag[0])
                output += translate_text(fst) + snd

                # pass text before closing tag and closing tag itself to output
                # text before <a| PARAMETERS>text inside|</span>| text after
                #                          fst             snd    input_text
                # NOTE: here we have to separate "PARAMETERS>" from "text inside"
                # so it doesn't get translated. So far only html tags have them so we only check for "<"
                fst, snd, input_text = input_text.partition(tag[1])
                if tag[0][0] == "<":
                    a, b, fst = fst.partition(">")
                    # text before <span| PARAMETERS|>|text inside|</span>| text after
                    #                         a     b     fst       snd    input_text
                    output += a + b + filter_text(fst) + snd
                else:
                    # tags without parameters
                    # text before `|text inside|`| text after
                    #                   fst    snd input_text
                    output += filter_text(fst) + snd
        else:  # no tags, translate the rest
            output += translate_text(input_text)
            input_text = ""

    return output


def main():

    if len(sys.argv) != 4:
        sys.exit("Wrong number of arguments! Check readme.md for proper usage.")

    # check second argument, open input file
    try:
        r = open(sys.argv[2], 'r', encoding='utf-8')
    except IOError:
        sys.exit("Something went wrong with opening " + sys.argv[2] + " file.")

    # output file
    try:
        w = open(sys.argv[3], 'w', encoding='utf-8')
    except IOError:
        sys.exit("Something went wrong with opening " + sys.argv[3] + " file.")

    # translate text
    output = filter_text(r.read())

    # after line is translated add it to output file
    w.write(output)

    # close files
    r.close()
    w.close()


if __name__ == "__main__":
    main()
