from make_zhuyin_jyutping_nospaces import *

for dictfile in list_dictionaries():
  for word,pinyin in get_word_and_pinyin_in_dictionary(dictfile + '.dict.yaml'):
    #if '#' in word:
    #  print(dictfile)
    pinyin = pinyin.strip()
    #print(pinyin)
    if pinyin in 'm m0 m1 m2 m3 m4 m5'.split(' '):
      print(word)
      print(pinyin)
      print(dictfile)
