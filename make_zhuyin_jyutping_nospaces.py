#!/usr/bin/env python3

import sys
from collections import Counter
import json

from memoize import memoize
import pinyin
import jyutping
# import pycantonese
# corpus = pycantonese.hkcancor()
#from hanziconv import HanziConv
# from opencc import OpenCC
# s2hk = OpenCC('s2hk').convert

from mkdict import pinyin_to_zhuyin_real as pinyin_to_zhuyin
from mkdict import get_all_yue, get_merged_entries

header_text = '''
---
name: leimaau_jyutping_zhuyin_nospaces
version: "20180826"
sort: by_weight #original
use_preset_vocabulary: true
...
'''

def print_header(name, outfile=sys.stdout):
  print(header_text.replace('leimaau_jyutping_zhuyin_nospaces', name), file=outfile)

def is_valid_pinyin(pin):
  alpha = 'abcdefghijklmnopqrstuvwxyz'
  alphabet = alpha + alpha.upper()
  all_valid = alphabet + '12345' + ' '
  for c in pin:
    if not c in all_valid:
      return False
  return True

@memoize
def get_word_to_jyutping_corpus_freq_all():
  return json.load(open('jyutping_corpus_freq.json'))

def get_word_to_jyutping_corpus_freq(word):
  word_to_corpus_freq = get_word_to_jyutping_corpus_freq_all()
  if word in word_to_corpus_freq:
    return word_to_corpus_freq[word]
  return {}

def get_word_to_jyutping_corpus_mostfreq(word):
  jyut_to_freq = get_word_to_jyutping_corpus_freq(word)
  max_count = 0
  jyut_with_max_count = None
  for jyut,count in get_word_to_jyutping_corpus_freq(word).items():
    if count > max_count:
      max_count = count
      jyut_with_max_count = jyut
  return jyut_with_max_count

@memoize
def get_word_to_zhuyin_list2():
  output = {}
  for item in get_merged_entries():
    zhu = item['zhu']
    zhu = zhu.strip().replace(' ', '')
    trad = item['trad']
    simp = item['simp']
    if trad not in output:
      output[trad] = []
    output[trad].append(zhu)
    if trad != simp:
      if simp not in output:
        output[simp] = []
      output[simp].append(zhu)
  return output

@memoize
def get_word_to_zhuyin_list():
  output = {}
  for word,pin in get_word_and_pinyin_in_dictionary('terra_pinyin.dict.yaml'):
    zhu = pinyin_to_zhuyin(pin.strip()).strip().replace(' ', '')
    if word not in output:
      output[word] = []
    output[word].append(zhu)
  return output

def get_all_zhuyin(word):
  output = []
  word_to_zhuyin_list = get_word_to_zhuyin_list()
  word_to_zhuyin_list2 = get_word_to_zhuyin_list2()
  if word in word_to_zhuyin_list:
    output.extend(word_to_zhuyin_list[word])
  if word in word_to_zhuyin_list2:
    output.extend(word_to_zhuyin_list2[word])
  pin = pinyin.get(word, format='numerical', delimiter=' ').strip()
  if is_valid_pinyin(pin) and (len(output) == 0 or len(output) > 1):
    output.insert(0, pinyin_to_zhuyin(pin).strip().replace(' ', ''))
  return output

def get_most_common(item_list):
  counts = Counter(item_list)
  maxcount = max(counts.values())
  for item in item_list:
    count = counts[item]
    if count == maxcount:
      return item

def get_zhuyin(word):
  all_zhuyin = get_all_zhuyin(word)
  if len(all_zhuyin) > 0:
    return get_most_common(all_zhuyin)

def is_unambiguous(item_list):
  for x in item_list:
    if type(x) == type([]):
      return False
  return True

def get_all_jyutping(word):
  output = []
  output.extend(get_all_yue(word))
  word_to_jyutping_list = get_word_to_jyutping_list()
  if word in word_to_jyutping_list:
    output.extend(word_to_jyutping_list[word])
  jyut = jyutping.get(word)
  if jyut != None and None not in jyut:
    if is_unambiguous(jyut) and (len(output) == 0 or len(output) > 1):
      output.insert(0, ''.join(get_first_of_all(jyut)).strip().replace(' ', ''))
  jyut = get_word_to_jyutping_corpus_mostfreq(word)
  if jyut != None:
    output.insert(0, jyut)
  return [x.strip().replace(' ', '') for x in output]

def get_first_of_all(l):
  output = []
  for x in l:
    if type(x) == type([]):
      output.append(x[0])
    else:
      output.append(x)
  return output

@memoize
def get_word_to_jyutping_list():
  output = {}
  for word,jyut in get_word_and_pinyin_in_dictionary('leimaau_jyutping.dict.yaml'):
    if word not in output:
      output[word] = []
    output[word].append(jyut)
  return output

def get_jyutping(word):
  all_jyutping = get_all_jyutping(word)
  if len(all_jyutping) > 0:
    return get_most_common(all_jyutping)

def get_header_in_dictionary(dictfile):
  lines = open(dictfile).readlines()
  output = []
  for line in lines:
    x = line.strip()
    if x == '...':
      output.append(x)
      return output
    output.append(line)

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

def get_words_in_dictionary(dictfile):
  lines = open(dictfile).readlines()
  output = []
  is_started = False
  for x in lines:
    x = x.strip()
    if x == '...':
      is_started = True
      continue
    if not is_started:
      continue
    if x == '':
      continue
    output.append(x)
  return output

def print_with_pronunciation(word, pin=None, outfile=sys.stdout):
  if pin == None:
    zhu = get_zhuyin(word)
  else:
    zhu = pinyin_to_zhuyin(pin).strip()
  jyut = get_jyutping(word)
  if zhu != None and jyut != None:
    #pronunciation = jyut
    pronunciation = zhu + jyut
  elif zhu != None and jyut == None:
    #return
    pronunciation = zhu
  elif jyut != None and zhu == None:
    pronunciation = jyut
  else:
    return
  print(word + '\t' + ''.join(pronunciation), file=outfile)

def print_with_pronunciation_jyutzhu(word, pin=None, outfile=sys.stdout):
  if pin == None:
    zhu = get_zhuyin(word)
  else:
    zhu = pinyin_to_zhuyin(pin).strip()
  jyut = get_jyutping(word)
  if zhu != None and jyut != None:
    #pronunciation = jyut
    pronunciation = jyut + zhu
  elif zhu != None and jyut == None:
    #return
    pronunciation = zhu
  elif jyut != None and zhu == None:
    pronunciation = jyut
  else:
    return
  print(word + '\t' + ''.join(pronunciation), file=outfile)

def print_with_pronunciation_zhu(word, pin=None, outfile=sys.stdout):
  if pin == None:
    zhu = get_zhuyin(word)
  else:
    zhu = pinyin_to_zhuyin(pin).strip()
  if zhu != None:
    pronunciation = zhu
  else:
    return
  print(word + '\t' + ''.join(pronunciation), file=outfile)

def print_with_pronunciation_jyut(word, pin=None, outfile=sys.stdout):
  jyut = get_jyutping(word)
  if jyut != None:
    pronunciation = jyut
  else:
    return
  print(word + '\t' + ''.join(pronunciation), file=outfile)

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

def main():
  #for x in get_header_in_dictionary('terra_pinyin.dict.yaml'):
  #  print(x, end='')
  outfile = open('leimaau_jyutping_zhuyin_nospaces.dict.yaml', 'wt')
  print_header('leimaau_jyutping_zhuyin_nospaces', outfile=outfile)
  for word in get_word_list():
    print_with_pronunciation(word, outfile=outfile)
  outfile.close()
  outfile = open('leimaau_zhuyin_jyutping_nospaces.dict.yaml', 'wt')
  print_header('leimaau_zhuyin_jyutping_nospaces', outfile=outfile)
  for word in get_word_list():
    print_with_pronunciation_jyutzhu(word, outfile=outfile)
  outfile.close()
  outfile = open('terra_pinyin_nospaces.dict.yaml', 'wt')
  print_header('terra_pinyin_nospaces', outfile=outfile)
  for word in get_word_list():
    print_with_pronunciation_zhu(word, outfile=outfile)
  outfile.close()
  outfile = open('terra_pinyin_nospaces.extended.dict.yaml', 'wt')
  print_header('terra_pinyin_nospaces.extended', outfile=outfile)
  for word in get_word_list():
    print_with_pronunciation_zhu(word, outfile=outfile)
  outfile.close()
  outfile = open('leimaau_jyutping_nospaces.dict.yaml', 'wt')
  print_header('leimaau_jyutping_nospaces', outfile=outfile)
  for word in get_word_list():
    print_with_pronunciation_jyut(word, outfile=outfile)
  outfile.close()

if __name__ == '__main__':
  main()
#print(get_word_to_jyutping_corpus_mostfreq('从'))
#print(get_all_jyutping('从'))
#print(get_all_jyutping('從'))
#print(get_all_zhuyin('炒鱿鱼'))
#print(get_zhuyin_base('垃圾'))
#print(pinyin.get('垃圾', format='numerical', delimiter=' '))
#print(get_all_zhuyin('垃圾'))
# print(get_all_jyutping('什么'))
# print(get_all_zhuyin('说'))
# print(get_all_jyutping('说'))
#print(get_all_zhuyin('垃圾'))
#print(get_word_to_zhuyin_list()['垃圾'])
#print(get_word_to_zhuyin_list2()['垃圾'])
# for item in get_merged_entries():
#   zhu = item['zhu']
#   zhu = zhu.strip().replace(' ', '')
#   trad = item['trad']
#   simp = item['simp']
#   if trad == '大家好' or simp == '大家好':
#     print(item)
#     sys.exit()
# print(get_word_to_zhuyin_list()['大家好'])
#print(get_word_to_zhuyin_list2()['大家好'])
#print(get_word_to_zhuyin_list2())
#print(pinyin_to_zhuyin('yo1'))
#print(pinyin_to_zhuyin('yo'))
#print(pinyin_to_zhuyin('lve4'))
#print(get_jyutping('為'))
#print(get_jyutping('爲'))
#print(get_jyutping('为'))
#print(get_jyutping('丷'))
#print(pinyin_to_zhuyin('o'))
#print(pinyin_to_zhuyin('O'))
#print_with_pronunciation('二丁目')
#print(get_all_zhuyin('大家好'))
#print(get_all_jyutping('什么'))
#print(get_zhuyin_base('大家好'))
#print(is_valid_pinyin(pinyin.get('大家好', format='numerical', delimiter=' ')))