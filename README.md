# Scripts:

* [Subtitles translator](#subtitles-translator)
* [Presentations translator](#presentations-translator)

___

# subtitles-translator

Script [subtitles_translator.py](##subtitles_traslator.py) translates .srt subtitles and puts it onto new file.

The easiest way to use it is to put both script and subtitles into the same folder.
Then from cmd you can run them like so:

`python subtitles_translator.py <dest_lang> <file_name>`

For example:

`python subtitles_translator.py en test.srt`

will create `test_en.srt` file with translated subtitles.

___

# presentations-translator

NOTE: It only works for .md presentations.

I may not have included all html/markdown tags, so let me know about any issues you encounter :)
So far whitespace characters can be messed up so you have to manually add new lines (I'll update it when I have time).

---

## [`md_translator.py`](https://github.com/MrMijagi/work-translators/blob/master/md_translator.py)

This script takes 3 arguments: destination language, source filename and output filename like so:

`python md_translator.py <dest_lang> <input_filename> <output_filename>`

So let's say you have `polish.md` presentation and want to translate it and put into `english.md` file.

`python md_translator.py en polish.md english.md`

___

Here is the link for all language abbreviations: https://github.com/lushan88a/google_trans_new/blob/main/constant.py
