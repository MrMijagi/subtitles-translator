# Scripts:

* [Subtitles translator](#subtitles-translator)
* [Presentations translator](#presentations-translator)

___

# subtitles-translator

There are two python scripts:
* [subtitles_compressor.py](##subtitles_compressor.py)
* [subtitles_translator.py](##subtitles_translator.py)

The easiest way to use it is to put both script and subtitles into the same folder.
Then from cmd you can run them like so:

`python subtitles_compressor.py <file_name>`

or

`python subtitles_translator.py <file_name>`

Scripts will generate new file so don't worry about the original one :)

Also I've tested them only on .sbv files, but .srt should work as well. If there are problems let me know and I'll fix it.

---

## [`subtitles_compressor.py`](https://github.com/MrMijagi/work-translators/blob/master/subtitles_compress.py)

Since sentences are divided into fragments, first script connects them together and separates sentences from each other.

So for example from this .sbv subtitle:

```
0:00:10.068,0:00:12.637
Przejdźmy sobie do tych
kontenerów sekwencyjnych.

0:00:12.937,0:00:16.247
Wektor - to jest też taka tablica, tylko
mówimy, że ona jest już dynamiczna,

0:00:16.272,0:00:17.715
ponieważ może się rozszerzać.
```

You will get this output in other new file:

```
Przejdźmy sobie do tych kontenerów sekwencyjnych. 

Wektor - to jest też taka tablica, tylko mówimy, że ona jest już dynamiczna, ponieważ może się rozszerzać. 
```

Now you can make some corrections as well since program treats any dot '.' as the end of sentence (which isn't always the case).

---

## [`subtitles_translator.py`](https://github.com/MrMijagi/work-translators/blob/master/subtitles_translator.py)

The only thing left is to translate sentences. After using file generated above, you will get this output:

```
Przejdźmy sobie do tych kontenerów sekwencyjnych. 
Let's move on to these sequence containers.

Wektor - to jest też taka tablica, tylko mówimy, że ona jest już dynamiczna, ponieważ może się rozszerzać. 
Vector - this is also an array, but we say that it is dynamic because it can expand.
```

Next to original sentence you have the translated version, so you can correct it.
After that you can copy/paste fragments of translated sentences directly into subtitles :)

___

# presentations-translator

NOTE: It only works for .md presentations.

I may not have included all html/markdown tags, so let me know about any issues you encounter :)

---

## [`md_translator.py`](https://github.com/MrMijagi/work-translators/blob/master/md_translator.py)

This script takes 3 arguments: destination language (only 'pl' or 'en'), source filename and output filename like so:

`python md_translator.py [pl|en] <input_filename> <output_filename>`

So let's say you have `polish.md` presentation and want to translate it and put into `english.md` file.

`python md_translator.py en polish.md english.md`



