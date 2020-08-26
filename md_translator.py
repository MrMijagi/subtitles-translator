import sys
from googletrans import Translator

tags_with_inside = [["<span", "</span>"],
                    ["<a", "</a>"],
                    ["**", "**"],
                    ["[", "]"]]
tags_to_ignore = [["<img", ">"],
                  ["<image", ">"],
                  ["```", "```"],
                  ["`", "`", ]
                  ["<!--", "-->"]]

tags = [tags_to_ignore, tags_with_inside]
print("All tags:" + str(tags))

translator = Translator(service_urls=['translate.google.com'])


def find_first_tag(line):
    min_index = -1
    found_tag = ["", ""]
    for tag in tags:
        tmp = line.find(tag[0])
        if tmp != -1:
            min_index = tmp if tmp < min_index else min_index
            found_tag = tag

    return found_tag


def translate_text(text):
    if sys.argv[1] == "en":
        return translator.translate(text, src='pl', dest='en').text
    else:
        return translator.translate(text, src='en', dest='pl').text


def filter_text(input_text):
    output = ""
    while len(input_text) > 0:
        tag = find_first_tag(input_text)
        print("Found tag: " + str(tag))
        if tag[0] != "":  # tag was found
            if tag in tags_to_ignore:  # skip the inside, translate the rest
                fst, snd, input_text = input_text.partition(tag[0])
                output += translate_text(fst) + snd
                fst, snd, input_text = input_text.partition(tag[1])
                output += fst + snd
            else:  # pass inside of tag to filter (and translate), translate the rest
                fst, snd, input_text = input_text.partition(tag[0])
                output += translate_text(fst) + snd
                fst, snd, input_text = input_text.partition(tag[1])
                if tag[0][0] == "<":  # make sure we don't translate <span THOSE PARAMETERS>text to pass to filter</span
                    _, _, fst = fst.partition(">")  # take only the text after ">" symbol   ^^^^^^^^^^^^^^^^^^^^^^
                output += filter_text(fst) + snd
        else:  # no tag, translate the rest
            output += translate_text(input_text)
            input_text = ""

    return output


def main():

    # check first argument
    if sys.argv[1] != "pl" and sys.argv[1] != "en":
        sys.exit("First argument is incorrect! (must be 'pl' or 'en').")

    # check second argument, open input file
    try:
        r = open(sys.argv[2], 'r', encoding='utf-8')
    except IOError:
        sys.exit("Something went wrong with opening " + sys.argv[2] + " file.")

    # output file
    if sys.argv[1] == "en":
        w = open(sys.argv[2].replace('.pl.md', '.en.md'), 'w', encoding='utf-8')
    else:
        w = open(sys.argv[2].replace('.en.md', '.pl.md'), 'w', encoding='utf-8')

    # translate text
    output = filter_text(r.read())

    # after line is translated add it to output file
    w.write(output)
    #print(output)

    # close files
    r.close()
    w.close()


if __name__=="__main__":
    main()