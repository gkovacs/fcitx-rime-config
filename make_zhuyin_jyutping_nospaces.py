from memoize import memoize
import pinyin
import jyutping
import pycantonese

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

def print_header():
  print(header_text)

def is_valid_pinyin(pin):
  alpha = 'abcdefghijklmnopqrstuvwxyz'
  alphabet = alpha + alpha.upper()
  all_valid = alphabet + '12345' + ''
  for c in pin:
    if not c in 'abcdefghijklmnopqrstuvwxyz':
      return False
  return True

@memoize
def get_word_to_zhuyin():
  output = {}
  for item in get_merged_entries():
    zhu = item['zhu']
    trad = item['trad']
    simp = item['simp']
    output[trad] = zhu
    output[simp] = zhu
  return output

def get_zhuyin_base(word):
  word_to_zhuyin = get_word_to_zhuyin()
  if word in word_to_zhuyin:
    return word_to_zhuyin[word].strip().replace(' ', '')

def get_zhuyin(word):
  pin = pinyin.get(word, format='numerical', delimiter=' ')
  if is_valid_pinyin(pin):
    return pinyin_to_zhuyin(pin).strip().replace(' ', '')
  return get_zhuyin_base(word)

def get_first_of_all(l):
  output = []
  for x in l:
    if type(x) == type([]):
      output.append(x[0])
    else:
      output.append(x)
  return output

def get_jyutping(word):
  jyut = jyutping.get(word)
  if jyut == None or None in jyut:
    all_yue = get_all_yue(word)
    if len(all_yue) > 0:
      return ''.join(all_yue[0]).strip().replace(' ', '')
    else:
      return None
  else:
    return ''.join(get_first_of_all(jyut)).strip().replace(' ', '')

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

def print_with_pronunciation(word, pin=None):
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
  print(word + '\t' + ''.join(pronunciation))

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
  - luna_pinyin.biaoqing
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
  for dictionary_name in dictionaries:
    #if dictionary_name.startswith('terra_pinyin'):
    #  continue
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
  print_header()

  for word in get_word_list():
    print_with_pronunciation(word)

main()
#print(pinyin_to_zhuyin('lve4'))
#print(get_jyutping('丷'))
#print(pinyin_to_zhuyin('o'))
#print(pinyin_to_zhuyin('O'))
#print_with_pronunciation('二丁目')