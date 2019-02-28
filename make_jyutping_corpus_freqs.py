import sys
from collections import Counter

import json
from memoize import memoize
import pinyin
import jyutping
import pycantonese
corpus = pycantonese.hkcancor()
#from hanziconv import HanziConv
from opencc import OpenCC
s2hk = OpenCC('s2hk').convert

from mkdict import pinyin_to_zhuyin_real as pinyin_to_zhuyin
from mkdict import get_all_yue, get_merged_entries

def get_contents_in_dictionary(dictfile):
  lines = open(dictfile).readlines()
  output = []
  is_started = False
  for line in lines:
    x = line.strip()
    if x == '...':
      is_started = True
      continue
    if not is_started:
      continue
    output.append(line)
  return output

def get_word_and_pinyin_in_dictionary(dictfile):
  output = []
  for line in get_contents_in_dictionary(dictfile):
    if '\t' not in line:
      continue
    output.append(line.split('\t')[:2])
  return output

def list_dictionaries():
  dictionaries = '''
  - terra_pinyin
  - terra_pinyin.extra_hanzi
  - luna_pinyin.sgmain
  - luna_pinyin.sgplus
  - luna_pinyin.sgplus2
  - luna_pinyin.chat
  - luna_pinyin.net
  - luna_pinyin.user
  - luna_pinyin.website
  - luna_pinyin.poetry
  - luna_pinyin.computer
  - luna_pinyin.place
  - luna_pinyin.shopping
  '''
  dictionaries = dictionaries.split('-')
  dictionaries = [x.strip() for x in dictionaries]
  dictionaries = [x for x in dictionaries if x != '']
  return dictionaries

def get_word_list():
  output = []
  output_set = set()
  dictionaries = list_dictionaries()
  dictionaries.append('leimaau_jyutping')
  for dictionary_name in dictionaries:
    dictfile = dictionary_name + '.dict.yaml'
    for item in get_word_and_pinyin_in_dictionary(dictfile):
      word = item[0]
      if word not in output_set:
        output_set.add(word)
        output.append(word)
  for item in get_merged_entries():
    word = item['trad']
    if word not in output_set:
      output_set.add(word)
      output.append(word)
    word = item['simp']
    if word not in output_set:
      output_set.add(word)
      output.append(word)
  return output

def get_word_to_jyutping_corpus_freq(word):
  #trad = HanziConv.toTraditional(word)
  trad = s2hk(word)
  search_results = corpus.search(character=trad)
  output = Counter()
  for x in search_results:
    char = x[0]
    jyut = x[2]
    if char != trad:
      continue
    output[jyut] += 1
  return output

def main():
  output = {}
  seen = set()
  word_list = get_word_list()
  for idx,word in enumerate(word_list):
    if word in seen:
      continue
    if idx % 100 == 0:
      print(word, idx, '/', len(word_list))
    seen.add(word)
    corpus_freq = get_word_to_jyutping_corpus_freq(word)
    if len(corpus_freq.keys()) > 0:
      output[word] = corpus_freq
  json.dump(output, open('jyutping_corpus_freq.json', 'wt'))

main()