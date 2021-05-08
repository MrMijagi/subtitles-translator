# Scripts:

* [Subtitles translator](#subtitles-translator)
* [Markdown translator](#markdown-translator)

___

# subtitles-translator

The script below translates .srt subtitles to any language specified. What is important is that it doesn't translate text line by line. Instead, it concatenates all text and groups it into sentences so that the translation is more accurate. After that, it tries to divide the translated text into lines with the same length as before.

---

## [`subtitles_translator.py`](https://github.com/MrMijagi/work-translators/blob/master/subtitles_translator.py)

The easiest way to use it is to put both script and subtitles into the same folder.
Then from cmd you can run them like so:

`python subtitles_translator.py <dest_lang> <file_name>`

For example:

`python subtitles_translator.py en test.srt`

will create `test_en.srt` file with translated subtitles.

___

# markdown-translator

The script below translates markdown document while ignoring things that shouldn't be translated (for example tags with code inside them).

I may not have included all html/markdown tags, so let me know about any issues you encounter :) (you can also just put missing tags inside the python script yourself)

---

## [`md_translator.py`](https://github.com/MrMijagi/work-translators/blob/master/md_translator.py)

This script takes 3 arguments: destination language, source filename and output filename like so:

`python md_translator.py <dest_lang> <input_filename> <output_filename>`

So let's say you have `polish.md` presentation and want to translate it and put into `english.md` file.

`python md_translator.py en polish.md english.md`

___

Here is the link for all language abbreviations: https://github.com/lushan88a/google_trans_new/blob/main/constant.py
